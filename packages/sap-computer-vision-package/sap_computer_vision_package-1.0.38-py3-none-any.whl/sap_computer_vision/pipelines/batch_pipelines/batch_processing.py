import pathlib
import json
import logging
from typing import List, Dict
from functools import partial

import torch
from metaflow import FlowSpec, step, argo, argo_base, Parameter, JSONType
import numpy as np

from detectron2.config import CfgNode
from detectron2.structures import Instances
from detectron2.checkpoint import DetectionCheckpointer

from sap_computer_vision import setup_loggers, get_cfg
import sap_computer_vision.datasets.image_folder as imgf
from sap_computer_vision.utils.object_detection import torchvision_nms_on_model_output


@argo_base(
    labels={'scenarios.ai.sap.com/id': 'scenario-id',
            'ai.sap.com/version': 'scenario-version'},
    annotations={'scenarios.ai.sap.com/name': 'scenario-name',
                 'executables.ai.sap.com/name': 'executable-name',
                 'artifacts.ai.sap.com/datain.kind': 'dataset',
                 'artifacts.ai.sap.com/trainedmodel.kind': 'model'},
    image='mlf.docker.repositories.sapcdn.io/com.sap.ai/sap_cv_metaflow:0.0.25',
    imagePullSecrets=[{'name': 'your-image-pull-secret'}],
    envFrom=[{'secretRef': {'name': 'default-object-store-secret'}}],
    volumes=[{'name': 'dshm', 'emptyDir': {'medium': 'Memory'}}])
class BatchProcessing(FlowSpec):
    """Pipeline to batch processing data using a trained model.
    """
    # Constant values for during processing
    DATA_INPUT_DIR = pathlib.Path('/tmp/datain')
    MODEL_INPUT_DIR = pathlib.Path('/tmp/model')
    RESULT_OUTPUT_DIR = pathlib.Path('/tmp/results')
    DATASET_NAME = "predict_dataset"
    FALLBACK_TASK = 'IMAGE_CLASSIFICATION'
    # Pipeline parameters
    model_filename = Parameter("modelfile",
                         help=f"",
                         default='')
    batch_size = Parameter("batchsize",
                           help="Number of images per batch. Set to a value <= 0 to use the batch size used during training.",
                           default=0)
    imgtypes = Parameter("imgtypes",
                         help="Json encoded list of class names of expected images types",
                         type=JSONType,
                         default=json.dumps([".jpg", ".jpeg", ".png"]))
    imgtypes = Parameter("imgtypes",
                         help="Json encoded list of class names of expected images types",
                         type=JSONType,
                         default=json.dumps([".jpg", ".jpeg", ".png"]))
    iou_threshold = Parameter("iouthreshold",
                              help="Non-maximum suppression iou threshold for object detection. Only applied when the value is >= 0 and <= 1.",
                              type=float,
                              default=-1.0)
    @argo(output_artifacts=[{'name': 'results',
                             'globalName': 'results',
                             'path': str(RESULT_OUTPUT_DIR),
                             'archive': {'none': {}}}],
          input_artifacts=[{'name': 'datain',
                            'path': str(DATA_INPUT_DIR)},
                           {'name': 'modelin',
                            'path': str(MODEL_INPUT_DIR)}],
          labels={"ai.sap.com/resourcePlan": "train.l"},
          volumeMounts=[{'mountPath': '/dev/shm', 'name': 'dshm'}])
    @step
    def start(self):
        """In this step the model is trained.
        """
        logger = logging.getLogger(__name__)
        setup_loggers(str(self.RESULT_OUTPUT_DIR), color=False, additional_loggers=[__name__])
        model_folder = pathlib.Path(self.MODEL_INPUT_DIR)
        cfg_path = pathlib.Path(model_folder / 'used_config.yaml' )
        with cfg_path.open() as stream:
            cfg = CfgNode.load_cfg(stream)

        model_file = [model_folder / f for f in [self.model_filename, 'model_best.pth', 'model_final.pth'] if (model_folder / f ).exists()]
        if len(model_file) == 0:
            raise RuntimeError('No model found!')
        model_file = model_file[0]
        cfg.MODEL.DEVICE = get_cfg().MODEL.DEVICE
        cfg.MODEL.WEIGHTS = str(model_file)
        cfg.INPUT.IMS_PER_BATCH_EVAL = self.batch_size if self.batch_size > 0 else cfg.INPUT.IMS_PER_BATCH_EVAL
        images, _ = imgf.register(self.DATASET_NAME,
                                  base_dir=self.DATA_INPUT_DIR,
                                  extensions=self.imgtypes,
                                  class_names=cfg.TRAINING_INFO.get('THING_CLASSES', None))
        if len(images) == 0:
            raise RuntimeError('No images found!')

        result_output_path = pathlib.Path(self.RESULT_OUTPUT_DIR)
        result_output_path.mkdir(parents=True, exist_ok=True)
        with (result_output_path / 'used_config.yaml').open('w') as stream:
            stream.write(cfg.dump())

        self.task = cfg.TRAINING_INFO.get('TASK', 'UNKNOWN')
        if self.task == 'UNKNOWN':
            logger.warn(f"Unknown task: {self.task }. Try to process data using '{self.FALLBACK_TASK}' trainer as fallback.")

        if self.task == 'OBJECT_DETECTION' or self.FALLBACK_TASK == 'OBJECT_DETECTION':
            from sap_computer_vision.engine import ObjectDetectionTrainer as trainer
        elif self.task == 'IMAGE_CLASSIFICATION' or self.FALLBACK_TASK == 'IMAGE_CLASSIFICATION':
            from sap_computer_vision.engine import ImageClassificationTrainer as trainer
        elif self.task == 'TRIPLET_DISTANCE_MERIC_LEARNING' or self.FALLBACK_TASK == 'TRIPLET_DISTANCE_MERIC_LEARNING':
            from sap_computer_vision.engine import TripletDistanceTrainer as trainer
        model = trainer.build_model(cfg)
        checkpointer = DetectionCheckpointer(model)
        checkpointer.load(cfg.MODEL.WEIGHTS)
        dl_val = trainer.build_test_loader(cfg, self.DATASET_NAME)

        if isinstance(self.iou_threshold, float) and self.iou_threshold >= 0.0 and self.iou_threshold <= 1.0:
            nms_f = partial(torchvision_nms_on_model_output, device='cpu', iou_threshold=float(self.iou_threshold))
        else:
            nms_f = lambda batch: batch
        with JSONSaver(self.task, self.RESULT_OUTPUT_DIR, self.DATA_INPUT_DIR, self.combined, self.max_size) as saver:
            with torch.no_grad():
                model.eval()
                for batch in dl_val:
                    output = model(batch)
                    if self.task == 'OBJECT_DETECTION':
                        output = nms_f(output)
                    saver.register_batch(batch, output)
        self.next(self.end)

    @step
    def end(self):
        """Currently this step is empty, but it is added because
        metaflow DAGs always need a \'start\' and \'end\' step.
        """
        pass


class JSONSaver:
    def __init__(self, task, target_dir, data_in_dir, combined=True, max_size=None):
        self.task = task
        self._counter = 0
        self.combined = combined
        self.target_dir = pathlib.Path(target_dir)
        self.result_buffer = [] if combined else None
        self._in_context = False
        self.max_size = max_size if isinstance(max_size, int) and max_size > 0 else None
        self.crop_filename = lambda f: str(f).replace(str(self.data_in_dir) + '/', '')
        self.data_in_dir = data_in_dir

    def __enter__(self):
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self._in_context = True
        return self

    def __exit__(self, type, value, traceback):
        self._in_context = False
        if self.result_buffer and len(self.result_buffer) > 0:
            self._clear_buffer()

    def register_batch(self, model_input, model_output):
        model_output = results_to_jsonable_result_list(self.task, model_output)
        for in_, out_ in zip(model_input, model_output):
            in_file = self.crop_filename(in_['file_name'])
            out_['filename'] = in_file
            self.register_result(in_file, out_)

    def register_result(self, in_file, result):
        self._counter += 1
        if self.combined:
            self.result_buffer.append(result)
            if self.max_size:
                if self._counter % self.max_size == 0:
                    self._clear_buffer()
        else:
            out_file = self.target_dir / in_file.with_suffix('.json')
            with out_file.open() as stream:
                json.dump(result, stream)

    def _clear_buffer(self, base_name='results'):
        s, e = self._counter - len(self.result_buffer), self._counter - 1
        filenamne = base_name + (f'{s}-{e}'if self.max_size else '') + '.json'
        with (self.target_dir / filenamne).open('w') as stream:
            json.dump(self.result_buffer, stream)
        self.result_buffer = []


def results_to_jsonable_result_list(task, res, thing_classes=None) -> List[Dict]:
    result_list = []
    if task == 'OBJECT_DETECTION':
        for res_i in res:
            res_i = res_i['instances'].to('cpu')
            res_i = {**res_i.get_fields()}
            res_i['scores'] = res_i['scores'].tolist()
            res_i['pred_boxes'] = res_i['pred_boxes'].tensor.tolist()
            res_i['pred_classes'] = res_i['pred_classes'].tolist()
            result_list.append(res_i)
    elif task == 'IMAGE_CLASSIFICATION':
        probs = res.cpu().numpy()
        idx_max = np.argmax(probs, axis=1)
        if thing_classes is not None:
            predicted_class = [thing_classes[i] for i in idx_max]
        else:
            predicted_class = [''] * len(idx_max)
        for p, i, c in zip(probs, idx_max, predicted_class):
            result_list.append({'probs': p.tolist(), 'idx_max': i, 'pred_class': c})
    elif task == 'TRIPLET_DISTANCE_MERIC_LEARNING':
        embedding = res.squeeze().cpu().numpy()
        result_list.extend([{'embedding': embedding_i.tolist()} for embedding_i in embedding])
    return result_list

if __name__ == '__main__':
    from sap_computer_vision.utils.metaflow_utils import add_parameters_help_to_doc_string
    add_parameters_help_to_doc_string(BatchProcessing)
    BatchProcessing()

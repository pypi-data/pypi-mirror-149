import pathlib
import json
from metaflow import FlowSpec, step, argo, argo_base, Parameter, JSONType

DATA_OUTPUT_DIR = str(pathlib.Path('/tmp/dataout'))
DATA_INPUT_DIR = pathlib.Path('/tmp/datain')


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
class PrepareTraining(FlowSpec):
    """Pipeline to train a model for image classification.
    """
    data_input = Parameter("datain",
                       help=f"Name of the file within {DATA_INPUT_DIR} containing filenames of the validation dataset.",
                       default="val.txt")
    image_target_size = Parameter("imagesize",
                                  help=f"Image size of the prepared data.",
                            type=JSONType,
                            default=json.dumps([500, 500]))
    seed = Parameter("seed",
                     help="Random seed.",
                     default=1337)
    @argo(output_artifacts=[{'name': 'prepareddata',
                             'globalName': 'prepareddata',
                             'path': str(DATA_OUTPUT_DIR),
                             'archive': {'none': {}}}],
          input_artifacts=[{'name': 'datain',
                            'path': str(DATA_INPUT_DIR)}],
          labels={"ai.sap.com/resourcePlan": "train.l"},
          volumeMounts=[{'mountPath': '/dev/shm', 'name': 'dshm'}])
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    from sap_computer_vision.utils.metaflow_utils import add_parameters_help_to_doc_string
    add_parameters_help_to_doc_string(PrepareTraining)
    PrepareTraining()

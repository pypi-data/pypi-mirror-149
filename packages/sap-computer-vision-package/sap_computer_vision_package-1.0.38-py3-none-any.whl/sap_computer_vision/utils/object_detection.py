from typing import Union, Iterable, Dict

from torchvision.ops import nms
from functools import partial
from detectron2.structures import Instances


def torchvision_nms_on_model_output(model_output: Union[Dict[str, 'Instances'],
                                                        Iterable[Dict[str, 'Instances']],
                                                        'Instances',
                                                        Iterable['Instances']],
                                    iou_threshold: float=0.5,
                                    device=None):
    single_result = isinstance(model_output, Instances) or isinstance(model_output, dict)
    if single_result:
        model_output = [model_output]
    f_ = partial(nms_single_result, iou_threshold=iou_threshold, device=device)
    new_instances = [f_(inst) for inst in model_output]
    if single_result:
        return new_instances[0]
    else:
        return new_instances


def keep_input_output_format(f):

    def wrapped(model_output, iou_threshold, device):
        f_ = lambda inst: f(inst if device is None else inst.to(device), iou_threshold)
        if isinstance(model_output, dict):
            return {**model_output, **{'instances': f_(model_output['instances'])}}
        elif isinstance(model_output, Instances):
            return f_(model_output)
        else:
            raise AttributeError('')

    return wrapped


@keep_input_output_format
def nms_single_result(instances: 'Instances', iou_threshold: float=0.5) -> 'Instances':
    res = {k: v for k, v in instances.get_fields().items()}
    indices = nms(res['pred_boxes'].tensor, res['scores'], iou_threshold).detach().numpy()
    res_new = {k: v[indices] for k, v in res.items()}
    return Instances(
        image_size=instances.image_size,
        **res_new
    )

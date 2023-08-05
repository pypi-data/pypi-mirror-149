"""This module creates the cli for this package."""
import pathlib
import os
from re import M

import yaml
from ai_core_content_package_utils.cli import create_cli_for_module

import sap_computer_vision.pipelines
from sap_computer_vision import SAP_COMPUTER_VISION_DIR, DISCLAIMER, LICENSE

# TODO: provide an example pipeline-config yaml for the template generation (as it's unusable otherwise)

PIPELINES_ENVVAR = 'SAP_CV_PIPELINE_YAMLS'
PIPELINES_DIR = SAP_COMPUTER_VISION_DIR / 'pipelines'
EXAMPLES_DIR = SAP_COMPUTER_VISION_DIR / 'examples'

try:
    pipeline_env = os.environ['SAP_CV_PIPELINE_YAMLS']
except KeyError:
    pipeline_env = ''

pipelines = {}

for p in [PIPELINES_DIR / 'pipelines.yaml'] + pipeline_env.split(':'):
    p = pathlib.Path(p).resolve().absolute()
    if p.exists() and p.is_file():
        with p.open() as stream:
            pipelines_i = yaml.load(stream, Loader=yaml.SafeLoader)
        for pipeline, pipeline_info in pipelines_i.items():
            pipeline_info['_pipeline_dir'] = p.parent
        pipelines = {**pipelines, **pipelines_i}


cli = create_cli_for_module(sap_computer_vision,
                            sap_computer_vision.pipelines,
                            pipelines,
                            examples_dir=EXAMPLES_DIR,
                            show_files={
                                'disclaimer': DISCLAIMER,
                                'license': LICENSE,
                            })


if __name__ == '__main__':
    cli() # pylint: disable=E1120

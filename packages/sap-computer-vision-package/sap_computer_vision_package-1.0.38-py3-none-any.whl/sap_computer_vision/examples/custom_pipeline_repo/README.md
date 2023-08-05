# Add Custom Pipeline Repository

The pipeliens delivered by the `sap-computer-vision-package` are organized as a *content repository*. Every pipeline consists out of a python file and a set of dockerfiles. In the python file the pipeline is implemented as a `metaflow.FlowSpec`. The dockerfiles are used to generate the docker container that will be used as the pipeline`s execution environment.

## Structure of a Pipeline Repository

We recommend to create a new folder and keep only the needed files in the folder and subfolders.

Example:

```
pipeline_repository_folder
↳ pipelines.yaml
↳ prepare_data_pipeline
  ↳ metaflow_pipeline.py
  ↳ DockerfileCPU
  ↳ DockerfileGPU
↳ pipeline_2
  ↳ metaflow_pipeline.py
  ↳ Dockerfile
...
```
In the root of the repository a yaml file is used to define the content of the repository. For the example above the content would be:

```
prepare_data:
    py: prepare_data_pipeline/metaflow_pipeline.py
    class_name: PrepareTraining
    dockerfile:
        gpu:
            file: DockerfileGPU
        cpu:
            file: DockerfileCPU
evaluate_model:
    py: pipeline_2/metaflow_pipeline.py
    class_name: EvaluateModel
    dockerfile: Dockerfile
```

Every pipeline has its own entry and the keys of the entries (`prepare_data`/`evaluate_model`) are the names used to reference the pipeline in the CLI. `<pipeline_name>/py` is the relative path of the python file containing the `metaflow.FlowSpec`. `<pipeline_name>/class_name` is the name of the `metaflow.FlowSpec` class. For the dockerfiles either a set of dockerfiles (see example `prepare_data` pipeline) or a single dockerfile (see example `evaluate_model` pipeline) can be used. A set of dockerfiles is defined as a dict with the sturcture:
```
<docker_type_a>:
    file: <relative_path_to_the_dockerfile>
<docker_type_b>:
    file: <relative_path_to_the_dockerfile>
```
The first entry it the default dockerfile for the commands `sap_cv build-docker/dockerfile`. To select a different file use the `--docker-type=<docker_type>` option when execution the commands.

All paths in this yaml are relative to the folder containing the yaml file.

## Add a Custom Repository to the CLI

To add a custom repository to the CLI the path to the yaml has to be exposed through the environment variable `SAP_CV_PIPELINE_YAMLS`.

To add the pipeline repository from this package`s examples run:
```
# 1. Create a local copy of the examples
sap_cv examples sap_cv_examples_folder
# 2. Add yaml to SAP_CV_PIPELINE_YAMLS environment varialbe
export SAP_CV_PIPELINE_YAMLS=$PWD/sap_cv_examples_folder/custom_pipeline_repo/pipelines.yaml:$SAP_CV_PIPELINE_YAMLS
```
To test it run `sap_cv show` with an empty environment variable and the with extended variable.

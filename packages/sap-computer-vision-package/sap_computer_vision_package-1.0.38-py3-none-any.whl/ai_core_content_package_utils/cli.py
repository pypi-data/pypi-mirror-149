from os import pipe
import sys
import contextlib
import re
import shutil
import pathlib
from subprocess import run, call
import textwrap
import importlib
from importlib.machinery import SourceFileLoader
import tempfile
import json
import warnings
from types import ModuleType
from functools import partial

import yaml
import click

from metaflow.plugins.argo.argo_decorator import ArgoFlowDecorator


VALID_KEYWORDS = [*ArgoFlowDecorator.defaults.keys()]


class PipelineNotFound(Exception):

    def __init__(self, ctx, requested_pipeline):
        self.avaible_pipelines_message = 'Pipelines available are:\n' + '\n'.join([f'\t- {k}' for k in ctx.obj['pipelines'].keys()])
        self.pipeline = requested_pipeline
        self.message = f'Pipline `{self.pipeline}` not found!\n' + self.avaible_pipelines_message
        super().__init__(self.message)


def camel_to_kebap(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()


def split_kw_args(argv, pipeline_config=None, valid_keywords=VALID_KEYWORDS):
    if pipeline_config:
        pipeline_config = pathlib.Path(pipeline_config)
        with pipeline_config.open() as stream:
            pipeline_config = yaml.load(stream, Loader=yaml.SafeLoader)
        for k, v in pipeline_config.items():
            if not isinstance(v, str):
                pipeline_config[k] = json.dumps(v)
            else:
                pipeline_config[k] = v

        pipeline_config = {camel_to_kebap(k): s for k, s in pipeline_config.items()}
    else:
        pipeline_config = {}
    p = re.compile('--(.*?)=')
    valid_keywords = [camel_to_kebap(k) for k in valid_keywords]
    added_option = set()
    not_matching_argv, matching_argv = [], []
    for a in argv:
        match = p.search(a)
        if match:
            kw = match.group(1)
            if kw in valid_keywords:
                matching_argv.append(a)
                added_option.add(kw)
            else:
                not_matching_argv.append(a)
        else:
            not_matching_argv.append(a)
    argo_options = []
    for k, v in pipeline_config.items():
        if k not in added_option and k in valid_keywords:
            matching_argv.append(f'--{k}={v}')
        else:
            argo_options.append(f'--{k}={v}')
    return not_matching_argv, argo_options, matching_argv


def get_pipeline_infos(ctx, pipeline_name):
    try:
        return ctx.obj['pipelines'][pipeline_name]
    except KeyError:
        raise PipelineNotFound(ctx, pipeline_name)


def list_dockerfiles(pipeline_infos):
    dockerfiles = pipeline_infos['dockerfile']
    if isinstance(dockerfiles, str):
        click.echo('For this pipeline only one Dockerfile is registered!')
    elif isinstance(dockerfiles, dict):
        msg = ['Available types:'] + [f'\t- {t}' for t in dockerfiles.keys()]
        click.echo('\n'.join(msg))


def get_dockerfile(pipeline_infos, docker_type=None):
    pipelines_dir = pipeline_infos['_pipeline_dir']
    dockerfiles = pipeline_infos['dockerfile']
    if isinstance(dockerfiles, str):
        docker_context = pipeline_infos.get('docker_needs_context', False)
        dockerfile = dockerfiles
    elif isinstance(dockerfiles, dict):
        if not docker_type:
            docker_type = [*dockerfiles.keys()][0] if not docker_type else docker_type
        try:
            dockerfile = dockerfiles[docker_type]
        except KeyError:
            raise ValueError(f'`{docker_type}` is not a registered type of Dockerfile. '
                             f'Registered types: {", ".join([*dockerfiles.keys()])}')
        docker_context = dockerfile.get('docker_needs_context', False)
        dockerfile = dockerfile['file']
    else:
        raise RuntimeError('This is very much expected and most probably an error in the pipeline config! '
                           'Key `dockerfile` should be either a dict with '
                           '`docker_type: {file: <relative_path>, docker_needs_context: True/False}` '
                           'or a str (path directly to the Dockerfile).')
    dockerfile = pipelines_dir / dockerfile
    return dockerfile, docker_context


def create_cli_for_module(module,
                          pipelines_submodule,
                          pipelines,
                          examples_dir=None,
                          show_files={}):
    examples_dir = pathlib.Path(examples_dir) if examples_dir and pathlib.Path(examples_dir).exists() else None

    @click.group()
    @click.pass_context
    def cli(ctx):
        ctx.ensure_object(dict)
        ctx.obj['module'] = module
        ctx.obj['pipelines'] = pipelines

    @cli.command()
    @click.pass_context
    @click.argument('pipeline', nargs=1, type=str)
    @click.option('--clean', 'clean', is_flag=True)
    @click.option('--list-types', 'list_types', is_flag=True, default=None)
    @click.option('--docker-type', 'docker_type', type=str, default=None)
    def dockerfile(ctx, pipeline, clean, list_types=False, docker_type=None):
        pipeline_infos = get_pipeline_infos(ctx, pipeline)
        if list_types:
            list_dockerfiles(pipeline_infos)
            return
        dockerfile, docker_context = get_dockerfile(pipeline_infos, docker_type)
        if not clean:
            if docker_context:
                click.echo(click.style('Dockerfile needs specific build context!', fg='red'))
                if isinstance(docker_context, str):
                    click.echo(click.style('It comes with custom script to create the correct contet.', fg='red'))
                    click.echo("Run:", nl=True)
                    click.echo(click.style(f'sap_cv docker-build {pipeline} [DOCKEROPTIONS]\n', fg='green'))
                else:
                    click.echo(" You can either run:", nl=True)
                    click.echo(click.style(f'docker build [DOCKEROPTIONS] -f {dockerfile} {dockerfile.parent}', fg='green'))
                    click.echo("or:", nl=True)
                    click.echo(click.style(f'sap_cv docker-build {pipeline} [DOCKEROPTIONS]\n', fg='green'))
            else:
                click.echo("You can either run:", nl=True)
                click.echo(click.style(f'sap_cv dockerfile {pipeline} >> Dockerfile && docker build [DOCKEROPTIONS] .', fg='green'))
                click.echo("or:", nl=True)
                click.echo(click.style(f'sap_cv docker-build {pipeline} [DOCKEROPTIONS]\n', fg='green'))
        with dockerfile.open() as stream:
            if not clean:
                click.echo(click.style(f'Dockerfile [{dockerfile}]\n' + "="*20 + "\n", fg='blue'))
            click.echo(stream.read())

    @cli.command(context_settings=dict(ignore_unknown_options=True), add_help_option=False)
    @click.pass_context
    @click.argument('pipeline', nargs=1, type=str)
    @click.argument('pipeline_args', nargs=-1, type=click.UNPROCESSED)
    def raw_metaflow_cli(ctx, pipeline, pipeline_args):
        pipeline_infos = get_pipeline_infos(ctx, pipeline)
        py = pipeline_infos['_pipeline_dir'] / pipeline_infos['py']
        cwd = py.parent
        flow = py.stem
        cmdline = ['python', f'-m{flow}'] + [*pipeline_args]
        call(cmdline, cwd=cwd)

    @cli.command(context_settings=dict(ignore_unknown_options=True))
    @click.pass_context
    @click.argument('pipeline', nargs=1, type=str)
    @click.argument('pipeline_args', nargs=-1, type=click.UNPROCESSED)
    @click.option('--argo-help', 'argo_help', is_flag=True)
    @click.option('--pipeline-config', 'pipeline_config', type=click.Path(exists=True), default=None, help=', '.join(VALID_KEYWORDS))
    @click.option('-o', '--output-file', 'target_file', type=click.Path(), default=None)
    def create_template(ctx, pipeline, target_file, pipeline_args, argo_help, pipeline_config):
        pipeline_infos = get_pipeline_infos(ctx, pipeline)
        if 'template' in pipeline_infos.keys():
            template_file = pipeline_infos['_pipeline_dir'] / pipeline_infos['template']
            with template_file.open() as stream:
                if target_file:
                    with open(target_file, 'w') as f:
                        f.write(stream.read())
                else:
                    click.echo(stream.read())
        else:
            py = pipeline_infos['_pipeline_dir'] / pipeline_infos['py']
            cwd = py.parent
            flow = py.stem
            metaflow_args, argo_args, pipeline_args = split_kw_args(pipeline_args, pipeline_config)
            template_kwargs = pipeline_infos.get('template_kwargs', {})
            metaflow_args += [f'--{key}={value}' for key, value in template_kwargs.items()]
            cmdline = ['python', f'-m{flow}']
            cmdline += [*metaflow_args]
            cmdline += ['argo'] + argo_args + ['create']
            if argo_help:
                cmdline += ['--help']
                r = run(cmdline, cwd=cwd)
            else:
                cmdline += [*pipeline_args]
                cmdline += ['--only-json']
                if target_file:
                    with open(target_file, 'w') as f:
                        run(cmdline, stdout=f, cwd=cwd)
                else:
                    run(cmdline, cwd=cwd)

    @cli.command(context_settings=dict(ignore_unknown_options=True))
    @click.pass_context
    @click.option('--docker-help', 'docker_help', is_flag=True)
    @click.option('--list-types', 'list_types', is_flag=True, default=None)
    @click.option('--docker-type', 'docker_type', type=str, default=None)
    @click.argument('pipeline', nargs=1, type=str)
    @click.argument('docker_args', nargs=-1, type=click.UNPROCESSED)
    def build_docker(ctx, pipeline, docker_args, docker_help, list_types=False, docker_type=None):
        if docker_help:
            run(['docker', 'build', '--help'])
        else:
            pipeline_infos = get_pipeline_infos(ctx, pipeline)
            if list_types:
                list_dockerfiles(pipeline_infos)
                return
            dockerfile, docker_context = get_dockerfile(pipeline_infos, docker_type)
            module_dir = pathlib.Path(ctx.obj['module'].__file__).parent
            if docker_context:
                @contextlib.contextmanager
                def build_dir():
                    with tempfile.TemporaryDirectory() as t_dir:
                        t_dir = pathlib.Path(t_dir)
                        shutil.copytree(dockerfile.parent, t_dir, dirs_exist_ok=True)
                        dest = t_dir / ctx.obj['module'].__name__
                        shutil.copytree(module_dir, dest)
                        yield (t_dir / dockerfile.name), t_dir
            else:
                @contextlib.contextmanager
                def build_dir():
                    yield dockerfile, dockerfile.parent

            click.echo(click.style(f'Building Dockerfile: {dockerfile}\n' + "="*20 + "\n", fg='blue'))
            with build_dir() as (dockerfile, build_context):
                pkg_version = getattr(ctx.obj['module'], '__version__', None)
                if pkg_version is not None:
                    pkg_version = ["--build-arg", f"pkg_version==={pkg_version}"]
                else:
                    pkg_version = ["--build-arg", f'pkg_version=']
                cmd = ['docker', 'build', *docker_args, *pkg_version, f'-f{dockerfile}', f'{build_context}']
                run(cmd)

    @cli.command(context_settings=dict(ignore_unknown_options=True))
    @click.pass_context
    @click.argument('pipeline', nargs=1, type=str, required=False, default='*')
    @click.argument('metaflow_args', nargs=-1, type=click.UNPROCESSED)
    def show(ctx, pipeline, metaflow_args):
        wrapper = textwrap.TextWrapper(initial_indent="\t- ", tabsize=4, expand_tabs=True, subsequent_indent='\t  ')
        import sap_computer_vision.pipelines as p

        def print_pipeline(name):
            pipeline_infos = get_pipeline_infos(ctx, name)
            deployable = pipeline_infos.get('template', None)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                module_name = pipeline_infos["class_name"].lower() + "_.name"
                file_name =str(pipeline_infos['_pipeline_dir'] / pipeline_infos['py'])
                module = SourceFileLoader(module_name, file_name).load_module()
            pipeline = getattr(module, pipeline_infos['class_name'])
            msg = click.style(name + (' [Deployment]' if deployable else ' [Execution]'), fg='magenta' if deployable else 'green')
            msg += "\n" + "="*20 + "\n"
            doc_str = pipeline.__doc__
            doc_str = doc_str.replace('\n', ' ')
            doc_str = doc_str.replace('\t', ' ')
            doc_str = re.sub(' +', ' ', doc_str)
            msg += wrapper.fill(doc_str) + '\n'
            for m in [m for m in sys.modules if m.startswith('metaflow')]:
                sys.modules.pop(m)
            return pipeline_infos['_pipeline_dir'], msg

        if pipeline == '*':
            pipelines = {}
            for k, v in ctx.obj["pipelines"].items():
                pipeline_dir, msg = print_pipeline(k)
                repo_piplines = pipelines.setdefault(pipeline_dir, [])
                repo_piplines.append(msg)
            for repo, msgs in pipelines.items():
                click.echo(click.style(repo, fg='bright_black'))
                msg = ''.join(msgs)
                click.echo(msg)


        else:
            flow = get_pipeline_infos(ctx, pipeline)
            if 'template' in flow.keys():
                print_pipeline(pipeline)
            else:
                from sap_computer_vision.utils.metaflow_utils import add_parameters_help_to_doc_string
                from metaflow.cli import cli
                module = SourceFileLoader("module", str(flow['_pipeline_dir'] / flow['py'])).load_module()
                pipeline = getattr(module, flow['class_name'])
                f = cli.commands['show'].callback
                while hasattr(f, '__wrapped__'):
                    f = f.__wrapped__
                add_parameters_help_to_doc_string(pipeline)
                class GraphProxy:
                    graph = pipeline(use_cli=False)._graph
                f(GraphProxy)

    if examples_dir is not None:
        @cli.command(context_settings=dict(ignore_unknown_options=True))
        @click.pass_context
        @click.argument('target_dir', nargs=1, type=str, required=False, default=None)
        def examples(ctx, target_dir):
            if target_dir is None:
                click.echo('This commands creates a folder containing examples for the package.\n'
                           'E.g.: `sap_cv examples <target_folder_name>`.')
            else:
                target_dir = pathlib.Path(target_dir)
                if target_dir.exists():
                    click.echo(f'{target_dir} already exists. Please choose another target directory.')
                else:
                    target_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(examples_dir, target_dir)

    def echo_file(f):
        f = pathlib.Path(f)
        with f.open() as stream:
            s = stream.read()
        s += f'\n[File: {f.absolute()}]'
        click.echo(s)

    for n, f in show_files.items():
        if not pathlib.Path(f).exists():
            continue
        cli.command(name=n.lower())(partial(echo_file, f=f))

    return cli

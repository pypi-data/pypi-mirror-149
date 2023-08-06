import json
import os

from ruamel.yaml import YAML

from build_utils import docker_utils, utils
from build_utils.execution_context import ExecutionContext
from build_utils.rules import (
    build_docker_image,
    build_generic_artifact,
    build_maven_artifact,
    build_npm_package,
    create_elastic_beanstalk_docker_app_bundle,
    create_tar_archive,
    get_image_tag_from_config,
    get_passthrough_config,
    write_output_to_hcl,
    write_output_to_json,
    write_output_to_cfn_parameters
)

yaml = YAML(typ='safe')

def execute_child_builds(execution_context, definition_paths):
    build_rule_map = _get_build_rule_map()
    output_rule_map = _get_output_rule_map()
    rule_output = {}
    for child_definition_path in definition_paths:
        full_child_definition_path = os.path.join(execution_context.dir_path, child_definition_path)
        child_execution_context = ExecutionContext(
            build_context=execution_context.build_context,
            dir_path=os.path.dirname(full_child_definition_path),
            output=rule_output,
            enable_output_steps=execution_context.enable_output_steps
        )
        build_config = _read_build_config(full_child_definition_path)
        for build_step_config in build_config['steps']:
            output_rule_name, output_rule_args = _parse_build_step_config(**build_step_config)
            build_rule_function = build_rule_map[output_rule_name]

            child_rule_output = build_rule_function(child_execution_context, **output_rule_args)

            if child_rule_output:
                utils.recursive_merge_dicts(rule_output, child_rule_output)

        if execution_context.enable_output_steps:
            for output_step_config in build_config.get('output_steps', []):
                output_rule_name, output_rule_args = _parse_build_step_config(**output_step_config)
                output_rule_function = output_rule_map[output_rule_name]

                output_rule_function(child_execution_context, **output_rule_args)

    return rule_output

def _read_build_config(config_file_path):
    _, config_ext = os.path.splitext(config_file_path)
    with open(config_file_path) as config_file:
        if config_ext == '.json':
            return json.load(config_file)
        elif config_ext in ('.yml', '.yaml'):
            return yaml.load(config_file)
        else:
            raise ValueError("Invalid build config file extension: {0}".format(config_ext))

def _parse_build_step_config(rule, args={}):
    return rule, args

def _get_build_rule_map():
    build_rules = [
        execute_child_builds,
        build_docker_image.build_docker_image,
        build_generic_artifact.build_generic_artifact,
        build_maven_artifact.build_maven_artifact,
        build_npm_package.build_npm_package,
        create_tar_archive.create_tar_archive,
        create_elastic_beanstalk_docker_app_bundle.create_elastic_beanstalk_docker_app_bundle,
        get_image_tag_from_config.get_image_tag_from_config,
        get_passthrough_config.get_passthrough_config,
        write_output_to_hcl.write_output_to_hcl,
        write_output_to_json.write_output_to_json,
        write_output_to_cfn_parameters.write_output_to_cfn_parameters
    ]

    build_rule_map = {}
    for build_rule in build_rules:
        build_rule_map[build_rule.__name__] = build_rule

    return build_rule_map

def _get_output_rule_map():
    output_rules = [
        write_output_to_hcl.write_output_to_hcl,
        write_output_to_json.write_output_to_json,
        write_output_to_cfn_parameters.write_output_to_cfn_parameters
    ]

    output_rule_map = {}
    for output_rule in output_rules:
        output_rule_map[output_rule.__name__] = output_rule

    return output_rule_map

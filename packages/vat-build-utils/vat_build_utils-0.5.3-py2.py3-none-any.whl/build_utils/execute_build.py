from build_utils.build_context import BuildContext
from build_utils.execution_context import ExecutionContext
from build_utils.rules.execute_child_builds import execute_child_builds

def execute_build(build_context_config, build_definition_path, enable_output_steps=True):
    execution_context = ExecutionContext(
        build_context=BuildContext(build_context_config),
        dir_path='.',
        output={},
        enable_output_steps=enable_output_steps
    )
    return execute_child_builds(execution_context, definition_paths=[build_definition_path])

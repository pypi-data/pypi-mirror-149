from collections import namedtuple

ExecutionContext = namedtuple('ExecutionContext', ['build_context', 'output', 'dir_path', 'enable_output_steps'])

import json
import logging
import os

from build_utils import utils

logger = logging.getLogger(__name__)

def write_output_to_cfn_parameters(execution_context, path):
    output_file_path = os.path.join(execution_context.dir_path, path)
    with open(output_file_path, mode='w') as parameter_file:
        for output_key, output_value in execution_context.output.items():
            if output_key == 'images':
                # Write images
                for image_id, image_uri in output_value.items():
                    parameter_file.write("{0}Image={1}\n".format(image_id, image_uri))

            elif output_key == 'files':
                # Write files
                for artifact_id, artifact_location in output_value.items():
                    for key, value in artifact_location.items():
                        if key == 'type':
                            continue
                        parameter_file.write("{0}File{1}={2}\n".format(
                            artifact_id, key.capitalize(), value))

            else:
                logger.warn("Output values with key '%s' currently not supported", output_key)

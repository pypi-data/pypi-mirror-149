import os

from vat_utils.config import create_config_client_v2

def get_image_tag_from_config(execution_context, image_name, config_source):
    """
    Get image tag from a config source.
    """
    old_working_directory = os.getcwd()
    try:
        os.chdir(execution_context.dir_path)
        config = create_config_client_v2(config_source).get_root_json_value()
    finally:
        os.chdir(old_working_directory)
        
    image_registry = execution_context.build_context.get_image_registry()

    return {
        "images": {
            image_name: image_registry.get_full_image_tag(image_name, config["tag"])
        }
    }


from docker.errors import ImageNotFound

from build_utils import docker_utils

class LocalRegistry(object):
    def get_full_image_tag(self, name, tag):
        return "{0}:{1}".format(name, tag)

    def has_image(self, name, tag):
        docker_client = docker_utils.get_docker_client_from_env()

        try:
            docker_client.images.get("{0}:{1}".format(name, tag))
            return True
        except ImageNotFound:
            return False

    def push_image(self, name, tag):
        pass

    def pull_image(self, name, tag):
        return self.get_full_image_tag(name, tag)

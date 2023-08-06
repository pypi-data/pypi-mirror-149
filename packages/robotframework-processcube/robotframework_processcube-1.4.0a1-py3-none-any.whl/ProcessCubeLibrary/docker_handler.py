import docker
import time

from robot.api import logger


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class DockerHandler:

    IMAGE_NAME = '5minds/engine'

    def __init__(self, **kwargs):

        params = {
            'timeout': 120
        }

        self._client = docker.from_env(**params)
        self._name = kwargs.get(
            'container_name', 'robotframework_5minds-engine')
        self._auto_remove = str2bool(kwargs.get('auto_remove', True))
        self._image_name = kwargs.get('image_name', DockerHandler.IMAGE_NAME)

        self._delay = kwargs.get('delay', 5.0)

    def start(self):
        logger.console(f"Starting engine within a docker container '{self._image_name}' ...")

        args = {
            'detach': True,
            'publish_all_ports': True,
            'name': self._name,
            'auto_remove': self._auto_remove,
        }

        if self.find_container():
            if self._container.status == 'exited':
                self._container.restart()
        else:
            self._container = self._client.containers.run(
                self._image_name, **args)

        time.sleep(float(self._delay))

        container = self._client.containers.get(self._container.id)

        key = list(container.attrs['NetworkSettings']['Ports'].keys())[0]

        self._port = container.attrs['NetworkSettings']['Ports'][key][0]['HostPort']

        logger.console(f"Starting engine within a docker container '{self._image_name}' ... done")


    def get_engine_url(self):
        engine_url = f"http://localhost:{self._port}"

        return engine_url

    def find_container(self):
        containers = self._client.containers.list(
            all=True, filters={'name': self._name})

        if len(containers) > 0:
            self._container = containers[0]
            found = True
        else:
            found = False

        return found

    def shutown(self, prune=False):
        self._container.stop()

        if prune:
            self._client.containers.prune()

    def report(self):
        print(f"container id: {self._container.id}")
        print(f"container attr: {self._port}")


def main():
    handler = DockerHandler(auto_remove=False)

    handler.start()
    handler.report()
    handler.shutown()


if __name__ == '__main__':
    main()

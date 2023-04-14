import docker

client = docker.from_env()

container = client.containers.get('mysql')

logs = container.logs()
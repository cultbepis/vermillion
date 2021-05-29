from django.shortcuts import render
from docker import from_env as docker_client
from docker.errors import DockerException

def index(request):
    try:
        client = docker_client()
    except DockerException as e:
        context = {
            'error': str(e)
        }

        return render(request, 'vermillion/index.html', context, status=500)

    container_data = []
    for container in client.containers.list():
        datas = {
            'name': container.name,
            'status': container.status,
        }
        container_data.append(datas)

    context = {
        'container_data': container_data,
    }

    return render(request, 'vermillion/index.html', context)

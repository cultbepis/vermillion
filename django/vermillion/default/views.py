from django.shortcuts import render
import docker

def index(request):
    client = docker.from_env()
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

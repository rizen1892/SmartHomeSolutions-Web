from django.shortcuts import render
from django.shortcuts import redirect
from home.models import Configuration
from home.models import Movement
from home.models import get_recordings
from home.models import get_photos
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def recordings(request, recording=None):
    recordings = get_recordings()

    if recording is None and len(recordings) != 0:
        recording = recordings[0].name

    return render(request, 'recordings.html', {"recordings": recordings, "recording": recording})


def photos(request, photo=None, page=1):
    page = int(page)

    photos_all = get_photos()
    paginator = Paginator(photos_all, 100)

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    if photo is None and len(photos.object_list) != 0:
        photo = photos.object_list[0].name

    return render(request, 'photos.html', {"photos": photos, "photo": photo})


def movements(request, page=1):
    page = int(page)

    mov_all = Movement.objects.order_by('-time').all()
    paginator = Paginator(mov_all, 100)

    try:
        movements = paginator.page(page)
    except PageNotAnInteger:
        movements = paginator.page(1)
    except EmptyPage:
        movements = paginator.page(paginator.num_pages)

    return render(request, 'movements.html', {"movements": movements})


def stream(request):
    return render(request, 'stream.html')


def stream_data(request):
    from gevent import socket
    from time import sleep

    sleep(0.5)
    s = socket.create_connection(("127.0.0.1", 1234))
    sf = s.makefile()

    return StreamingHttpResponse(FileWrapper(sf), content_type='text/plain')


def get_config(request):
    return render(request, 'configuration.html', {"config": Configuration.objects.first()})


def restart_app(request):
    import subprocess
    import os
    import time

    current_path = os.path.abspath(__file__)
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

    stop_cmd = [os.path.join(base_path, "webcam.sh"), "stop", "app"]
    start_cmd = [os.path.join(base_path, "webcam.sh"), "start", "app"]

    subprocess.Popen(stop_cmd, cwd=base_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True).wait()
    time.sleep(2)
    subprocess.Popen(start_cmd, cwd=base_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    return redirect('home.views.get_config')


def restart_pi(request):
    import subprocess

    cmd = ["reboot"]
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    return redirect('home.views.get_config')


def shutdown_pi(request):
    import subprocess

    cmd = ["shutdown", "-h", "now"]
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    return redirect('home.views.get_config')
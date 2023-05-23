import flask as fl
import json
import time
import cv2

from queue import Queue
from ..utils import check_license, get_info

bp = fl.Blueprint(
    name="monitoring_routes", url_prefix="/monitoring", import_name=__name__
)

queue = Queue(maxsize=10)
camera = cv2.VideoCapture(1)


def gen_monitoring():
    # Read until video is completed
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if success:
            tag = "ENY-9C32" # Substituir pelo retorno da IA

            checked, vehicle = check_license(tag)
            if checked:
                queue.put(get_info(vehicle))
            else:
                queue.put({'status': 2})

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            break
        key = cv2.waitKey(20)


def gen_info():
    while True:
        if not queue.empty():
            info = queue.get()
        else:
            info = {'status': 0}

        # Yield the car data as a JSON string
        yield "data: " + json.dumps(info) + "\n\n"
        time.sleep(0.2)


@bp.route("/", methods=["GET"], strict_slashes=False)
def send_info():
    return fl.Response(gen_info(), mimetype="text/event-stream")


@bp.route("/video-stream", methods=["GET"], strict_slashes=False)
def send_video():
    return fl.Response(
        gen_monitoring(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

import flask as fl
import json
import time
import cv2
import datetime

from queue import Queue
from ..utils import check_license, get_info, open_serial_message

bp = fl.Blueprint(
    name="monitoring_routes", url_prefix="/monitoring", import_name=__name__
)

queue = Queue(maxsize=10)
camera = cv2.VideoCapture(0)
lastTag: str = None

delay = 10000

@fl.stream_with_context
def gen_monitoring():
    # Read until video is completed
    lastTag = None
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if success:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            break
        key = cv2.waitKey(20)


@fl.stream_with_context
def gen_info():
    global lastTag
    while True:
        if not queue.empty():
            info = queue.get()
            open_serial_message()
            start = datetime.datetime.now()
            while datetime.datetime.now() - start <= datetime.timedelta(seconds=10): 
                # Yield the car data as a JSON string
                yield "data: " + json.dumps(info) + "\n\n"
                time.sleep(0.2)
                lastTag = None
        else:
            info = {"status": 0}
            # Yield the car data as a JSON string
            yield "data: " + json.dumps(info) + "\n\n"
            time.sleep(0.2)


def enqueue_car(info: dict):
    global lastTag
    tag = info["carId"].upper()
    entry = info["time"]
    if tag != None and tag != lastTag:
        checked, vehicle = check_license(tag)
        if checked:
            data = get_info(vehicle, entry)
        else:
            data = {"status": 2, "entry": entry, "license": tag}
        lastTag = tag
    if queue.full():
        queue.get()
    queue.put(data)

    return data


@bp.route("/", methods=["GET"], strict_slashes=False)
def send_info():
    return fl.Response(gen_info(), mimetype="text/event-stream")


@bp.route("/", methods=["POST"], strict_slashes=False)
def receive_info():
    return enqueue_car(fl.request.get_json()), 201


@bp.route("/video-stream", methods=["GET"], strict_slashes=False)
def send_video():
    return fl.Response(
        gen_monitoring(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

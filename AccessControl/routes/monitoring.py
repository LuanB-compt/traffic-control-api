import flask as fl
import json
import time
import cv2

bp = fl.Blueprint(
    name="monitoring_routes", url_prefix="/monitoring", import_name=__name__
)
camera = cv2.VideoCapture(1)


def gen_frames():
    # Read until video is completed
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


def gen_info():
    car_id = 0
    while True:
        car_data = {
            "car_id": car_id,
            "make": "Example Make",
            "model": "Example Model",
            "color": "Example Color",
        }
        car_id += 1

        # Yield the car data as a JSON string
        yield json.dumps(car_data) + "\n"


@bp.route("/", methods=["GET"], strict_slashes=False)
def monitoring():
    def generate_events():
        while True:
            cars = [
                {"make": "Toyota", "model": "Camry", "year": 2020},
                {"make": "Honda", "model": "Civic", "year": 2021},
                {"make": "Ford", "model": "Mustang", "year": 2019},
            ]

            for car in cars:
                yield "data: " + "{}" + "\n\n"
                # yield 'data: ' + json.dumps(car) + '\n\n'
                time.sleep(1)  # Delay between each car event

    return fl.Response(generate_events(), mimetype="text/event-stream")


@bp.route("/video-stream", methods=["GET"], strict_slashes=False)
def send_video():
    return fl.Response(
        gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

from flask import Flask, Response
import picamera
import io

app = Flask(__name__)


@app.route("/")
def index():
    return "Camera Stream"


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 24
        self.stream = io.BytesIO()

    def get_frame(self):
        self.camera.capture(self.stream, "jpeg", use_video_port=True)
        self.stream.seek(0)
        frame = self.stream.read()
        self.stream.seek(0)
        self.stream.truncate()
        return frame


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

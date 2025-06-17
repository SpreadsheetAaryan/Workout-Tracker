import cv2 as cv
import threading

class Camera:
    def __init__(self):
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            raise ValueError("Camera not found")
        
        self.width = self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)

        self.camera.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        self.camera.set(cv.CAP_PROP_FPS, 30)
        self.camera.set(cv.CAP_PROP_BUFFERSIZE, 1)
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.ret = False
        self.frame = None
        self.lock = threading.Lock()
        
        self.thread = threading.Thread(target=self._capture_loop, args=())
        self.thread.daemon = True
        self.thread.start()

    def _capture_loop(self):
        while True:
            ret, frame = self.camera.read()
            if ret:
                with self.lock:
                    self.ret = ret
                    self.frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def get_frame(self):
        with self.lock:
            return self.ret, self.frame

    def __del__(self):
        self.camera.release()
import cv2
from multiprocessing import Process
import sys


def camera():
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        check, frame = video.read()
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


def camera2():
    video = cv2.VideoCapture(0)
    while True:
        check, frame = video.read()
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


# if __name__ == '__main__':
    # p1 = Process(target=camera())
    # p1.start()
    # p2 = Process(target=camera2())
    # p2.start()
    # p1.join()
    # p2.join()

camera()
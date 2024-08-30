from ultralytics import YOLO
from threading import Lock
import cv2



class YoloModel:
    _model = None
    _lock = Lock()
    _class_names = {
        0:'Zimmerpflanze', 
        1:'dungen', 
        2:'halb sonnig schattig', 
        3:'keine Sonne', 
        4:'mittel giesen', 
        5:'schattig', 
        6:'sonnig', 
        7:'viel giesen',
        8: 'wenig giesen'
    }

    @classmethod
    def _load_model(cls):
        with cls._lock:
            if cls._model is None:
                cls._model = YOLO("runs/detect/train7/weights/best.pt")

    @classmethod
    def prediction(cls, image):
        if cls._model is None:
            cls._load_model()
        result = cls._model(image)
        return result
    
    @classmethod
    def draw_predictions(cls, image, results):
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            labels = result.boxes.cls.cpu().numpy()

            for box, conf, label in zip(boxes, confs, labels):
                x1, y1, x2, y2 = map(int, box)
                label_name = cls._class_names.get(int(label), "Unknown")
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"{label_name}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image
    
    @classmethod
    def getObjekts(cls,results):
        detected_objects = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            labels = result.boxes.cls.cpu().numpy()

            for label in labels:
                class_id = int(label)
                class_name = cls._class_names.get(class_id, "Unknown")
                detected_objects.append(class_name)
        return detected_objects


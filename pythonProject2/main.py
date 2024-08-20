from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a custom model

#Predict with the model
model.train(data=r'C:\Users\Marc\Desktop\pythonProject2\test\data.yaml', epochs=100, imgsz=640)

model = YOLO("runs\\detect\\train7\\weights\\best.pt")


result=model("0_big.jpg")
result=model("0_big.jpg")

from ultralytics import YOLO

def study():
  dataset_path = "data.yaml"
  model = YOLO("yolo11n.pt")
  model.train(data=dataset_path, epochs=150, batch=16, imgsz=640)


def testCase():
  model = YOLO("runs/detect/train/weights/best.pt")
  result = model("DataSet/train/images/2_png.rf.7502d3472d76229b017d73eee6c5105a.jpg", conf=0.1)
  result[0].show()


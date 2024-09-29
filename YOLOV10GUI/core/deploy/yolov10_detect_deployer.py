import torch

from ultralytics import YOLOv10

class YOLOv10Deployer:
    def __init__(self, weights_path: str, model_yaml: str, conf: float = 0.3,imgsz=512):
        self.weights_path = weights_path
        self.model_yaml = model_yaml
        self.conf = conf
        self.imgsz=imgsz
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = YOLOv10(model_yaml).load(weights_path)
    def predict(self,img):
        # 进行预测
        results = self.model.predict(
            source=img,
            conf=self.conf,
            imgsz=self.imgsz,
            device=self.device
        )
        # print(results)
        results=results[0]
        confidences = results.boxes.conf
        classes = results.boxes.cls
        boxes = results.boxes.xyxy  # xyxy format: [x1, y1, x2, y2]
        names = results.names

        # 组装预测结果
        detections = []
        for i in range(len(confidences)):
            class_id = int(classes[i])  # 获取类别索引
            detection = {
                "class": names[class_id],  # 获取类名
                "class_id": class_id,  # 类别号
                "conf": confidences[i].item(),  # 置信度
                "box": {
                    "x1": boxes[i][0].item(),
                    "y1": boxes[i][1].item(),
                    "x2": boxes[i][2].item(),
                    "y2": boxes[i][3].item()
                }
            }
            detections.append(detection)
        return detections








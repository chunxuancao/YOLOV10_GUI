from fastapi import UploadFile

from YOLOV10GUI.core.deploy.yolov10_detect_deployer import YOLOv10Deployer
import os
from YOLOV10GUI.core.deploy.utils import GetSlices,convert_yolo_to_geo


def geo_yolo_detect(tif_file, cache_path: str=r"E:\System_settings\Project\YOLOV10模型开发GUI训练\cache", tile_size: int = 512, stride: int = 512):
    # 获取当前文件的绝对路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 定义相对路径
    weights_path = os.path.join(base_dir, 'model_param\\yolov10_detect\\best.pt')
    model_yaml = os.path.join(base_dir, 'model_param\\yolov10_detect\\yolov10m.yaml')
    # 创建 YOLOv10Deployer 实例
    yolo = YOLOv10Deployer(weights_path=weights_path, model_yaml=model_yaml)
    result = []
    # 传入cache以及遥感图像进行切片以及得到所有切片信息
    with GetSlices(tif_file,cache_path) as slices:
        for slice in slices:
            yolo_detect=yolo.predict(slice['file_name'])
            detects=convert_yolo_to_geo(slice,yolo_detect)
            for detect in detects:
                result.append(detect)  # 使用 tuple 以便存储在集合中
    return result



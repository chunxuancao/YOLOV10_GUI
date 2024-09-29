import zipfile
from io import BytesIO

from fastapi import APIRouter, File, UploadFile
import os
import json
from YOLOV10GUI.core.deploy.geoDetect import geo_yolo_detect

router = APIRouter()

UPLOAD_FOLDER = 'uploads/deploy'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# 指定保存文件的目录
SAVE_DIR = 'uploads/deploy'  # 替换为实际路径
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/upload")
async def upload_blob(file: UploadFile = File(...)):
    # 读取文件并解压
    with zipfile.ZipFile(BytesIO(await file.read())) as zip_file:
        zip_file.extractall(SAVE_DIR)
    return {"message": "File uploaded and extracted"}


@router.post("/upload_data")
async def upload_data(file: UploadFile = File(...)):
    print(file)
    print(type(file))
    tif_file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(tif_file_location, "wb") as f:
        f.write(await file.read())
    result=geo_yolo_detect(tif_file_location)
    prediction_result = {
        "status": "success",
        "prediction_result": json.dumps(result)
    }
    print(prediction_result)
    return prediction_result

@router.post("/predict")
async def predict():
    # 在这里添加预测的逻辑
    # 假设返回一些示例数据
    tif_path=r'E:\System_settings\Project\YOLOV10模型开发GUI训练\YOLOV10GUI\uploads\deploy\plane.tif'
    result=geo_yolo_detect(tif_path)
    prediction_result = {
        "status": "success",
        "prediction_result": json.dumps(result)
    }
    print(prediction_result)
    return prediction_result
def predict1(tif_path):
    # 在这里添加预测的逻辑
    result=geo_yolo_detect(tif_path)
    prediction_result = {
        "status": "success",
        "prediction_result": json.dumps(result)
    }
    return prediction_result
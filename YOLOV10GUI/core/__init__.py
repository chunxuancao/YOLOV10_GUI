import os
import torch
from YOLOV10GUI.core.ultralytics import YOLOv10
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import uvicorn

def get_data_yaml(yaml):
    return yaml

def get_model_yaml(yaml):
    return yaml

def get_detect_train(folder,name,data_yaml, model_yaml,hyp_yaml,epochs= 100,imgsz= 512,save_period=20):
    weights_path="yolov10m.pt"
    model = YOLOv10(model_yaml).load(weights_path)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # 开始训练
    model.train(
        data=data_yaml,  # 数据集配置文件
        epochs=epochs,  # 训练的轮数
        imgsz=imgsz,  # 图像尺寸
        device=device,  # 设备（CPU 或 GPU）
        resume=True,  # 从上次中断位置恢复训练
        project='runs/train',  # TensorBoard 日志目录
        name='plane',  # 实验名称，用于日志子目录
        save_period=save_period  # 每多少轮保存一次模型检查点
    )
    model.save(os.path.join(folder,name))  # 保存训练后的模型到指定路径
    model.export(format="onnx")




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
    # ��ʼѵ��
    model.train(
        data=data_yaml,  # ���ݼ������ļ�
        epochs=epochs,  # ѵ��������
        imgsz=imgsz,  # ͼ��ߴ�
        device=device,  # �豸��CPU �� GPU��
        resume=True,  # ���ϴ��ж�λ�ûָ�ѵ��
        project='runs/train',  # TensorBoard ��־Ŀ¼
        name='plane',  # ʵ�����ƣ�������־��Ŀ¼
        save_period=save_period  # ÿ�����ֱ���һ��ģ�ͼ���
    )
    model.save(os.path.join(folder,name))  # ����ѵ�����ģ�͵�ָ��·��
    model.export(format="onnx")




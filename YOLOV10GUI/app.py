from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from control import control_trainer, control_deploy
import os

app = FastAPI()

# 设置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 提供静态文件
app.mount("/YOLOV10GUI/templates/static", StaticFiles(directory=r"E:\System_settings\Project\YOLOV10模型开发GUI训练\YOLOV10GUI\templates\static"), name="static")

# 包含路由
app.include_router(control_trainer, prefix="/train", tags=["train"])
app.include_router(control_deploy, prefix="/deploy", tags=["deploy"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


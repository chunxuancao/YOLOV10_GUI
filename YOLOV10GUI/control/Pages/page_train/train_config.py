# 提交训练配置
from YOLOV10GUI.control.Pages.page_train.model_config import router, app
from ultralytics.nn import BaseModel


class TrainConfig(BaseModel):
    evaluation_choice: str
    loss_function: str
    gpu_choice: str
    learning_rate: float
    learning_rate_strategy: str
    optimizer: str

@router.post("/configure-training")
async def configure_training(train_config: TrainConfig):
    # 返回接收到的训练配置
    return {"message": "Training configured successfully", "train_config": train_config}

app.include_router(router)

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List

app = FastAPI()
router = APIRouter()

# 返回模型列表
@router.get("/models", response_model=List[str])
async def get_models():
    # 示例返回可用的模型名称列表
    return ["Model A", "Model B", "Model C"]

# 提交模型配置
class ModelConfig(BaseModel):
    model_name: str
    description: str
    selected_model: str

@router.post("/configure-model")
async def configure_model(config: ModelConfig):
    # 返回接收到的配置
    return {"message": "Model configured successfully", "config": config}

app.include_router(router)

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List

app = FastAPI()
router = APIRouter()

# ����ģ���б�
@router.get("/models", response_model=List[str])
async def get_models():
    # ʾ�����ؿ��õ�ģ�������б�
    return ["Model A", "Model B", "Model C"]

# �ύģ������
class ModelConfig(BaseModel):
    model_name: str
    description: str
    selected_model: str

@router.post("/configure-model")
async def configure_model(config: ModelConfig):
    # ���ؽ��յ�������
    return {"message": "Model configured successfully", "config": config}

app.include_router(router)

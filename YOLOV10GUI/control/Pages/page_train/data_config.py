# 返回样本集列表
from YOLOV10GUI.control.Pages.page_train.model_config import router
from ultralytics.nn import BaseModel


@router.get("/datasets", response_model=List[str])
async def get_datasets():
    # 示例返回可用的样本集名称列表
    return ["Dataset A", "Dataset B", "Dataset C"]

# 提交样本配置
class SampleConfig(BaseModel):
    selected_dataset: str
    preprocessing_params: dict

@router.post("/configure-sample")
async def configure_sample(sample_config: SampleConfig):
    # 返回接收到的样本配置
    return {"message": "Sample configured successfully", "sample_config": sample_config}

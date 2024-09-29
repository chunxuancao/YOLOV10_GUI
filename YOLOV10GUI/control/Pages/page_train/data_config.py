# �����������б�
from YOLOV10GUI.control.Pages.page_train.model_config import router
from ultralytics.nn import BaseModel


@router.get("/datasets", response_model=List[str])
async def get_datasets():
    # ʾ�����ؿ��õ������������б�
    return ["Dataset A", "Dataset B", "Dataset C"]

# �ύ��������
class SampleConfig(BaseModel):
    selected_dataset: str
    preprocessing_params: dict

@router.post("/configure-sample")
async def configure_sample(sample_config: SampleConfig):
    # ���ؽ��յ�����������
    return {"message": "Sample configured successfully", "sample_config": sample_config}

from ultralytics import YOLOv10,YOLO,YOLOWorld


class ModelSelect(object):
    def __init__(self):
        # ģ���б�
        self.models = {'Detect':[YOLOv10, YOLO, YOLOWorld]}

    def select_model(self, task,id, data, model_cfg,hyp_cfg):
        # ��֤ģ������
        model=self.models[task][id](
            data=data,
            cfg=model_cfg
        )
        result=model.train(
            cfg=hyp_cfg
        )

        model.trainer
        return result



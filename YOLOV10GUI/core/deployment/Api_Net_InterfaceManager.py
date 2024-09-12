# �ӿڹ�����
# ����ģ�����������ӿڣ�����ӿ��������Ӧ��
from typing import Dict, Any
import yaml
from fastapi import FastAPI, HTTPException
from Deployer import ModelDeployer


class ModelInterface:
    def __init__(self, model_config_path: str):
        self.deployer = ModelDeployer(config_path=model_config_path)

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        �����������ݲ�����ģ��������
        """
        try:
            return self.deployer.deploy(input_data)
        except Exception as e:
            return {"error": str(e)}





class InterfaceManager:
    def __init__(self, interface_config_path: str):
        self.interface_config_path = interface_config_path
        self.app = FastAPI()
        self.model_interface = None
        self.load_config()

    def load_config(self):
        """
        �������ļ����ؽӿ����ã���ʼ���ӿ�
        """
        with open(self.interface_config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        model_config_path = self.config.get('model_config_path')
        if not model_config_path:
            raise ValueError("Model configuration path is missing in the interface configuration")

        self.model_interface = ModelInterface(model_config_path=model_config_path)
        self.setup_routes()

    def setup_routes(self):
        """
        ���������ļ����� FastAPI ·��
        """
        routes = self.config.get('routes', [])

        for route in routes:
            endpoint = route.get('endpoint')
            methods = route.get('methods', ['POST'])

            if not endpoint:
                raise ValueError("Endpoint is missing in the route configuration")

            if 'POST' in methods:
                self.app.post(endpoint)(self.handle_request)

    async def handle_request(self, input_data: dict):
        """
        ���� HTTP ���󲢷���ģ��������
        """
        try:
            result = self.model_interface.predict(input_data)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def run(self, host='0.0.0.0', port=8000):
        """
        ���� FastAPI Ӧ��
        """
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

# ʹ��ʾ��
# manager = InterfaceManager(interface_config_path='interface_config.yaml')
# manager.run()


# 接口管理器
# 管理模型推理的网络接口，处理接口请求和响应。
from typing import Dict, Any
import yaml
from fastapi import FastAPI, HTTPException
from Deployer import ModelDeployer


class ModelInterface:
    def __init__(self, model_config_path: str):
        self.deployer = ModelDeployer(config_path=model_config_path)

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据并返回模型推理结果
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
        从配置文件加载接口配置，初始化接口
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
        根据配置文件设置 FastAPI 路由
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
        处理 HTTP 请求并返回模型推理结果
        """
        try:
            result = self.model_interface.predict(input_data)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def run(self, host='0.0.0.0', port=8000):
        """
        运行 FastAPI 应用
        """
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

# 使用示例
# manager = InterfaceManager(interface_config_path='interface_config.yaml')
# manager.run()


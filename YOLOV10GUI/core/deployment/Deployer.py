# 模型部署器
# 负责模型的部署过程，包括配置和启动部署服务。


# 主要要做的是把模型的功能给释放出来
# 对于输入数据
# 1.模型部署配置yaml
# 需要记载的是
#   模型的任务配置
#   模型的构造配置
#   数据预处理的配置
#   数据输出处理配置

# 2.根据配置去调用对应的模块
# 需要做的是
#   1.装载模型
#   2.装载数据预处理的类
#   3.装载数据后处理的类
#   4.将这些装载为模型部署类
import yaml
import importlib
class ModelDeployer:
    def __init__(self, config_path):
        self.config_path = config_path
        self.model = None
        self.preprocessor = None
        self.postprocessor = None
        self.load_config()

    def load_config(self):
        """
        从配置文件加载模型、预处理和后处理的配置
        """
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        # 装载模型
        self.load_model()

        # 装载数据预处理类
        self.load_preprocessor()

        # 装载数据后处理类
        self.load_postprocessor()

    def load_model(self):
        """
        根据配置装载模型
        """
        model_config = self.config.get('model')
        if not model_config:
            raise ValueError("Model configuration is missing in the config file")

        module_name = model_config.get('module')
        class_name = model_config.get('class')

        if not module_name or not class_name:
            raise ValueError("Model module or class name is missing in the configuration")

        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        self.model = model_class()

    def load_preprocessor(self):
        """
        根据配置装载数据预处理类
        """
        preprocessor_config = self.config.get('preprocessor')
        if not preprocessor_config:
            return

        module_name = preprocessor_config.get('module')
        class_name = preprocessor_config.get('class')

        if not module_name or not class_name:
            raise ValueError("Preprocessor module or class name is missing in the configuration")

        module = importlib.import_module(module_name)
        preprocessor_class = getattr(module, class_name)
        self.preprocessor = preprocessor_class()

    def load_postprocessor(self):
        """
        根据配置装载数据后处理类
        """
        postprocessor_config = self.config.get('postprocessor')
        if not postprocessor_config:
            return

        module_name = postprocessor_config.get('module')
        class_name = postprocessor_config.get('class')

        if not module_name or not class_name:
            raise ValueError("Postprocessor module or class name is missing in the configuration")

        module = importlib.import_module(module_name)
        postprocessor_class = getattr(module, class_name)
        self.postprocessor = postprocessor_class()

    def deploy(self, input_data):
        """
        使用装载的模型和处理器来处理输入数据并输出结果
        """
        if self.preprocessor:
            input_data = self.preprocessor.process(input_data)

        if self.model:
            model_output = self.model.predict(input_data)

        if self.postprocessor:
            model_output = self.postprocessor.process(model_output)

        return model_output
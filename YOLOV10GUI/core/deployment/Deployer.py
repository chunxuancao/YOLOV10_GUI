# ģ�Ͳ�����
# ����ģ�͵Ĳ�����̣��������ú������������


# ��ҪҪ�����ǰ�ģ�͵Ĺ��ܸ��ͷų���
# ������������
# 1.ģ�Ͳ�������yaml
# ��Ҫ���ص���
#   ģ�͵���������
#   ģ�͵Ĺ�������
#   ����Ԥ���������
#   ���������������

# 2.��������ȥ���ö�Ӧ��ģ��
# ��Ҫ������
#   1.װ��ģ��
#   2.װ������Ԥ�������
#   3.װ�����ݺ������
#   4.����Щװ��Ϊģ�Ͳ�����
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
        �������ļ�����ģ�͡�Ԥ����ͺ��������
        """
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        # װ��ģ��
        self.load_model()

        # װ������Ԥ������
        self.load_preprocessor()

        # װ�����ݺ�����
        self.load_postprocessor()

    def load_model(self):
        """
        ��������װ��ģ��
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
        ��������װ������Ԥ������
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
        ��������װ�����ݺ�����
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
        ʹ��װ�ص�ģ�ͺʹ������������������ݲ�������
        """
        if self.preprocessor:
            input_data = self.preprocessor.process(input_data)

        if self.model:
            model_output = self.model.predict(input_data)

        if self.postprocessor:
            model_output = self.postprocessor.process(model_output)

        return model_output
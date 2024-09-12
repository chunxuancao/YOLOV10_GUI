import os

# 项目目录结构定义
project_structure = {
    "YOLOV10_GUI": {
        "config": [
            ("config_manager.py", "# 超参数配置管理器\n\n# 负责超参数配置的管理，包括读取和保存配置文件。\n"),
            ("yaml_loader.py", "# YAML 配置文件加载器\n\n# 用于加载和解析 YAML 配置文件。\n"),
            ("config_example.yaml", "# 示例配置文件\n\n# 提供超参数和模块设置的示例。\n")
        ],
        "core": [
            ("__init__.py", "# 核心模块初始化文件\n\n# 用于将 core 目录标记为一个包。\n"),
            ("model_manager.py", "# 模型管理器\n\n# 处理模型的保存、加载和管理功能。\n"),
            ("module_manager.py", "# 模块管理器\n\n# 负责加载和协调核心训练和数据处理模块。\n"),
            ("extension_module_manager.py", "# 扩展模块管理器\n\n# 支持加载和管理扩展功能的模块。\n"),
            ("data_manager.py", "# 数据处理模块管理器\n\n# 处理数据的预处理和加载功能。\n"),
            ("extension_data_manager.py", "# 扩展数据处理模块管理器\n\n# 支持自定义和扩展数据处理的功能。\n")
        ],
        "gui": [
            ("__init__.py", "# GUI 初始化文件\n\n# 用于将 gui 目录标记为一个包。\n"),
            ("main_window.py", "# 主窗口\n\n# 提供 GUI 的主要界面。\n"),
            ("config_window.py", "# 配置管理窗口\n\n# 允许用户设置超参数和模块配置。\n"),
            ("training_window.py", "# 训练窗口\n\n# 显示训练过程并提供控制选项。\n"),
            ("deployment_window.py", "# 部署窗口\n\n# 管理模型的部署设置和启动。\n"),
            ("utils.py", "# GUI 辅助功能\n\n# 包括常见的 GUI 工具和组件。\n")
        ],
        "training": [
            ("__init__.py", "# 训练模块初始化文件\n\n# 用于将 training 目录标记为一个包。\n"),
            ("train.py", "# 模型训练器\n\n# 负责模型训练的主要逻辑，包括训练循环和优化。\n"),
            ("evaluator.py", "# 模型评估器\n\n# 提供模型评估功能，包括计算损失和准确度。\n")
        ],
        "deployment": [
            ("__init__.py", "# 部署模块初始化文件\n\n# 用于将 deployment 目录标记为一个包。\n"),
            ("Deployer.py", "# 模型部署器\n\n# 负责模型的部署过程，包括配置和启动部署服务。\n"),
            ("Api_Net_InterfaceManager.py", "# 接口管理器\n\n# 管理模型推理的网络接口，处理接口请求和响应。\n")
        ],
        "utils": [
            ("__init__.py", "# 工具模块初始化文件\n\n# 用于将 utils 目录标记为一个包。\n"),
            ("file_utils.py", "# 文件操作工具\n\n# 提供文件操作功能，包括读取、写入和删除文件。\n"),
            ("visualization_utils.py", "# 可视化工具\n\n# 提供训练和评估结果的可视化功能。\n")
        ],
        "tests": [
            ("__init__.py", "# 测试模块初始化文件\n\n# 用于将 tests 目录标记为一个包。\n"),
            ("test_trainer.py", "# 模型训练器单元测试\n\n# 对模型训练器进行单元测试，确保其功能正确。\n"),
            ("test_deployer.py", "# 模型部署器单元测试\n\n# 对模型部署器进行单元测试，验证其部署能力。\n"),
            ("test_gui.py", "# GUI 单元测试\n\n# 对 GUI 进行单元测试，确保界面和交互功能正常。\n")
        ],
        "README.md": "# 项目说明文件\n\n# 介绍项目的背景、功能和使用方法。\n",
        "requirements.txt": "# Python 依赖包\n\n# 列出项目所需的 Python 依赖包。\n",
        "main.py": "# 主程序入口\n\n# 启动 GUI 并执行主逻辑。\n"
    }
}

def create_files_and_directories(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            if not os.path.exists(path):
                os.makedirs(path)
            create_files_and_directories(path, content)
        elif isinstance(content, list):
            if not os.path.exists(path):
                os.makedirs(path)
            for file_name, file_content in content:
                file_path = os.path.join(path, file_name)
                with open(file_path, 'w') as file:
                    file.write(file_content)
        elif content is None:
            with open(path, 'w') as file:
                file.write(content)

# 根目录
base_path = "."
create_files_and_directories(base_path, project_structure)

print("项目结构和文件已成功创建，并包含了注释内容！")

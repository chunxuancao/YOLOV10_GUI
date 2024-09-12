import os

# 定义目录结构
directories = [
    'config',
    'interface_manager',
    'module_manager',
    'utils',
    'gui',
    'tests'
]

# 定义文件结构
files = {
    'config': [
        '__init__.py',
        'config.py',
        'settings.py',
        'config_manager.py'
    ],
    'interface_manager': [
        '__init__.py',
        'base_interface.py',
        'interface_manager.py'
    ],
    'module_manager': [
        '__init__.py',
        'module_base.py',
        'module_manager.py',
        'module1.py',
        'module2.py'
    ],
    'utils': [
        '__init__.py',
        'helper_functions.py',
        'logger.py',
        'validation.py'
    ],
    'gui': [
        '__init__.py',
        'main_window.py',
        'dialogs.py',
        'widgets.py',
        'layout.py',
        'config_manager_gui.py'
    ],
    'tests': [
        '__init__.py',
        'test_config.py',
        'test_interface_manager.py',
        'test_module_manager.py',
        'test_utils.py',
        'test_gui.py',
        'test_config_manager.py'
    ]
}

# 创建目录和文件
def create_project_structure(base_dir):
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file_name in files.get(directory, []):
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'w') as file:
                # 创建空文件或写入初始内容
                if file_name.endswith('.py'):
                    file.write(f"# {file_name} - This file is generated automatically.\n")

# 主程序
if __name__ == "__main__":
    base_directory = os.getcwd()  # 使用当前工作目录
    create_project_structure(base_directory)
    print("Project structure created successfully.")

import sys
from cx_Freeze import setup, Executable
import os

# Функция для безопасного добавления файлов/папок
def include_folder(folder_path, target_name=None):
    """
    Рекурсивно включает все файлы из папки
    """
    if target_name is None:
        target_name = folder_path

    result = []
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                src_path = os.path.join(root, file)
                # Создаем относительный путь для назначения
                rel_path = os.path.relpath(root, folder_path)
                if rel_path == '.':
                    dest_path = target_name
                else:
                    dest_path = os.path.join(target_name, rel_path)
                result.append((src_path, dest_path))
    else:
        print(f"Warning: Folder {folder_path} does not exist")

    return result


# Функция для безопасного добавления файлов/папок
def safe_include_files(file_list):
    result = []
    for item in file_list:
        if isinstance(item, tuple):
            src, dest = item
            if os.path.exists(src):
                result.append((src, dest))
            else:
                print(f"Warning: {src} does not exist, skipping")
        else:
            if os.path.exists(item):
                # Для папок используем рекурсивное включение
                result.extend(include_folder(item, item))
            else:
                print(f"Warning: {item} does not exist, skipping")
    return result

# Список файлов и папок для включения
include_items = [
    ('images2d', 'images2d'),
    ('assets', 'assets'),
    ('configs', 'configs'),
    ('saves', 'saves'),
    'config.prc'
]

# Попробуйте найти и добавить плагины Panda3D
try:
    import panda3d

    panda3d_path = os.path.dirname(panda3d.__file__)
    plugins_path = os.path.join(panda3d_path, 'plugins')
    if os.path.exists(plugins_path):
        include_items.extend(include_folder(plugins_path, 'plugins'))
    else:
        print("Warning: Panda3D plugins directory not found")

        # Ручное копирование плагинов если нужно
        plugins_src = input("Введите путь к папке plugins Panda3D вручную: ")
        if plugins_src and os.path.exists(plugins_src):
            include_items.extend(include_folder(plugins_src, 'plugins'))

except ImportError:
    print("Warning: Panda3D not installed or not found")

# Безопасное добавление файлов
include_files = safe_include_files(include_items)

# Отладочная информация
print("Included files:")
for i, (src, dest) in enumerate(include_files[:20]):  # Покажем первые 20 файлов
    print(f"  {i + 1}. {src} -> {dest}")
if len(include_files) > 20:
    print(f"  ... and {len(include_files) - 20} more files")

build_exe_options = {
    "packages": ["panda3d", "yaml", "chardet"],
    "include_files": include_files,
    "includes": ["unittest"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="StepDefence",
    version="1.0",
    description="StepDefence Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="assets/icon.ico")]
)
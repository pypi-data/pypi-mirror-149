import os


folder = os.path.dirname(os.path.abspath(__file__))
texturefolder = os.path.join(folder, 'textrues')  # textures文件夹路径
resfolder = os.path.join(folder, 'res')


def get_path(f: str):
    """Get resource file path in `res` directory."""
    return os.path.join(resfolder, f)

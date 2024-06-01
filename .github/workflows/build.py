from flask_frozen import freezer # 替換為你的Flask應用的入口模塊和freezer實例
from earthquake_project.app import app # 替換為你的Flask應用的入口模塊和freezer實例

if __name__ == '__main__':
    freezer.freeze()

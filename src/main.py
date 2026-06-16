"""
多角色聊天机器人 - 项目入口
启动 Flask Web 服务
"""

import sys
import os

# 将项目根目录加入 Python 路径，确保 src 模块可导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import create_app


def main():
    app = create_app()
    print("\n" + "=" * 50)
    print("  多角色聊天机器人 已启动")
    print("  请打开浏览器访问: http://127.0.0.1:5000")
    print("  按 Ctrl+C 退出程序")
    print("=" * 50 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()

# Python 语言程序设计 — 期末综合实验

## 基本信息

| 项目 | 内容 |
|------|------|
| **课程名称** | Python 语言程序设计 |
| **实验名称** | 多角色聊天机器人 |
| **学号** | 25251111253 |
| **姓名** | 袁鸣 |
| **提交日期** | 2026-06-16 |
| **开发环境** | Python 3.10+，Windows 10/11 |
| **第三方依赖** | Flask==3.0.0 |

## 实验目的与功能概述

### 实验目的

综合运用 Python Web 框架、数据库操作、前后端交互等知识，完成一个可运行的聊天机器人应用。

### 实现功能

1. 多角色切换：内置四种角色（理性分析师、创意伙伴、温暖倾听者、知识导师），用户可实时切换
2. 智能回复：支持接入 OpenAI 兼容 API；未配置 API 时使用本地规则生成回复，保证项目独立运行
3. 对话历史：SQLite 持久化存储，按角色分频道管理，支持清空
4. Web 界面：原生 HTML/CSS/JS，支持角色可视化切换与消息气泡展示

### 技术栈

Flask（后端）、SQLite（数据库）、原生 HTML/CSS/JS（前端）、Jinja2（模板）

## 项目目录说明

```
25251111253-袁鸣-期末综合实验/
├── src/
│   ├── main.py                 # 入口，启动 Flask 服务
│   ├── app.py                  # Flask 路由与 API
│   ├── chatbot.py              # 聊天引擎（意图识别 + 回复生成）
│   ├── config.py               # 角色定义、API 配置、回复模板
│   ├── database.py             # SQLite 数据库操作
│   └── templates/
│       └── index.html          # 前端聊天界面
├── output/                     # 日志与输出（可选）
├── requirements.txt            # Python 依赖
└── README.md                   # 本文件
```

### 核心文件说明

| 文件 | 功能 |
|------|------|
| `main.py` | 程序入口，启动 Flask 并输出访问地址 |
| `app.py` | 定义页面路由与 `/api/chat`、`/api/history`、`/api/clear`、`/api/roles` 四个接口 |
| `chatbot.py` | 回复生成引擎，优先调用 API，回退本地模拟 |
| `config.py` | 集中管理角色 Prompt、意图关键词、本地回复模板 |
| `database.py` | 封装 SQLite 的增删查操作 |
| `index.html` | 前端界面，包含角色选择面板与聊天区域 |

## 环境与运行教程

### 前置条件

Python 3.10 或以上，无需额外服务。

### 安装与运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动项目
python src/main.py

# 浏览器访问 http://127.0.0.1:5000
# 按 Ctrl+C 退出
```

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| `ModuleNotFoundError: No module named 'flask'` | `pip install -r requirements.txt` |
| 端口 5000 被占用 | 修改 `main.py` 中 `port` 参数 |
| 导入 src 模块失败 | 确保在项目根目录运行 |

### 可选：接入 AI API

编辑 `src/config.py`：

```python
OPENAI_API_KEY = "sk-xxx"
OPENAI_API_BASE = "https://api.openai.com/v1"
```

并执行 `pip install openai`。未配置时自动使用本地模拟，不影响运行。

## 测试结果

| 测试项 | 输入 | 结果 |
|--------|------|------|
| 基本对话 | "你好" | 四角色回复风格各异 |
| 角色切换 | 切换至"创意伙伴" | 回复风格从分析转向创意联想 |
| 情感回应 | "今天好累" | 分析师做问题拆解，倾听者做情感共情 |
| 历史记录 | 多轮对话后刷新 | 记录完整保留 |
| 清空历史 | 点击清空按钮 | 当前角色记录清空 |
| 无 API 运行 | 不配置 API Key | 本地模拟正常运行 |

## 缓存清理

```bash
# Windows
Remove-Item -Recurse -Force src/__pycache__
Remove-Item -Force chat_history.db

# macOS / Linux
rm -rf src/__pycache__
rm -f chat_history.db
```

## 难点与总结

1. 多角色风格差异化：通过"意图分类 + 独立模板库"双层机制，确保本地模拟状态下四个角色回复有明显差异
2. API 与本地双轨切换：采用懒加载与 try/except 容错，保证有无 API 均可正常运行
3. 前后端状态同步：前端通过 Fetch API 与后端交互，实现消息实时渲染与历史加载

## 原创声明

本项目独立完成，所有代码自主编写，无抄袭、无照搬开源项目。

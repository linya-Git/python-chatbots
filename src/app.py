"""
多角色聊天机器人 - Flask 应用
定义路由和 API 接口
"""

from flask import Flask, render_template, request, jsonify
from src.chatbot import ChatBot
from src.database import init_db, save_message, load_history, clear_history
from src.config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL


# 全局 API 配置（运行时可通过前端面板动态修改）
api_settings = {
    "api_key": OPENAI_API_KEY,
    "api_base": OPENAI_API_BASE,
    "model": OPENAI_MODEL,
}


def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__, template_folder="templates")
    bot = ChatBot(settings=api_settings)

    # 初始化数据库
    init_db()

    # ==================== 页面路由 ====================

    @app.route("/")
    def index():
        """聊天主页面"""
        return render_template("index.html", characters=bot.list_characters())

    # ==================== API 接口 ====================

    @app.route("/api/roles", methods=["GET"])
    def get_roles():
        """获取所有角色列表"""
        return jsonify({"status": "ok", "data": bot.list_characters()})

    @app.route("/api/chat", methods=["POST"])
    def chat():
        """发送消息并获取回复"""
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "请求数据为空"}), 400

        user_message = data.get("message", "").strip()
        character_id = data.get("character", "").strip()

        if not user_message:
            return jsonify({"status": "error", "message": "消息不能为空"}), 400
        if not character_id:
            return jsonify({"status": "error", "message": "请选择角色"}), 400

        character = bot.get_character(character_id)
        if not character:
            return jsonify({"status": "error", "message": "角色不存在"}), 400

        save_message("user", user_message, character_id)
        reply = bot.generate_reply(user_message, character_id)
        save_message("bot", reply, character_id)

        return jsonify({
            "status": "ok",
            "data": {
                "user_message": user_message,
                "reply": reply,
                "character": character["name"],
                "avatar": character["avatar"]
            }
        })

    @app.route("/api/history", methods=["GET"])
    def history():
        """获取对话历史"""
        character_id = request.args.get("character", "").strip() or None
        messages = load_history(character=character_id)
        return jsonify({"status": "ok", "data": messages})

    @app.route("/api/clear", methods=["POST"])
    def clear():
        """清空对话历史"""
        data = request.get_json() or {}
        character_id = data.get("character", "").strip() or None
        clear_history(character=character_id)
        return jsonify({"status": "ok", "message": "对话历史已清空"})

    @app.route("/api/settings", methods=["GET"])
    def get_settings():
        """获取当前 API 配置（Key 脱敏）"""
        masked_key = ""
        if api_settings["api_key"]:
            raw = api_settings["api_key"]
            masked_key = raw[:4] + "***" + raw[-4:] if len(raw) > 8 else "***"
        return jsonify({
            "status": "ok",
            "data": {
                "api_key": masked_key,
                "api_base": api_settings["api_base"],
                "model": api_settings["model"],
                "has_api": bool(api_settings["api_key"])
            }
        })

    @app.route("/api/settings", methods=["POST"])
    def update_settings():
        """更新 API 配置"""
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "数据为空"}), 400

        api_key = data.get("api_key", "").strip()
        if "***" in api_key and api_settings["api_key"]:
            api_key = api_settings["api_key"]

        api_settings["api_key"] = api_key
        api_settings["api_base"] = data.get("api_base", "").strip()
        api_settings["model"] = data.get("model", "gpt-3.5-turbo").strip()

        bot.update_settings(api_settings)
        return jsonify({"status": "ok", "message": "配置已更新"})

    return app

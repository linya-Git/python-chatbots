"""
多角色聊天机器人 - 聊天引擎
负责意图识别与回复生成（API 优先，本地模拟回退）
"""

import random
from src.config import CHARACTERS, OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL
from src.config import INTENT_KEYWORDS, LOCAL_REPLIES


class ChatBot:
    """聊天机器人引擎"""

    def __init__(self, settings=None):
        self.characters = {c["id"]: c for c in CHARACTERS}
        self._openai_client = None
        self._settings = settings or {}  # 动态 API 配置

    @property
    def openai_client(self):
        """懒加载 OpenAI 客户端（优先使用动态配置）"""
        api_key = self._settings.get("api_key") or OPENAI_API_KEY
        if self._openai_client is None and api_key:
            try:
                from openai import OpenAI
                kwargs = {"api_key": api_key}
                api_base = self._settings.get("api_base") or OPENAI_API_BASE
                if api_base:
                    kwargs["base_url"] = api_base
                self._openai_client = OpenAI(**kwargs)
            except ImportError:
                self._openai_client = False
            except Exception:
                self._openai_client = False
        return self._openai_client if self._openai_client else None

    def get_character(self, character_id):
        """获取角色信息"""
        return self.characters.get(character_id)

    def list_characters(self):
        """列出所有角色"""
        return [
            {"id": c["id"], "name": c["name"], "avatar": c["avatar"], "description": c["description"]}
            for c in CHARACTERS
        ]

    def generate_reply(self, user_message, character_id):
        """
        生成回复：优先使用 OpenAI API，不可用时使用本地智能模拟
        """
        character = self.get_character(character_id)
        if not character:
            return "抱歉，我似乎迷失了角色……请重新选择。"

        # 尝试使用 API
        api_reply = self._try_api_reply(user_message, character)
        if api_reply:
            return api_reply

        # 回退到本地模拟
        return self._local_reply(user_message, character)

    def update_settings(self, settings):
        """更新 API 配置并重置客户端"""
        self._settings = settings
        self._openai_client = None  # 重置客户端以使用新配置

    def _try_api_reply(self, user_message, character):
        """尝试通过 OpenAI API 生成回复"""
        client = self.openai_client
        if not client:
            return None
        model = self._settings.get("model") or OPENAI_MODEL
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": character["system_prompt"]},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return None

    def _local_reply(self, user_message, character):
        """本地智能模拟回复"""
        intent = self._classify_intent(user_message)
        replies_pool = LOCAL_REPLIES.get(character["id"], {}).get(intent, [])
        if not replies_pool:
            replies_pool = LOCAL_REPLIES.get(character["id"], {}).get("default", ["请继续。"])
        return random.choice(replies_pool)

    def _classify_intent(self, message):
        """基于关键词匹配识别用户意图"""
        message_lower = message.lower().strip()
        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in message_lower:
                    return intent
        return "default"

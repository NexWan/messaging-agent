from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from .claude import ClaudeAgent
import os
import logging
import markdown

class TelegramHandler:

    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.telegram_token = os.getenv("TELEGRAM_TOKEN", "TOKEN_HERE")
        self.claude_agent = ClaudeAgent()
        allowed_user_id = os.getenv("ALLOWED_USER_ID", "")
        self.allowed_user_id = int(allowed_user_id) if allowed_user_id else None

    def init_bot(self):
        app = ApplicationBuilder().token(self.telegram_token).build()
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        app.run_polling()

    async def handle_message(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):

        if not update.message:
            raise Exception("Something went wrong!")
        
        user_id = update.message.from_user.id if update.message.from_user else None
        self.logger.info("User ID %s", user_id)
        self.logger.info("Allowed user id: %s", self.allowed_user_id)
        if user_id != self.allowed_user_id:
            await update.message.reply_text("Sorry, you can't use this bot.")
            return

        user_message = update.message.text
        self.logger.info("Message received from telegram: %s", user_message)

        if not user_message:
            await update.message.reply_text("Something went wrong, please try again.")
            return

        agent_response = await self.claude_agent.run_agent(user_message) or ""
        self.logger.info("Sending back Claude message to user....")
        formated_message = self._format_html(agent_response)

        try:
            await update.message.reply_text(formated_message, parse_mode="HTML")
        except Exception:
            await update.message.reply_text(agent_response)


    def _format_html(self, message=""):
        return markdown.markdown(message, extensions=["fenced_code", "tables"])
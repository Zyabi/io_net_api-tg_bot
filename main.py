import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Завантаження змінних середовища
load_dotenv()

# Ініціалізація клієнта OpenAI
client = openai.OpenAI(
    api_key=os.getenv("IOINTELLIGENCE_API_KEY"),
    base_url="https://api.intelligence.io.solutions/api/v1/",
)


def remove_before_word(text, target_word):
    pos = text.find(target_word)

    if pos != -1:
        return text[pos + len(target_word):].strip()
    else:
        return text


async def handle_rozumakha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробляє повідомлення з командою !розумаха"""
    # Перевірка чи команда викликана в груповому чаті
    # if update.message.chat.type not in ["group", "supergroup"]:
    #     await update.message.reply_text("Ця команда працює тільки в групових чатах!")
    #     return

    # Отримання тексту після команди
    full_text = update.message.text
    print(full_text)
    if full_text.startswith("роз"):
        user_prompt = full_text.replace("роз", "", 1).strip()

    user_prompt = full_text.replace("розумаха", "", 1).strip()

    print(user_prompt)

    if not user_prompt:
        await update.message.reply_text("Напиши по людськи")
        return

    try:
        # Відправка "думаю..." повідомлення
        thinking_msg = await update.message.reply_text("🤔 Пу-пу-пу...")

        # Генерація відповіді від AI
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-0528",
            messages=[
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Відправка відповіді та видалення "думаю..."
        ai_response = response.choices[0].message.content
        print(ai_response)
        normalized_response = remove_before_word(ai_response, "</think>")
        await thinking_msg.delete()  # Видаляємо "думаю..."
        await update.message.reply_text(normalized_response)

    except Exception as e:
        await update.message.reply_text(f"Сталася помилка: {str(e)}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробляє помилки"""
    print(f"Update {update} caused error: {context.error}")
    if update.message:
        await update.message.reply_text("Сталася помилка при обробці запиту")


def main():
    """Запуск бота"""
    # Отримання токену
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Telegram токен не знайдено в .env файлі!")

    # Створення додатку
    app = Application.builder().token(TOKEN).build()

    # Реєстрація обробника для !розумаха
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^розумаха\b'), handle_rozumakha))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^роз\b'), handle_rozumakha))
    app.add_error_handler(error_handler)

    # Запуск бота
    print("Бот запущено...")
    app.run_polling()


if __name__ == "__main__":
    main()

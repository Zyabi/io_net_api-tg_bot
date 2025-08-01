# Rozumakha Telegram Bot

**Rozumakha** — це Telegram-бот, який інтегрується з AI-моделлю через API-платформу [Intelligence.io.solutions](https://api.intelligence.io.solutions/) і генерує відповіді на запити користувача. Бот активується командами `розумаха` або `роз`.

## 🔧 Вимоги

- Python 3.10+
- Аккаунт на [intelligence.io.solutions](https://api.intelligence.io.solutions/) з API-ключем
- Telegram Bot Token
- Файл `.env` з налаштуваннями

## 📦 Встановлення

1. Клонувати репозиторій:
   ```bash
   git clone <URL>
   cd rozumakha-bot
   ```

2. Встановити залежності:
   ```bash
   pip install -r requirements.txt
   ```

3. Створити `.env` файл у корені проєкту:
   ```dotenv
   TELEGRAM_BOT_TOKEN=your_telegram_token
   IOINTELLIGENCE_API_KEY=your_intelligence_api_key
   ```

## 🚀 Запуск

```bash
python main.py
```

Після запуску бот очікує на повідомлення, які починаються з `розумаха` або `роз`, обробляє запит, надсилає його до AI-моделі і повертає відповідь.

## ⚙️ Архітектура

- `handle_rozumakha`: основна функція, що обробляє текстові запити.
- `remove_before_word`: допоміжна функція для очищення тексту після AI-відповіді.
- `client.chat.completions.create`: запит до AI-моделі `deepseek-ai/DeepSeek-R1-0528`.
- `error_handler`: обробка помилок.
- `main`: ініціалізація Telegram-бота та запуск.

## 🧪 Приклад використання

```text
Користувач: розумаха чому небо синє?
Бот: Тому що молекули в атмосфері розсіюють короткохвильове світло більше, ніж довгохвильове.
```

## ⚠️ Примітки

- Команда працює як у приватних, так і групових чатах.
- AI-відповідь обрізається до вмісту після тегу `</think>`, якщо він присутній.
- Поточна модель: `deepseek-ai/DeepSeek-R1-0528` (можна змінити в коді).
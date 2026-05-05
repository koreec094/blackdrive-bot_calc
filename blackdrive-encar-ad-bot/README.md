# blackdrive-encar-ad-bot

Отдельный Telegram-бот для генерации объявлений по ссылке Encar.

## MVP
- `/start` с кнопками:
  - 📝 Создать объявление по Encar
  - 👨‍💼 Связаться с менеджером
- Прием Encar-ссылки, валидация и извлечение `carid`.
- Получение данных авто с Encar.
- Добавление фиксированных расходов `KOREA_EXPENSES_KRW` (по умолчанию `1_640_000`).
- Формирование объявления в Telegram-формате без Google Sheets и без API калькулятора.

## Переменные окружения
```env
BOT_TOKEN=<новый токен бота от BotFather>
MANAGER_TELEGRAM_URL=https://t.me/blackdriveauto1
KOREA_EXPENSES_KRW=1640000
ENCAR_REQUEST_TIMEOUT=15
```

Не используются:
- `CALCULATOR_API_URL`
- `CALCULATOR_API_TOKEN`
- `GOOGLE_SHEETS_ID`
- `GOOGLE_SERVICE_ACCOUNT_JSON`

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m bot.main
```

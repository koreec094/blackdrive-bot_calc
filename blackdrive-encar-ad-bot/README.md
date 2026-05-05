# blackdrive-encar-ad-bot

Отдельный Telegram-бот для генерации объявлений по ссылке Encar.

## MVP
- `/start` и отдельное меню.
- Прием Encar-ссылки, валидация и извлечение `carid`.
- Получение данных авто с Encar.
- Добавление фиксированных расходов `KOREA_EXPENSES_KRW`.
- Вызов внешнего расчетного слоя через `services/calculator_client.py`.
- Формирование объявления и выдача кнопок:
  - Создать еще одно объявление
  - Связаться с менеджером

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m bot.main
```

## Интеграция расчета
Google Sheets не используется: переменные `GOOGLE_SHEETS_ID` и `GOOGLE_SERVICE_ACCOUNT_JSON` не нужны.

Бот берет `BOT_TOKEN` из `.env` — здесь должен быть токен **нового** Telegram-бота, созданного через BotFather.

По умолчанию `calculator_client.py` ходит в `CALCULATOR_API_URL` (HTTP API), что позволяет переиспользовать существующую расчетную систему без дублирования формул.

Локальный калькулятор можно поднять на этом же сервере:

```bash
uvicorn calculator_api:app --host 127.0.0.1 --port 8000
```

Рекомендуемые переменные окружения:

```env
CALCULATOR_API_URL=http://127.0.0.1:8000/calculate
CALCULATOR_API_TOKEN=<INTERNAL_BEARER_TOKEN>
```

`CALCULATOR_API_TOKEN` — внутренний Bearer-токен для защиты API. Он не связан с Telegram и проверяется в заголовке:

```http
Authorization: Bearer <CALCULATOR_API_TOKEN>
```

Если API не настроен, бот вернет частичный расчет (цена + фиксированные расходы), а поля таможни/утиля останутся `требуется проверка`.

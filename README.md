# "Крестики-Нолики"

## Описание

Этот проект представляет собой Telegram-бота для игры в "Крестики-Нолики".
Бот позволяет двум игрокам по очереди делать ходы на игровом поле 3x3. Игра заканчивается, когда один из игроков выигрывает или когда все клетки заполнены, что приводит к ничьей.

## Установка

### Требования

- `Python 3.7` или выше
- Библиотеки:
  - `aiogram==3.*`
  - `python-dotenv`

### Установка зависимостей

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/HapppyEnd/tic_tac_toe
   cd tic_tac_toe
   ```

2. Установите необходимые библиотеки:

   ```bash
   pip install -r requirements.txt
   ```

### Настройка

1. Создайте файл `.env` в корневой директории проекта и добавьте ваш токен бота:

   ```
   BOT_TOKEN=ваш_токен_бота
   ```

   Чтобы получить токен, создайте нового бота через [BotFather](https://t.me/botfather) в Telegram.

## Использование

1. Запустите бота:

   ```bash
   python main.py
   ```

2. Откройте Telegram и найдите вашего бота, используя его имя пользователя.
3. Отправьте команду `/start`, чтобы начать игру.
4. Выберите "Начать новую игру" для начала новой партии или "Выход" для завершения работы с ботом.
5. Игроки по очереди делают ходы, нажимая на кнопки, соответствующие клеткам на игровом поле.
6. После окончания игры бот предложит начать новую игру или выйти.

## Функциональность

- Возможность начать новую игру или выйти из игры.
- Проверка на наличие победителя после каждого хода.
- Возможность сыграть в ничью.
- Интуитивно понятный интерфейс с кнопками для взаимодействия.

## Вклад

Если вы хотите внести вклад в проект, пожалуйста, создайте форк репозитория, внесите изменения и создайте pull request.

## Контакты
Если у вас есть вопросы или предложения, вы можете связаться с автором проекта:

- **Telegram**: [Happpy_13](https://t.me/Happpy_13)
- **GitHub**: [HapppyEnd](https://github.com/HapppyEnd)



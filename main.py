import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

games: dict[int, 'Game'] = {}


class Game:
    def __init__(self) -> None:
        """Initialize the game with an empty board and the first player."""
        self.board: list[list[str]] = [
            [' ' for _ in range(3)] for _ in range(3)]
        self.current_player: str = 'X'
        self.is_game_over: bool = False

    def check_winner(self) -> str | None:
        """Check for a winner.

        Returns:
            str | None: The symbol of the winner ('X' or 'O')
            if there is one, otherwise None.
        """
        lines = (
            self.board +  # rows
            # columns
            [[self.board[i][j] for i in range(3)] for j in range(3)] +
            [[self.board[i][i] for i in range(3)], [
                self.board[i][2 - i] for i in range(3)]]  # diagonals
        )
        for line in lines:
            if line[0] == line[1] == line[2] != ' ':
                return line[0]
        return None

    def make_move(self, x: int, y: int) -> str | None:
        """Make a move on the board.

        Args:
            x (int): The row index.
            y (int): The column index.

        Returns:
            str | None: The symbol of the winner, 'draw'
            in case of a draw, or None if the game continues.
        """
        if self.board[x][y] == ' ' and not self.is_game_over:
            self.board[x][y] = self.current_player
            winner = self.check_winner()

            if winner:
                self.is_game_over = True
                return winner
            elif all(cell != ' ' for row in self.board for cell in row):
                self.is_game_over = True
                return 'draw'
            else:
                self.current_player = ('O' if self.current_player == 'X'
                                       else 'X')
                return None
        return None

    def get_board_display(self) -> str:
        """Get a string representation of the board.

        Returns:
            str: The string representation of the board.
        """
        return '\n'.join([' | '.join(row) for row in self.board])


@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    """Handler for the /start command to begin the game.

    Args:
        message (types.Message): The message from the user.
    """
    chat_id = message.chat.id
    await send_welcome_message(chat_id)


async def send_welcome_message(chat_id: int) -> None:
    """Send a welcome message with buttons.

    Args:
        chat_id (int): The chat ID.
    """
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Начать новую игру', callback_data='start_game'),
         InlineKeyboardButton(text='Выход', callback_data='exit_game')]
    ])
    await bot.send_message(
        chat_id,
        'Добро пожаловать в игру Крестики-нолики! Выберите действие:',
        reply_markup=reply_markup)


@dp.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery) -> None:
    """Handler for callback queries from buttons.

    Args:
        callback_query (types.CallbackQuery): The callback query object.
    """
    chat_id = callback_query.message.chat.id
    data = callback_query.data

    if data == 'start_game':
        games[chat_id] = Game()
        logger.info(f'Game started for chat {chat_id}.')
        await send_board(chat_id)
    elif data == 'exit_game':
        await bot.send_message(chat_id, 'Спасибо за игру! До свидания!')
        logger.info(f'Game ended for chat {chat_id}.')
        games.pop(chat_id, None)
    elif data == 'restart':
        games[chat_id] = Game()  # Start a new game
        logger.info(f'New game started for chat {chat_id}.')
        await send_board(chat_id)
    else:
        if chat_id in games:
            x, y = map(int, data.split(','))
            game = games[chat_id]
            result = game.make_move(x, y)

            if result == 'draw':
                await end_game(chat_id, 'Ничья!\nХотите сыграть заново?')
            elif result:
                await end_game(
                    chat_id,
                    f'Игрок {result} выиграл!\nХотите сыграть заново?')
            else:
                await send_board(chat_id)
        else:
            await bot.send_message(
                chat_id, 'Пожалуйста, начните новую игру с помощью /start.')
            logger.warning(
                f'Attempt to act in a non-existent game for chat {chat_id}.')


async def send_board(chat_id: int) -> None:
    """Send the current state of the board to the player.

    Args:
        chat_id (int): The chat ID.
    """
    game = games[chat_id]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=game.board[i][j]
            if game.board[i][j] == ' '
            else game.board[i][j],
            callback_data=f'{i},{j}') for j in range(3)]
        for i in range(3)
    ])
    await bot.send_message(
        chat_id,
        f'Ход игрока {game.current_player}:',
        reply_markup=reply_markup)


async def end_game(chat_id: int, result: str) -> None:
    """End the game and send the result.

    Args:
        chat_id (int): The chat ID.
        result (str): The result of the game.
    """
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='restart'),
         InlineKeyboardButton(text='Нет', callback_data='exit')]
    ])
    await bot.send_message(chat_id, result, reply_markup=reply_markup)
    logger.info(f'Game ended for chat {chat_id}: {result}')
    del games[chat_id]


if __name__ == '__main__':
    async def main() -> None:
        """Main function to run the bot."""
        await dp.start_polling(bot)

    asyncio.run(main())

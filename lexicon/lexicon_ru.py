from collections.abc import Mapping

LEXICON_RU: Mapping[str, str] = {
    "mine": "💥",
    "marked": "🚩",
    "closed": ".",
    "opened": " ",
    "no_stat": "Вы еще не играли, чтобы сыграть, введите команду "
               "<code>/play</code>",
    "stat": "Ваша статистика 📊:\n\nПобед: <b>{wins}</b>\n\n"
            "Поражений: <b>{losses}</b>",
    "mines_num": "{mines_num}",
    "click": "🖱️ Текущий мод: Click",
    "mark": "🚩 Текущий мод: Flag",
    "game_mode": "Размер: {field_width}x{field_height}, мин: {number_of_mines}",
    "mines_marked": "{mines_marked}/{mines_total} мин помечено.",
    "cancel_menu_entry": "❌ Отмена",
    "cancel_message": "Очень жаль, если вы передумали, введите команду "
                    "<code>/play</code>, чтобы начать игру",
    "/play": "Выберите размер игрового поля:",
    "/start": "<b>Приветствую, это игра сапер</b>.\n\n"
              "Чтобы начать играть введите команду <code>/play</code>\n"
              "Чтобы вывести справку, введите команду <code>/help</code>",
    "/help": "<b>Правила игры</b>\n\n"
             "<i>Цель игры</i>: найти все мины. "
             "Правила как в классическом сапере.\n\n"
             "Чтобы пометить поле с миной, "
             "переключите <i>Текущий мод</i> "
             "на <code>flag</code> (кнопка внизу игрового поля). "
             "Для открытия поля переключите <i>Текущий мод</i> на "
             "<code>click</code>.\n\n",
    "lose_message": "К сожалению вы проиграли. Чтобы сыграть заново, "
                    "введите команду <code>/play</code>",
    "lose_notify": "BOOOM!!!💥💥💥",
    "win_message": "Поздравляю, вы нашли все мины. Чтобы сыграть заново, "
                   "введите команду <code>/play</code>",
    "unexpected_command": "Упс, неизвестная команда",
    "error": "Похоже, что-то пошло не так. Попробуйте начать новую игру",
}

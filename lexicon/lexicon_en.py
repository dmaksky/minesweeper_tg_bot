from collections.abc import Mapping

LEXICON_EN: Mapping[str, str] = {
    "mine": "💥",
    "marked": "🚩",
    "closed": ".",
    "opened": " ",
    "no_stat": "You didn't play yet. To play use command "
    "<code>/play</code>",
    "stat": "Your stat 📊:\n\nWins: <b>{wins}</b>\n\n"
    "Losses: <b>{losses}</b>",
    "mines_num": "{mines_num}",
    "click": "🖱️ Current mod: Click",
    "mark": "🚩 Current mod: Flag",
    "game_mode": "Size: {field_width}x{field_height}, mines: {number_of_mines}",
    "mines_marked": "{mines_total}/{mines_marked} mines marked.",
    "cancel_menu_entry": "❌ Cancel",
    "cancel_message": "It's a pity. To play use command " "<code>/play</code>",
    "/play": "Choose game field size :",
    "/start": "<b>Hello, this is tg version of minesweeper</b>.\n\n"
    "Start new game - <code>/play</code>\n"
    "Show help - <code>/help</code>",
    "/help": "<b>Game rules: </b>\n\n"
    "<i>Goal</i>: find all mines. "
    "Rules like in a classic minesweeper.\n\n"
    "To mark mine field, "
    "switch <i>Current mod</i> "
    "on <code>flag</code> (button on the bottom). "
    "To open mine switch <i>Current mod</i> on "
    "<code>click</code>.\n\n",
    "lose_message": "Your lose!!!, to play again "
    "use command <code>/play</code>",
    "lose_notify": "BOOOM!!!💥💥💥",
    "win_message": "Congratulations, you have found all mines.!"
    "Play again - <code>/play</code>",
    "unexpected_command": "Oops, unexpected command",
    "error": "It seems that something went wrong.Try starting a new game",
}

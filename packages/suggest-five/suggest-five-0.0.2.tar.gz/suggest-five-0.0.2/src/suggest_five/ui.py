import curses as standard_curses
from dataclasses import dataclass
from typing import cast

from suggest_five.guess_results import GuessResult, GuessResults


@dataclass
class KeyConfig:
    display_char: str
    guess_result: GuessResult


KEY_CONFIG = {
    "B": KeyConfig("⬛", GuessResult.INCORRECT),
    "G": KeyConfig("🟩", GuessResult.CORRECT),
    "Y": KeyConfig("🟨", GuessResult.MOVED),
}
RESULT_COLUMN = 7


class UserInterface:
    def __init__(self, curses=standard_curses):
        self.curses = curses

    def __enter__(self):
        self.screen = self.curses.initscr()
        self.curses.noecho()
        self.curses.cbreak()
        self.screen.keypad(True)
        self.screen.addstr(0, 0, "suggest_five")
        self.screen.addstr(1, 0, "------------")
        self.current_row = 3
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.curses.nocbreak()
        self.screen.keypad(False)
        self.curses.echo()
        self.curses.endwin()

    def display_guess(self, guess: str) -> None:
        self.screen.addstr(self.current_row, 0, f"{guess} [          ]")
        self.screen.move(self.current_row, RESULT_COLUMN)
        self.screen.refresh()

    def get_guess_results(self) -> GuessResults:
        guess_results: list[GuessResult] = []

        while True:
            key = self.screen.getkey().upper()

            if key == "\n" and len(guess_results) == 5:
                self.current_row += 1
                break
            elif (key_config := KEY_CONFIG.get(key)) and len(guess_results) < 5:
                self.screen.addstr(self.current_row, RESULT_COLUMN + len(guess_results) * 2, key_config.display_char)
                guess_results.append(key_config.guess_result)
                self.screen.move(self.current_row, RESULT_COLUMN + len(guess_results) * 2)
                self.screen.refresh()
            elif key == "KEY_BACKSPACE" and guess_results:
                guess_results.pop()
                self.screen.addstr(self.current_row, RESULT_COLUMN + len(guess_results) * 2, "  ")
                self.screen.move(self.current_row, RESULT_COLUMN + len(guess_results) * 2)
                self.screen.refresh()

        assert len(guess_results) == 5
        return GuessResults(
            cast(tuple[GuessResult, GuessResult, GuessResult, GuessResult, GuessResult], tuple(guess_results))
        )

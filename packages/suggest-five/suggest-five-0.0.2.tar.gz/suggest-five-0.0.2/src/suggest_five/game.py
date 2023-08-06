from collections import Counter
from typing import cast

from suggest_five.guess_results import GuessResult as GR
from suggest_five.guess_results import GuessResults


class Game:
    def __init__(self, answer: str):
        self.answer = answer

    def guess(self, guess: str) -> GuessResults:
        non_correct_chars = Counter(
            answer_char for index, answer_char in enumerate(self.answer) if answer_char != guess[index]
        )

        output = []

        for index, guess_char in enumerate(guess):
            if guess_char == self.answer[index]:
                output.append(GR.CORRECT)
            elif non_correct_chars.get(guess_char, 0) > 0:
                output.append(GR.MOVED)
                non_correct_chars[guess_char] -= 1
            else:
                output.append(GR.INCORRECT)

        assert len(output) == 5
        return GuessResults(cast(tuple[GR, GR, GR, GR, GR], tuple(output)))

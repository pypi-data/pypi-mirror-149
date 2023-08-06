from dataclasses import dataclass
from enum import Enum


class GuessResult(Enum):
    CORRECT = 0
    MOVED = 1
    INCORRECT = 2


@dataclass
class GuessResults:
    guess_results: tuple[GuessResult, GuessResult, GuessResult, GuessResult, GuessResult]

    def is_finished(self) -> bool:
        return all(guess_result == GuessResult.CORRECT for guess_result in self.guess_results)

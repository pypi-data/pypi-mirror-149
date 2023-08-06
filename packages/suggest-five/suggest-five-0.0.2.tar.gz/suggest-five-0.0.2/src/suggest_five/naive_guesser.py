from suggest_five.guess_results import GuessResults
from suggest_five.util import filter_word_list


class NaiveGuesser:
    def __init__(self, answers: list[str]):
        self.answers = answers

    def guess(self) -> str:
        return self.answers[0]

    def train(self, guess: str, guess_results: GuessResults) -> None:
        self.answers = filter_word_list(self.answers, guess, guess_results)

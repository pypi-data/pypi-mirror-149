from suggest_five.game import Game
from suggest_five.naive_guesser import NaiveGuesser


def benchmark_performance(answers: list[str]) -> None:
    total_num_guesses = 0
    num_failures = 0

    for answer in answers:
        num_guesses_required = _run_single_game(answers, answer)
        total_num_guesses += num_guesses_required

        if num_guesses_required > 6:
            num_failures += 1

    num_guesses_per_game = total_num_guesses / len(answers)
    failure_percentage = 100.0 * num_failures / len(answers)

    print(f"{num_guesses_per_game=:0.2f}")
    print(f"{failure_percentage=:0.1f}%")


def _run_single_game(answers: list[str], answer: str) -> int:
    game = Game(answer)
    guesser = NaiveGuesser(answers)
    num_guesses = 0

    while True:
        guess = guesser.guess()
        guess_results = game.guess(guess)
        guesser.train(guess, guess_results)
        num_guesses += 1

        if guess_results.is_finished():
            break

    return num_guesses

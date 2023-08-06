#!/usr/bin/env python3

from io import TextIOWrapper

from click import File, command, option

from suggest_five.benchmark_performance import benchmark_performance
from suggest_five.io import load_words_from_file
from suggest_five.naive_guesser import NaiveGuesser
from suggest_five.ui import UserInterface


@command()
@option("-a", "--answers-filename", type=File("r"))
def suggest_five(answers_filename: TextIOWrapper) -> None:
    answers = list(load_words_from_file(answers_filename))
    guesser = NaiveGuesser(answers)
    guess = guesser.guess()

    with UserInterface() as user_interface:
        user_interface.display_guess(guess)

        while not (guess_results := user_interface.get_guess_results()).is_finished():
            guesser.train(guess, guess_results)
            guess = guesser.guess()
            user_interface.display_guess(guess)


@command()
@option("-a", "--answers-filename", type=File("r"))
def suggest_five_performance(answers_filename: TextIOWrapper) -> None:
    answers = list(load_words_from_file(answers_filename))
    benchmark_performance(answers)

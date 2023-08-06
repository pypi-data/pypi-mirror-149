from collections import Counter

from suggest_five.guess_results import GuessResult, GuessResults


def filter_word_list(word_list: list[str], guess: str, guess_results: GuessResults) -> list[str]:
    return [word for word in word_list if matches(word, guess, guess_results)]


def matches(word: str, guess: str, guess_results: GuessResults) -> bool:
    return (
        _all_correct_characters_match(word, guess, guess_results)
        and _all_incorrect_characters_do_not_match(word, guess, guess_results)
        and _word_contains_correct_number_of_moved_characters(word, guess, guess_results)
        and _word_contains_no_incorrect_characters(word, guess, guess_results)
    )


def _all_correct_characters_match(word: str, guess: str, guess_results: GuessResults) -> bool:
    for index, guess_result in enumerate(guess_results.guess_results):
        if guess_result == GuessResult.CORRECT and word[index] != guess[index]:
            return False

    return True


def _all_incorrect_characters_do_not_match(word: str, guess: str, guess_results: GuessResults):
    return all(
        word[index] != guess[index]
        for index, guess_result in enumerate(guess_results.guess_results)
        if guess_result != GuessResult.CORRECT
    )


def _get_incorrect_characters(guess: str, guess_results: GuessResults) -> set[str]:
    return {
        guess[index]
        for index, guess_result in enumerate(guess_results.guess_results)
        if guess_result == GuessResult.INCORRECT
    }


def _get_moved_characters_count(guess: str, guess_results: GuessResults) -> Counter[str]:
    return Counter(
        guess[index]
        for index, guess_result in enumerate(guess_results.guess_results)
        if guess_result == GuessResult.MOVED
    )


def _get_word_non_correct_characters_count(word: str, guess_results: GuessResults) -> Counter[str]:
    return Counter(
        word[index]
        for index, guess_result in enumerate(guess_results.guess_results)
        if guess_result != GuessResult.CORRECT
    )


def _word_contains_correct_number_of_moved_characters(word: str, guess: str, guess_results: GuessResults) -> bool:
    guess_moved_characters_count = _get_moved_characters_count(guess, guess_results)
    word_non_correct_characters_count = _get_word_non_correct_characters_count(word, guess_results)

    return all(word_non_correct_characters_count[char] >= count for char, count in guess_moved_characters_count.items())


def _word_contains_no_incorrect_characters(word: str, guess: str, guess_results: GuessResults) -> bool:
    guess_moved_characters_count = _get_moved_characters_count(guess, guess_results)
    guess_incorrect_characters = _get_incorrect_characters(guess, guess_results)

    for index, char in enumerate(word):
        if guess_results.guess_results[index] != GuessResult.CORRECT:
            if char in guess_incorrect_characters and guess_moved_characters_count.get(char, 0) == 0:
                return False

            guess_moved_characters_count[char] -= 1

    return True

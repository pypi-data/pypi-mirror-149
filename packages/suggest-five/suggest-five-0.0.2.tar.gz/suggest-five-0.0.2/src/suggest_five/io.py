from io import TextIOWrapper
from typing import Iterable


def load_words_from_file(input_file: TextIOWrapper) -> Iterable[str]:
    for line in input_file:
        stripped = line.strip()

        if len(stripped) != 5:
            raise ValueError(f"The input contained a word {stripped} whose length was not 5")

        yield stripped.upper()

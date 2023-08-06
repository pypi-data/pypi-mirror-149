# suggest-five
Suggest answers for a popular five-letter word game. 

## Usage

`suggest-five` takes as an argument a text file which should contain all possible puzzle answers, one per line:

```bash
$ suggest-five -a answers.txt
```

The official word list may be downloaded from several locations. As an alternative, a list of five-letter words can be
generated using the python module [wordfreq](https://github.com/rspeer/wordfreq/).

Once loaded, the programme will suggest a series of words. After each word, you should let `suggest-five` know the
results from using that word by pressing **G** to denote a correct match, **Y** to denote a letter in the wrong position
and **B** to denote an incorrect letter.

## How it works

The current algorithm is still quite naïve. It uses the feedback from the game to filter its word list without doing
anything much smarter. For example, if you report that the letter X is ⬛, future suggestions will omit any words with
an X.

## Performance

Performance is measured using the original official word list. Across all words, the average number of attempts needed
to guess each word was 4.35 and the algorithm failed to guess the correct word in 6 attempts 2.5% of the time.
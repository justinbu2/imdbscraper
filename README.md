# imdbscraper
Generic scraper that takes in the IMDB ID of a movie and writes to a JSON file all movies that involve two or more of the same cast members of the given IMDB ID.


# Usage
First, install the Python 3 packages listed in `requirements.txt`.
```
./main.py -t TITLE
```
where TITLE is the IMDB ID of a movie, e.g. `tt1677720` for _Ready Player One_.


# Output
Output will be in `output/`. Files created there will have a filename of the form `TitleID-mutual-movies.json`. Movies will be ordered in descending order of number of mutual actors with the input movie. A sample output from _Ready Player One_ can be found [here](output/sample-rpo-mutual-movies.json).


# Implementation details
A folder named `cached-sites` will be created upon invoking the script. This will contain a cache of movies and actor HTMLs that have already been visited, so we wouldn't need to bomboard IMDB with requests.

If a movie does not exist in `cached-sites`, the scraper would fetch the HTML using the `requests` library. The HTML would then be parsed using the `bs4` library.

This web scraper implements multiprocessing. The parameter can be tuned in the `src/constants.py` file. The only section of the code that is parallelized is that which fetches all the movies for every cast member in the input movie. From my testing, a 3-4x speedup was observed with caching. The default is to use 4 parallel processes, but the optimal number may vary based on your computer's architecture.

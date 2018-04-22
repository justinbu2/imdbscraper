import os


# Number of parallel processes to run when fetching movies
NUM_PROCESSES = 4
IMDB_HOMEPAGE = "https://www.imdb.com"
SAMPLE_OUTPUT_DIR = os.path.realpath(
    "{0}/../output".format(os.path.dirname(os.path.realpath(__file__))))
CACHED_SITES_DIR = os.path.realpath(
    "{0}/../cached-sites".format(os.path.dirname(os.path.realpath(__file__))))

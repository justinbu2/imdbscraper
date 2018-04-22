#!/usr/bin/env python3

import argparse
import collections
import json
import multiprocessing as mp
import timeit

from src import cast, movies, constants


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Imdb title looker upper")
    parser.add_argument("-t", "--title", type=str, required=True,
                        metavar="TITLE", help="title code of starting movie")
    return parser.parse_args()


def get_mutual_movies(cast_data):
    # Parallelizable tasks:
    # 1. making the request to fetch the data from FS or HTTP
    # 2. parsing the data and extracting the actors from those movies
    pool = mp.Pool(processes=4)
    mutual_movies = collections.defaultdict(dict)
    cast_movies = pool.map(movies.get_movies, cast_data) # list of all movies each cast has been in
    for actor_data, actor_movies in zip(cast_data, cast_movies):
        for movie in actor_movies:
            movie_id = movie["id"]
            if movie_id not in mutual_movies:
                mutual_movies[movie_id]["name"] = movie["name"]
                mutual_movies[movie_id]["mutual_actors"] = []
            mutual_movies[movie_id]["mutual_actors"].append(actor_data["name"])
    return mutual_movies


def marshall_mutual_movies(mutual_movies, title_id):
    output_movies = []
    for movie_id, movie in mutual_movies.items():
        if movie_id == title_id or len(movie["mutual_actors"]) == 1:
            continue
        output_movies.append({
            "movie_name": movie["name"],
            "mutual_actors": movie["mutual_actors"]
        })
    # Order movies by descending number of mutual actor count
    output_movies = sorted(output_movies, key=lambda x: -len(x["mutual_actors"]))
    return output_movies

def main():
    args = parse_arguments()
    if args.title:
        title_id = args.title

    t1 = timeit.default_timer()
    cast_data = cast.get_cast(title_id)
    t2 = timeit.default_timer()
    print(f"Fetched cast for IMDB title id {title_id} in {(t2 - t1):.2f}s.")
    mutual_movies = get_mutual_movies(cast_data)
    t3 = timeit.default_timer()
    print(f"Fetched all cast-movie information in {(t3 - t2):.2f}s.")

    output_movies = marshall_mutual_movies(mutual_movies, title_id)
    output_filepath = f"{constants.SAMPLE_OUTPUT_DIR}/{title_id}-mutual-movies.json"
    with open(output_filepath, 'w') as f:
        print(f"\nOutputting results to {output_filepath}")
        json.dump(output_movies, f, indent=2)
    t4 = timeit.default_timer()
    print(f"Total running time: {(t4 - t1):.2f}s.")


if __name__ == "__main__":
    main()

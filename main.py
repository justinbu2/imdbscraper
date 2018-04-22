#!/usr/bin/env python3

import argparse
import collections
import json
import multiprocessing as mp

from src import cast, movies, constants


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Imdb title looker upper")
    parser.add_argument("-t", "--title", type=str, required=True,
                        metavar="TITLE", help="title code of starting movie")
    return parser.parse_args()


def main():
    args = parse_arguments()
    print("Starting up...")
    cast_data = cast.get_cast(args.title)

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

    output_movies = []
    for movie_id, movie in mutual_movies.items():
        if movie_id == args.title or len(movie["mutual_actors"]) == 1:
            continue
        output_movies.append({
            "feature_name": movie["name"],
            "mutual_actors": movie["mutual_actors"]
        })

    # Output movies in descending order of mutual actor count
    output_movies = sorted(output_movies, key=lambda x: -len(x["mutual_actors"]))
    with open(f"{constants.SAMPLE_OUTPUT_DIR}/{args.title}-mutual-movies.json", 'w') as f:
        print("Outputting results...")
        json.dump(output_movies, f, indent=2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import collections
import json

from src import cast, movies, constants


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Imdb title looker upper")
    parser.add_argument("-t", "--title", type=str, required=True,
                        metavar="TITLE", help="title code of starting movie")
    return parser.parse_args()


def main():
    args = parse_arguments()
    cast_data = cast.get_cast(args.title)
    mutual_movies = collections.defaultdict(dict)
    for actor_data in cast_data:
        movies_list = movies.get_movies(actor_data)
        for movie in movies_list:
            if movie["id"] not in mutual_movies:
                mutual_movies[movie["id"]]["name"] = movie["name"]
                mutual_movies[movie["id"]]["mutual_actors"] = []
            mutual_movies[movie["id"]]["mutual_actors"].append(actor_data["name"])

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
        json.dump(output_movies, f, indent=2)


if __name__ == "__main__":
    main()

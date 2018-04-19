import argparse
import json

from src import cast, movies


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Imdb title looker upper")
    parser.add_argument("-t", "--title", type=str, required=True,
                        metavar="TITLE", help="title code of starting movie")
    return parser.parse_args()


def main():
    args = parse_arguments()
    cast_data = cast.get_cast(args.title)
    for actor_data in cast_data:
        actor_data["movies"] = movies.get_movies(actor_data)

    print(json.dumps(cast_data, indent=2))


if __name__ == "__main__":
    main()

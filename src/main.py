import argparse
import bs4
import itertools
import json
import os
import requests

IMDB_HOMEPAGE = "https://wwww.imdb.com"
SAMPLE_OUTPUT_LOC = os.path.realpath(
    "{0}/../dummy-output".format(os.path.dirname(os.path.realpath(__file__))))


def dump(soup):
    with open(SAMPLE_OUTPUT_LOC + "/dummy.html", "w") as f:
        f.write(soup.prettify())


def get_cast(soup):
    # plan to return list of {name: NAME, character: NAME, page: LINK} dicts
    cast = []
    cast_tag = soup.find("table", "cast_list") # type bs4.element.Tag
    odds = cast_tag.find_all("tr", "odd")
    evens = cast_tag.find_all("tr", "even")
    for pair in zip(odds, evens):
        for actor in pair:
            actor_info = {}
            actor_itemprop = actor.find("td", class_="itemprop")
            actor_itemprop_child = actor.find("a", href=True)
            actor_info["link"] = f"{IMDB_HOMEPAGE}{actor_itemprop_child['href']}"
            actor_info["name"] = actor_itemprop.span.text
            actor_character = actor.find("td", class_="character").div
            actor_info["characters"] = [x.text for x in actor_character.find_all("a")]
            cast.append(actor_info)
    return cast


def get_fullcredits_soup(movie_id):
    r = requests.get(f"https://www.imdb.com/title/{movie_id}/fullcredits")
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Imdb title looker upper")
    parser.add_argument("-t", "--title", type=str,
                        metavar="TITLE", help="title code of starting movie")
    return parser.parse_args()


def main():
    args = parse_arguments()
    soup = get_fullcredits_soup(args.title)
    dump(soup)
    cast = get_cast(soup)
    print(json.dumps(cast, indent=2))


if __name__ == "__main__":
    main()

from . import util
from .constants import SAMPLE_OUTPUT_DIR


# Given a soup
def get_cast(movie_id):
    print(f"Getting cast info for movie id {movie_id}...")
    soup = util.lookup(movie_id, f"/title/{movie_id}/fullcredits")

    # plan to return list of {name: NAME, character: NAME, page: LINK} dicts
    cast = []
    cast_tag = soup.find("table", "cast_list") # type bs4.element.Tag
    actors = cast_tag.find_all("tr", ["odd", "even"])
    for i, actor in enumerate(actors):
        actor_info = {}
        actor_itemprop = actor.find("td", class_="itemprop")
        actor_itemprop_child = actor.find("a", href=True)
        actor_info["site_path"] = actor_itemprop_child['href']
        actor_info["id"] = extract_actor_id(actor_info["site_path"])
        actor_info["name"] = actor_itemprop.span.text.strip()
        actor_character = actor.find("td", class_="character").div
        characters = [x.text for x in actor_character.find_all("a")]
        aux_character = ' '.join(actor_character.text.split())
        if aux_character and aux_character not in characters:
            characters.append(aux_character)
        actor_info["characters"] = characters
        cast.append(actor_info)
        print(f"Fetched {i + 1} of {len(actors)} actors for movie id {movie_id}", end='\r')
    print(f"\nSuccessfully fetched all actors for movie id {movie_id}")
    return cast


def extract_actor_id(site_path):
    return site_path.split('/')[2]

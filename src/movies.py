from . import util


# Given an actor, fetch all the movies that the actor was in.
def get_movies(actor_data):
    print(f"Fetching movies for {actor_data['name']}")
    site_path = actor_data["site_path"]
    actor_id = actor_data["id"]
    soup = util.lookup(actor_id, site_path)

    filmography = soup.find("div", id="filmography").find("div", class_="filmo-category-section")
    movies = filmography.find_all("div", ["filmo-row odd", "filmo-row even"])
    movies_list = []
    for i, movie_info in enumerate(movies):
        movie = movie_info.b.find("a", href=True)
        movies_list.append({
            "id": extract_movie_id(movie["href"]),
            "name": movie.text.strip(),
            "site_path": movie["href"]
        })
        print(f"Fetched {i + 1} of {len(movies)} movies for actor {actor_data['name']}", end='\r')
    print(f"\nSuccessfully fetched all movies for actor {actor_data['name']}")
    return movies_list


def extract_movie_id(site_path):
    return site_path.split('/')[2]

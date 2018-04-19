from . import util


# Given an actor, fetch all the movies that the actor was in.
def get_movies(actor_data):
    site_path = actor_data["site_path"]
    actor_name = '_'.join(actor_data["name"].split())
    soup = util.lookup(actor_name, site_path)

    filmography = soup.find("div", id="filmography").find("div", class_="filmo-category-section")
    movies = filmography.find_all("div", ["filmo-row odd", "filmo-row even"])
    movies_list = []
    for movie_info in movies:
        movie = movie_info.b.find("a", href=True)
        movies_list.append({
            "name": movie.text,
            "site_path": movie["href"]
        })
    return movies_list

import requests

api_key = '677f36157cb98fe39b4a8f2f967c5165'

def search_movies(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&language=es-ES'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['results'] if data['results'] else "No se encontraron resultados."
    except requests.exceptions.RequestException as e:
        return f"Error con la solicitud: {e}"
    except Exception as e:
        return f"Ocurrió un error: {e}"

def get_all_movies():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES&page=1'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['results'] if data['results'] else "No se encontraron resultados."
    except requests.exceptions.RequestException as e:
        return f"Error con la solicitud: {e}"
    except Exception as e:
        return f"Ocurrió un error: {e}"

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=es-ES'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error con la solicitud: {e}"
    except Exception as e:
        return f"Ocurrió un error: {e}"

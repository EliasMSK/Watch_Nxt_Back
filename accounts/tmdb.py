import requests


def search_movies(query):
    api_key = '677f36157cb98fe39b4a8f2f967c5165'
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results']
        else:
            return "No se encontraron resultados."
    else:
        return f"Error: {response.status_code} - {response.text}"

import requests

class MovieAPIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def get_now_playing(self):
        url = f"{self.base_url}/movie/now_playing"
        params = {"api_key": self.api_key, "language": "en-US", "region": "GB"}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["results"]
        return []
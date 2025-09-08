from db.database import Database
from typing import List, Dict, Any

class MovieService:
    def __init__(self):
        self.db = Database()
    
    #!Fetches movies
    def get_all_movies(self) -> List[Dict[str, Any]]:
        return self.db.get_movies()
    #!Fetches information about a movie
    def get_movie_by_title(self, title: str) -> Dict[str, Any]:
        movies = self.db.get_movies()
        for movie in movies:
            if movie['title'] == title:
                return movie
        return None
    #!CRUD operations for movies
    def add_movie(self, title: str, genre: str, duration: int, showtimes: List[str], screen: int):
        showtimes_str = ','.join(showtimes)
        self.db.add_movie(title, genre, duration, showtimes_str, screen)
    
    def update_movie(self, movie_id: int, title: str, genre: str, duration: int, showtimes: List[str], screen: int):
        showtimes_str = ','.join(showtimes)
        self.db.update_movie(movie_id, title, genre, duration, showtimes_str, screen)
    
    def delete_movie(self, movie_id: int):
        # Get movie title before deleting
        movies = self.db.get_movies()
        movie_title = None
        for movie in movies:
            if movie['id'] == movie_id:
                movie_title = movie['title']
                break
        
        self.db.delete_movie(movie_id)
        if movie_title:
            self.db.delete_reservations_by_movie(movie_title)
    
    def get_available_screens(self) -> List[int]:
        return [1, 2, 3, 4]
    
    def get_showtimes_for_movie(self, movie_title: str) -> List[str]:
        movie = self.get_movie_by_title(movie_title)
        if movie and movie['showtimes']:
            return movie['showtimes'].split(',')
        return []
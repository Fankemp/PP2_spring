movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

#Task1
def is_high_rated(movie_name):
    for movie in movies:
        if movie["name"].lower() == movie_name.lower():
            return movie["imdb"] > 5.5
    return False

#Task2
def high_rated_movies(movies):
    return [movie for movie in movies if movie["imdb"] > 5.5]

#Task3
def movies_by_category(movies, category):
    return [movie for movie in movies if movie["category"] == category]

#Task4
def average_imdb_score(movies):
    return sum(movie["imdb"] for movie in movies) / len(movies)

#Task5
def average_imdb_by_category(movies, category):
    category_movies = movies_by_category(movies, category)
    return average_imdb_score(category_movies)
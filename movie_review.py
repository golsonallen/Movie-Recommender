import requests
import json
import secrets

class InvalidTitle(Exception):
    pass

#returns num_recs movies related to the movie passed in
def get_movies_from_tastedive(movie_title, num_recs):
    search = {}
    search["q"] = movie_title
    search["type"] = "movies"
    search["limit"] = num_recs
    data = requests.get("https://tastedive.com/api/similar", params = search)
    #parsed = json.loads(data.text)
    #print(json.dumps(parsed, indent=4))
    return data.json()

#extracts the movie titles from the json data
def extract_movie_titles(json_data):
    titles = []
    related_titles = json_data["Similar"]["Results"]
    #no related titles
    if len(related_titles) == 0:
        #raise exception, passing in the invalid title
        raise InvalidTitle(json_data["Similar"]["Info"][0]["Name"])
    for movie_d in related_titles:
        titles.append(movie_d["Name"])
    return titles

#takes in a list of movie titles and returns num_recs related titles for each movie in the list
def get_related_titles(movie_titles, num_recs):
    related_titles = []
    for movie in movie_titles:
        titles = extract_movie_titles(get_movies_from_tastedive(movie, num_recs))
        for title in titles:
            related_titles.append(title)
    return related_titles

#use OMDB API to get info about the movie
def get_movie_data(movie_title):
    search_param = {"apikey": secrets.api_key, "t": movie_title, "r": "json"}
    data = requests.get("http://www.omdbapi.com/", params = search_param)
    #parsed = json.loads(data.text)
    #print(json.dumps(parsed, indent=4))
    return data.json()

#extracts the movies ratings, scales each rating to be out of 100 and returns the average rating
def get_movie_rating(json_data):
    ratings_sum = 0.0
    ratings_lst = json_data["Ratings"]
    for rating in ratings_lst:
        if rating["Source"] == "Rotten Tomatoes":
            ratings_sum += float(rating["Value"][:-1])
        if rating["Source"] == "Internet Movie Database":
            ratings_sum += float(rating["Value"][:-3]) * 10
        if rating["Source"] == "Metacritic":
            ratings_sum += float(rating["Value"][:-4])
    return ratings_sum // 3

#returns info about related movies, sorted in descending order of rating
def get_sorted_recommendations(titles_lst, num_recs):
    movie_data = {}
    related_titles = get_related_titles(titles_lst, num_recs)
    for title in related_titles:
        d = get_movie_data(title)
        rating = get_movie_rating(d)
        #store important info about each movie
        movie_data[title] = rating, d["Plot"], d["Genre"], d["Actors"], d["Awards"]
        #sort based on reviews
    sorted_movie_data = sorted(movie_data.items(), key=lambda x: x[1], reverse=True)
    return sorted_movie_data

#prints each related movie, and some info about it
def print_recommendations(movie_data):
    #movie data is a list of tuples, where the first element of the tuple is the movie title 
    #and the second is a tuple with the movies info
    for movie in movie_data:
        print("")
        print(movie[0])
        print("Genre:", movie[1][2])
        rating = str(movie[1][0])[:2] + '%'
        print("Rating:", rating)
        print("Plot:", movie[1][1])
        print("Awards:", movie[1][4])
        print("Actors:", movie[1][3])
    print("")

def movie_recommendations(num_recs):
    titles = input("Title(s): ")
    print("")
    #strip whitespace in front of titles
    movie_list = [title.lstrip() for title in titles.split(',')]
    return get_sorted_recommendations(movie_list, num_recs)

def main():
    print("Welcome to Movie Recommender!")
    print("-----------------------------")
    num_recs = input("Number of recommendations per movie: ")
    print("Please enter one or more movie titles. Use commas to seperate multiple titles")
    print('Ex. "Superman, The Dark Knight, Avengers Endgame"')
    while True:
        try:
            #exception will be thrown here if there are no related titles
            movies = movie_recommendations(num_recs)
            print("Recommendations")
            print("---------------", end = "")
            print_recommendations(movies)
            break
        except InvalidTitle as e:
            print('Invalid title "{}". Please enter the EXACT title'.format(e))
            
if __name__ == "__main__":
    main()
Movie Recommender
=====================

By Griffin Olson-Allen <griffino@umich.edu>

This program recommends related movies to the user. It utilizes the TasteDive API to get recommended movies and the OMDB API to get info about each related movie. The user enters their desired number of recommendations for each title and one or more movie titles. They receive recommendations for each movie as well as the recommended movie's genre, rating, plot, awards, and actors. 

If the user enters an incorrect title (ex. "Kingsman" or "Kingsman Golden Circle" instead of "Kingsman The Golden Circle") they will receive an error message and get to retry. Movie titles are **not** case sensitive. 
from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route("/")
def hello_world():
  return render_template('home.html',movies=movies)


@app.route("/apply",methods=['post'])
def recommendations():
  data = request.form
  data= dict(data)
  print(data);
  print(data['movie'])
  recommended_movies = []
  movie_index = movies[movies['title'] == data['movie']].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
  for i in movies_list:
    movie_id = movies['movie_id'][i[0]]
    recommended_movies.append(movies['title'][i[0]])

  return render_template('recomm.html',recommended_movies=recommended_movies)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
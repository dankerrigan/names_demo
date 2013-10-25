__author__ = 'dankerrigan'

from flask import Flask, render_template, redirect, url_for, g

from riakjson.query import ASCENDING, DESCENDING
from ..data.name_data import NameData, MAX_YEAR
from ..data.user_data import UserData


# Flask Setup
app = Flask(__name__)

@app.before_request
def before_request():
    g.names = NameData()
    g.users = UserData()

@app.route('/')
def index():
    return render_template('index.html')

## Name Popularity Resources

@app.route('/search/<name_prefix>/years/<start>/<stop>')
def name_search(name_prefix, start, stop):
    result = g.names.partial_name_search(name_prefix, start_year=int(start), stop_year=int(stop))

    return render_template('generic.json', data=result)

@app.route('/usage/<name>/years/<start>/<stop>')
def name_usage(name, start, stop):
    result = g.names.name_usage(name, start_year=int(start), stop_year=int(stop))

    return render_template('generic.json', data=result)

@app.route('/popularity/state/<state>/most/<count>/years/<start>/<stop>')
def most_used_by_state(state, count, start, stop):
    result = g.names.popularity_by_state(state, int(count), DESCENDING, start_year=int(start), stop_year=int(stop))

    return render_template('generic.json', data=result)

@app.route('/popularity/state/<state>/least/<count>/years/<start>/<stop>')
def least_used_by_state(state, count, start, stop):
    result = g.names.popularity_by_state(state, int(count), ASCENDING, start_year=int(start), stop_year=int(stop))

    return render_template('generic.json', data=result)

@app.route('/popularity/states/most/<count>/years/<start>/<stop>')
def most_used_states(count, start, stop):
    result = g.names.state_popularity(int(count), DESCENDING, start_year=int(start), stop_year=int(stop))

    return render_template('generic.json', data=result)

@app.route('/popularity/states/least/<count>/years/<start>/<stop>')
def least_used_states(count, start, stop):
    result = g.names.state_popularity(int(count), ASCENDING, start_year=int(start), stop_year=int(stop))

    return render_template('generic.json', data=result)


## User Resources

@app.route('/user/<user>/favorites')
def user_favorites(user):
    result = g.users.user_favorites(user)

    return render_template('generic.json', data=result)

@app.route('/user/<user>/favorite/add/<name>')
def user_add_favorite(user, name):
    result = g.useres.add_user_favorite(user, name)

    return redirect(url_for('user_favorites'))

from flask import render_template, url_for, redirect, request, Blueprint
from config import Config
from fuel_tracker.forms import SearchForm
import requests
import json

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    """
    Entry point, handles search form input/submission
    """
    form = SearchForm()
    if form.validate_on_submit():
        url = generate_url(form.address_city_state_zip.data, form.fuel_type.data, form.distance_radius.data)
        response = requests.get(url).json()
        results_found = response['total_results']
        locations = response['fuel_stations']
        return redirect(url_for('main.search', locations=locations, results_found=results_found , form=form))
    return render_template('index.html', form = form)

@main.route("/search", methods=['GET', 'POST'])
def search():
    """
    Fetches search results, handles re-search form input/submission
    """
    form = SearchForm()
    if form.validate_on_submit():
        url = generate_url(form.address_city_state_zip.data, form.fuel_type.data, form.distance_radius.data)
        response = requests.get(url).json()
        results_found = response['total_results']
        locations = response['fuel_stations']
        return render_template('search_results.html', locations=locations, results_found=results_found, form=form)
    return redirect(url_for('main.home', form = form))


#Utility to create API query url
def generate_url(location, fuel_type, range_in_miles):
    """
    Concats the search params to the API url
    """
    URL_WITH_KEY = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=" + str(Config.API_KEY)
    #limit or offset? (see docs)
    search_query = URL_WITH_KEY + "&location=" + location + "&fuel_type=" + fuel_type +\
            "&radius=" + range_in_miles
    return search_query
from utils import load_csv


def load_all_data():

    airports = load_csv("data/airports.csv")
    runways = load_csv("data/runways.csv")
    frequencies = load_csv("data/airport-frequencies.csv")
    countries = load_csv("data/countries.csv")
    regions = load_csv("data/regions.csv")

    return airports, runways, frequencies, countries, regions

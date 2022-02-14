import json
from flask import current_app


def load_clubs():
    print(f" * DATABASE clubs : {current_app.config['DATABASE']}/clubs.json")
    with open(f"{current_app.config['DATABASE']}/clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    print(f" * DATABASE competitions : {current_app.config['DATABASE']}/competitions.json")
    with open(f"{current_app.config['DATABASE']}/competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions

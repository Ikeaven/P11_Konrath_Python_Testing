import json


def load_clubs():
    with open("data/clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("data/competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions

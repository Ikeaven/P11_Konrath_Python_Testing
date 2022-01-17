import json
import logging
from datetime import datetime, date

# import logging
from flask import Flask, render_template, request, redirect, flash, url_for

from models import Booking


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


MAX_PLACES = 12
PRICE_PER_PLACE = 1

app = Flask(__name__)

app.secret_key = "something_special"

logging.basicConfig(level=logging.ERROR)

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        return render_template("index.html", error="Unknown Email"), 404
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.errorhandler(400)
@app.errorhandler(403)
@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    # check competition date
    competition_year = int(competition["date"].split(" ")[0].split("-")[0])
    competition_month = int(competition["date"].split(" ")[0].split("-")[1])
    competition_day = int(competition["date"].split(" ")[0].split("-")[2])
    competition_date = date(competition_year, competition_month, competition_day)
    today = date(
        int(datetime.now().strftime("%Y")), int(datetime.now().strftime("%m")), int(datetime.now().strftime("%d"))
    )

    if today > competition_date:
        flash("Error : you cannot book a place in a past competition !")
        return render_template("welcome.html", club=club, competitions=competitions), 403

    try:
        places_required = abs(int(request.form["places"]))
    except ValueError:
        flash("Bad request : number of place must be an integer !")
        return render_template("welcome.html", club=club, competitions=competitions), 400

    # places_required must be < than club point, < than competition's place, < than MAX_PLACES
    if (
        (places_required * PRICE_PER_PLACE) <= int(club["points"])
        and places_required <= int(competition["numberOfPlaces"])
        and places_required <= MAX_PLACES
    ):
        already_booked = Booking.already_booked(club["name"], competition["name"])

        # Check if club has already book places to this competition
        if already_booked:
            logging.info("INFORMATION : the club as already booked place to this competition")

            # Check if passed_book + place_required <= MAX_PLACES
            if int(already_booked.nb_places_booked) + int(places_required) <= MAX_PLACES:
                already_booked.nb_places_booked += int(places_required)
            else:
                flash(f"Error : A club can't reserve more than {MAX_PLACES} places to the same competition")
                return render_template("welcome.html", club=club, competitions=competitions), 403

        # It's the first time the club booked places to this competition => init a booking
        else:
            logging.info("INFORMATION : Is the first time the club booked places to this competition")
            Booking(club["name"], competition["name"], places_required)

        # Mise à jour des valeurs club et competition
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
        club["points"] = int(club["points"]) - (places_required * PRICE_PER_PLACE)
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("Error : Too much places booked")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))

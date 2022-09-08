import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from math import floor


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    error = None
    return render_template("index.html", error=error)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    error = None
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            "welcome.html", club=club, clubs=clubs, competitions=competitions
        )
    except:
        error = "Unknown or invalid email. Please enter a valid email adress : \n"
        return render_template("index.html", error=error)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    date_now = datetime.now()
    now = date_now.strftime("%Y-%m-%d %H:%M:%S")
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    date_competition = competition["date"]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    # Test if the competition is in the future
    if date_competition > now:
        # Check that a number has been entered for places.
        if request.form["places"]:
            placesRequired = int(request.form["places"])
            clubPlaces = floor(int(club["points"]) / 3)

            # Test if everything is fine. If that's the case, book places.
            if (
                placesRequired < 13
                and placesRequired <= clubPlaces
                and placesRequired < int(competition["numberOfPlaces"])
            ):
                competition["numberOfPlaces"] = (
                    int(competition["numberOfPlaces"]) - placesRequired
                )
                club["points"] = int(club["points"]) - (placesRequired * 3)
                flash(
                    f"Great-booking complete! you have booked {placesRequired} places for {competition['name']}"
                )

            # Test if the user try to book more places than available in the competition.
            elif placesRequired > int(competition["numberOfPlaces"]):
                flash(
                    "You can not book more places than available in the competition !"
                )

            # Test if the user is trying to book more than 12 places which is not allowed.
            elif placesRequired > 12:
                flash("You can not book more than 12 points !")

            # Test if the user is trying to buy more places than his own count allow.
            elif placesRequired > clubPlaces:
                flash("You can not book more places than your points count")
        else:
            flash("Please enter a valid number when booking places")

    #  Display a message if the user is trying to book places for a past competition.
    else:
        flash("You can not book places for a competition in the past.")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/displayboard")
def displayboard():
    return render_template("displayboard.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))

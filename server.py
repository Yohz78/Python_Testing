import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
import time


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
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    date_now = datetime.now()
    now = date_now.strftime("%Y-%m-%d %H:%M:%S")
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    date_competition = competition["date"]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    if date_competition > now:
        placesRequired = int(request.form["places"])
        clubPoints = club["points"]
        if placesRequired < 13 and placesRequired <= int(clubPoints):
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = int(club["points"]) - placesRequired
            flash("Great-booking complete!")
        elif placesRequired > 12:
            flash("You can not book more than 12 points !")
        elif placesRequired > int(clubPoints):
            flash("You can not book more places than your points count")
    else:
        placesRequired = int(request.form["places"])
        flash("You can not book places for a competition in the past.")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))

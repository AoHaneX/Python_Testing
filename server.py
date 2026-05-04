import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


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
    # BUG FIX: Entering an unknown email crashes the app
    club = next(
        (club for club in clubs if club["email"] == request.form["email"]), None
    )
    if not club:
        # Error message if email is not found
        flash("Email not found, please try again.")
        return redirect(url_for("index"))

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if not foundClub or not foundCompetition:
        flash("Something went wrong - please try again")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )

    # BUG FIX: Booking places in past competitions
    competition_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )

    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    competitionPlaces = int(competition["numberOfPlaces"])
    flash("Great-booking complete!")

    # BUG FIX: Clubs should not be able to book 0 or negative places
    if placesRequired <= 0:
        flash("You must book at least 1 place.")
        return render_template("welcome.html", club=club, competitions=competitions)

    # BUG FIX: Clubs should not be able to book more than 12 places per competition
    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    # BUG FIX: Clubs should not be able to book more places than available in the competition
    if placesRequired > competitionPlaces:
        flash("Not enough places available in this competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))

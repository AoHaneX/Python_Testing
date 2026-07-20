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


def saveClubs():
    with open("clubs.json", "w") as file:
        json.dump({"clubs": clubs}, file, indent=4)


def saveCompetitions():
    with open("competitions.json", "w") as file:
        json.dump({"competitions": competitions}, file, indent=4)


def updateBooking(club, competition, placesRequested):
    competition["numberOfPlaces"] = str(
        int(competition["numberOfPlaces"]) - placesRequested
    )

    club["points"] = str(int(club["points"]) - placesRequested)


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form["email"].strip().lower()
    club = get_club_by_email(email)
    if not club:
        # Error message if email is not found
        flash("Email not found, please try again.")
        return redirect(url_for("index"))

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)
    if not foundClub or not foundCompetition:
        flash("Something went wrong - please try again")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )

    # BUG FIX: Booking places in past competitions
    if is_past_competition(foundCompetition):
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

    try:
        placesRequired = int(request.form["places"])
    except ValueError:
        flash("Invalid number of places.")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    is_valid, message = validate_booking(club, competition, placesRequired)

    if not is_valid:
        flash(message)
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    flash("Great-booking complete!")

    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


def get_club_by_email(email):
    """
    Searches for a club by email in the global clubs list.
    Returns the club dict if found, None otherwise.
    """
    return next((c for c in clubs if c["email"].lower() == email), None)


def is_past_competition(competition):
    """
    Checks if a competition date is in the past.
    Returns True if the competition is past, False otherwise.
    """
    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    return competition_date < datetime.now()


def validate_booking(club, competition, places_requested):
    available_places = int(competition["numberOfPlaces"])
    club_points = int(club["points"])

    if places_requested <= 0:
        return False, "You must book at least 1 place"

    if places_requested > club_points:
        return False, "Not enough points"

    if is_past_competition(competition):
        return False, "You cannot book places in a past competition"

    if places_requested > 12:
        return False, "You cannot book more than 12 places per competition"

    if places_requested > available_places:
        return False, "Not enough places available"

    if places_requested > club_points:
        return False, "Not enough points"

    return True, ""


def updateBooking(club, competition, places_requested):
    competition["numberOfPlaces"] = str(
        int(competition["numberOfPlaces"]) - places_requested
    )
    club["points"] = str(int(club["points"]) - places_requested)

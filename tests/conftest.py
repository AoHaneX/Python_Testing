import pytest

import server
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def isolated_data(monkeypatch):
    test_clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12",
        },
    ]

    test_competitions = [
        {
            "name": "Future Competition",
            "date": "2099-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Past Competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Limited Competition",
            "date": "2099-03-27 10:00:00",
            "numberOfPlaces": "3",
        },
    ]

    monkeypatch.setattr(server, "clubs", test_clubs)
    monkeypatch.setattr(server, "competitions", test_competitions)

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)

    return test_clubs, test_competitions

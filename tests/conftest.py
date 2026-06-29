import pytest

from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_club():
    return {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}


@pytest.fixture
def low_points_club():
    return {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}


@pytest.fixture
def future_competition():
    return {
        "name": "Future Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }


@pytest.fixture
def past_competition():
    return {
        "name": "Past Competition",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    }


@pytest.fixture
def limited_places_competition():
    return {
        "name": "Limited Places Competition",
        "date": "2030-10-22 13:30:00",
        "numberOfPlaces": "3",
    }

from server import validate_booking


def test_booking_negative_places_is_rejected():
    club = {"name": "Simply Lift", "points": "13"}
    competition = {
        "name": "Future Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    is_valid, message = validate_booking(club, competition, -1)
    assert is_valid is False
    assert message != ""


def test_booking_zero_places_is_rejected():
    club = {"name": "Simply Lift", "points": "13"}
    competition = {
        "name": "Future Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    is_valid, message = validate_booking(club, competition, 0)

    assert is_valid is False
    assert message != ""


def test_booking_more_than_available_places_is_rejected():
    club = {"name": "Simply Lift", "points": "13"}
    competition = {
        "name": "Limited Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "3",
    }
    is_valid, message = validate_booking(club, competition, 5)

    assert is_valid is False
    assert message != ""


def test_booking_more_than_twelve_places_is_rejected():
    club = {"name": "Simply Lift", "points": "20"}
    competition = {
        "name": "Future Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    is_valid, message = validate_booking(club, competition, 13)

    assert is_valid is False
    assert message != ""


def test_booking_past_competition_is_rejected():
    club = {"name": "Simply Lift", "points": "13"}
    competition = {
        "name": "Past Competition",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    is_valid, message = validate_booking(club, competition, 2)

    assert is_valid is False
    assert message != ""


def test_valid_booking_is_accepted():
    club = {"name": "Simply Lift", "points": "13"}
    competition = {
        "name": "Future Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }
    is_valid, message = validate_booking(club, competition, 2)
    assert is_valid is True
    assert message == ""

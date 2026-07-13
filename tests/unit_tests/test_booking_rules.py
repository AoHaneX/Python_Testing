from server import updateBooking, validate_booking


def create_valid_club():
    """Return a club with enough points for a valid booking."""
    return {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13",
    }


def create_future_competition():
    """Return a future competition with available places."""
    return {
        "name": "Future Competition",
        "date": "2099-03-27 10:00:00",
        "numberOfPlaces": "20",
    }


def test_booking_negative_places_is_rejected():
    club = create_valid_club()
    competition = create_future_competition()

    is_valid, message = validate_booking(club, competition, -1)

    assert is_valid is False
    assert message == "You must book at least 1 place"


def test_booking_zero_places_is_rejected():
    club = create_valid_club()
    competition = create_future_competition()

    is_valid, message = validate_booking(club, competition, 0)

    assert is_valid is False
    assert message == "You must book at least 1 place"


def test_booking_more_than_available_places_is_rejected():
    club = create_valid_club()
    club["points"] = "20"

    competition = create_future_competition()
    competition["numberOfPlaces"] = "3"

    is_valid, message = validate_booking(club, competition, 5)

    assert is_valid is False
    assert message == "Not enough places available"


def test_booking_more_than_twelve_places_is_rejected():
    club = create_valid_club()
    club["points"] = "20"

    competition = create_future_competition()

    is_valid, message = validate_booking(club, competition, 13)

    assert is_valid is False
    assert message == "You cannot book more than 12 places per competition"


def test_booking_more_than_club_points_is_rejected():
    club = create_valid_club()
    club["points"] = "4"

    competition = create_future_competition()

    is_valid, message = validate_booking(club, competition, 5)

    assert is_valid is False
    assert message == "Not enough points"


def test_booking_past_competition_is_rejected():
    club = create_valid_club()

    competition = {
        "name": "Past Competition",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "20",
    }

    is_valid, message = validate_booking(club, competition, 3)

    assert is_valid is False
    assert message == "You cannot book places in a past competition"


def test_valid_booking_is_accepted():
    club = create_valid_club()
    competition = create_future_competition()

    is_valid, message = validate_booking(club, competition, 3)

    assert is_valid is True
    assert message == ""


def test_club_points_are_decremented_after_booking():
    club = create_valid_club()
    competition = create_future_competition()

    updateBooking(club, competition, 3)

    assert club["points"] == "10"


def test_competition_places_are_decremented_after_booking():
    club = create_valid_club()
    competition = create_future_competition()

    updateBooking(club, competition, 3)

    assert competition["numberOfPlaces"] == "17"


def test_invalid_booking_does_not_modify_club_or_competition():
    club = create_valid_club()
    club["points"] = "4"

    competition = create_future_competition()

    original_points = club["points"]
    original_places = competition["numberOfPlaces"]

    is_valid, message = validate_booking(club, competition, 5)

    assert is_valid is False
    assert message == "Not enough points"
    assert club["points"] == original_points
    assert competition["numberOfPlaces"] == original_places

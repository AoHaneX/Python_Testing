import pytest


def test_book_page_returns_200(client, isolated_data):
    response = client.get("/book/Future%20Competition/Simply%20Lift")

    assert response.status_code == 200
    assert b"Future Competition" in response.data
    assert b"Simply Lift" in response.data


def test_valid_booking_updates_points_and_places(client, isolated_data):
    clubs, competitions = isolated_data

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Future Competition",
            "places": "3",
        },
    )

    assert response.status_code == 200
    assert clubs[0]["points"] == "10"
    assert competitions[0]["numberOfPlaces"] == "22"
    assert b"Great - booking complete!" in response.data


def test_valid_booking_displays_updated_points(client, isolated_data):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Future Competition",
            "places": "3",
        },
    )

    assert response.status_code == 200
    assert b"10" in response.data


@pytest.mark.parametrize(
    ("places", "expected_message"),
    [
        ("0", b"You must book at least 1 place"),
        ("-1", b"You must book at least 1 place"),
        ("13", b"You cannot book more than 12 places"),
    ],
)
def test_invalid_place_amount_is_rejected(
    client,
    isolated_data,
    places,
    expected_message,
):
    clubs, competitions = isolated_data

    initial_points = clubs[0]["points"]
    initial_places = competitions[0]["numberOfPlaces"]

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Future Competition",
            "places": places,
        },
    )

    assert response.status_code == 200
    assert expected_message in response.data
    assert clubs[0]["points"] == initial_points
    assert competitions[0]["numberOfPlaces"] == initial_places


def test_booking_more_than_available_places_is_rejected(
    client,
    isolated_data,
):
    clubs, competitions = isolated_data

    initial_points = clubs[0]["points"]
    limited_competition = competitions[2]
    initial_places = limited_competition["numberOfPlaces"]

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Limited Competition",
            "places": "5",
        },
    )

    assert response.status_code == 200
    assert b"Not enough places available" in response.data
    assert clubs[0]["points"] == initial_points
    assert limited_competition["numberOfPlaces"] == initial_places


def test_booking_more_than_club_points_is_rejected(
    client,
    isolated_data,
):
    clubs, competitions = isolated_data

    iron_temple = clubs[1]
    future_competition = competitions[0]

    initial_points = iron_temple["points"]
    initial_places = future_competition["numberOfPlaces"]

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Future Competition",
            "places": "5",
        },
    )

    assert response.status_code == 200
    assert b"Not enough points" in response.data
    assert iron_temple["points"] == initial_points
    assert future_competition["numberOfPlaces"] == initial_places


def test_booking_past_competition_is_rejected(
    client,
    isolated_data,
):
    clubs, competitions = isolated_data

    club = clubs[0]
    past_competition = competitions[1]

    initial_points = club["points"]
    initial_places = past_competition["numberOfPlaces"]

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Past Competition",
            "places": "2",
        },
    )

    assert response.status_code == 200
    assert b"past competition" in response.data
    assert club["points"] == initial_points
    assert past_competition["numberOfPlaces"] == initial_places


def test_invalid_number_of_places_is_rejected(
    client,
    isolated_data,
):
    clubs, competitions = isolated_data

    initial_points = clubs[0]["points"]
    initial_places = competitions[0]["numberOfPlaces"]

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Future Competition",
            "places": "abc",
        },
    )

    assert response.status_code == 200
    assert b"Invalid number of places" in response.data
    assert clubs[0]["points"] == initial_points
    assert competitions[0]["numberOfPlaces"] == initial_places

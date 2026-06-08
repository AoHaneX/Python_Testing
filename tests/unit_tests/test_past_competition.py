from server import is_past_competition


def test_is_past_competition_returns_true_for_past_date():
    competition = {
        "name": "Past Competition",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    result = is_past_competition(competition)

    assert result is True


def test_is_past_competition_returns_false_for_future_date():
    competition = {
        "name": "Future Competition",
        "date": "2030-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    result = is_past_competition(competition)

    assert result is False

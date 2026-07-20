import json

import server


def test_save_clubs_writes_clubs_to_json(tmp_path, monkeypatch):
    test_clubs = [
        {
            "name": "Test Club",
            "email": "test@example.com",
            "points": "7",
        }
    ]

    test_file = tmp_path / "clubs.json"

    # Replace application data with controlled test data
    monkeypatch.setattr(server, "clubs", test_clubs)

    server.saveClubs(test_file)

    with open(test_file, encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == {"clubs": test_clubs}


def test_save_competitions_writes_competitions_to_json(
    tmp_path,
    monkeypatch,
):
    test_competitions = [
        {
            "name": "Future Competition",
            "date": "2999-03-27 10:00:00",
            "numberOfPlaces": "17",
        }
    ]

    test_file = tmp_path / "competitions.json"

    # Replace application data with controlled test data
    monkeypatch.setattr(
        server,
        "competitions",
        test_competitions,
    )

    server.saveCompetitions(test_file)

    with open(test_file, encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == {"competitions": test_competitions}


def test_load_clubs_reads_clubs_from_json(tmp_path):
    expected_clubs = [
        {
            "name": "Test Club",
            "email": "test@example.com",
            "points": "10",
        }
    ]

    test_file = tmp_path / "clubs.json"

    with open(test_file, "w", encoding="utf-8") as file:
        json.dump({"clubs": expected_clubs}, file)

    clubs = server.loadClubs(test_file)

    assert clubs == expected_clubs


def test_load_competitions_reads_competitions_from_json(tmp_path):
    expected_competitions = [
        {
            "name": "Test Competition",
            "date": "2999-03-27 10:00:00",
            "numberOfPlaces": "20",
        }
    ]

    test_file = tmp_path / "competitions.json"

    with open(test_file, "w", encoding="utf-8") as file:
        json.dump(
            {"competitions": expected_competitions},
            file,
        )

    competitions = server.loadCompetitions(test_file)

    assert competitions == expected_competitions

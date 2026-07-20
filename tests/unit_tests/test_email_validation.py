import server


def test_get_club_by_email_returns_club_when_email_exists(monkeypatch):
    test_clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }
    ]

    monkeypatch.setattr(server, "clubs", test_clubs)

    club = server.get_club_by_email("john@simplylift.co")

    assert club == test_clubs[0]


def test_get_club_by_email_returns_none_when_email_is_unknown(monkeypatch):
    test_clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }
    ]

    monkeypatch.setattr(server, "clubs", test_clubs)

    club = server.get_club_by_email("unknown@email.com")

    assert club is None


def test_get_club_by_email_ignores_case_and_spaces(monkeypatch):
    test_clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }
    ]
    monkeypatch.setattr(server, "clubs", test_clubs)

    club = server.get_club_by_email("  JOHN@SIMPLYLIFT.CO  ")

    assert club == test_clubs[0]

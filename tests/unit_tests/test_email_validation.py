from server import get_club_by_email


def test_get_club_by_email_returns_club_when_email_exists():
    email = "john@simplylift.co"
    club = get_club_by_email(email)
    assert club is not None
    assert club["email"] == email


def test_get_club_by_email_returns_none_when_email_is_unknown():
    email = "unknown@email.com"
    club = get_club_by_email(email)
    assert club is None

from urllib import response

from server import app


def test_index_page_returns_200(client, isolated_data):
    response = client.get("/")

    assert response.status_code == 200
    assert b"GUDLFT" in response.data


def test_show_summary_with_valid_email_returns_200(client, isolated_data):
    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
    )

    assert response.status_code == 200
    assert b"Simply Lift" in response.data


def test_show_summary_unknown_email_redirects_to_index(client, isolated_data):
    response = client.post(
        "/showSummary",
        data={"email": "unknown@email.com"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_show_summary_unknown_email_displays_error(client, isolated_data):
    response = client.post(
        "/showSummary",
        data={"email": "unknown@email.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email not found, please try again." in response.data


def test_logout_redirects_to_index(client, isolated_data):
    response = client.get("/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

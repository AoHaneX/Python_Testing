from server import app


def test_points_page_is_public():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/points")

        assert response.status_code == 200


def test_points_page_displays_clubs_and_points():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/points")

        assert b"Points Display Board" in response.data
        assert b"Simply Lift" in response.data
        assert b"Iron Temple" in response.data
        assert b"She Lifts" in response.data


def test_index_page_displays_points_board():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200
        assert b"Points Display Board" in response.data
        assert b"Club" in response.data
        assert b"Points" in response.data


def test_welcome_page_displays_points_board_after_login():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/showSummary",
            data={"email": "john@simplylift.co"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Points Display Board" in response.data
        assert b"Simply Lift" in response.data

def test_points_page_is_public(client, isolated_data):
    response = client.get("/points")

    assert response.status_code == 200


def test_points_page_displays_all_clubs(client, isolated_data):
    response = client.get("/points")

    assert response.status_code == 200
    assert b"Points Display Board" in response.data
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


def test_points_page_displays_club_points(client, isolated_data):
    response = client.get("/points")

    assert response.status_code == 200
    assert b"13" in response.data
    assert b"4" in response.data
    assert b"12" in response.data


def test_index_page_displays_points_board(client, isolated_data):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Points Display Board" in response.data
    assert b"Simply Lift" in response.data


def test_welcome_page_displays_points_board_after_login(
    client,
    isolated_data,
):
    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
    )

    assert response.status_code == 200
    assert b"Points Display Board" in response.data
    assert b"Simply Lift" in response.data


def test_points_board_displays_updated_points_after_booking(
    client,
    isolated_data,
):
    client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Future Competition",
            "places": "3",
        },
    )

    response = client.get("/points")

    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"10" in response.data

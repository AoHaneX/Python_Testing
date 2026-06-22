from server import app


def test_show_summary_unknown_email_redirects_to_index():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/showSummary",
            data={"email": "unknown@email.com"},
            follow_redirects=False
        )

        assert response.status_code == 302
        assert response.headers["Location"] == "/"
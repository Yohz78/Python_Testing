from server import app, loadCompetitions, loadClubs


def test_full_use():
    """
    Test a complete app use. Open the index page, log in with a known club email,
    and try to book 2 place for a competition. Afterward, it logs out.
    The display page is then checked offline.
    """

    competitions = loadCompetitions()
    assert competitions[0]["name"] == "Spring Festival"
    clubs = loadClubs()
    assert clubs[0]["name"] == "Simply Lift"

    response = app.test_client().get("/")
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    response = app.test_client().post(
        "/showSummary", data=dict(email="kate@shelifts.co.uk")
    )
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data

    response = app.test_client().get("/book/Test%20competition/She%20Lifts")
    assert response.status_code == 200
    assert b"Test competition" in response.data

    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=2,
            club="She Lifts",
            competition="Test competition",
        ),
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert b"you have booked 2 places for Test competition" in response.data
    assert b"Your club, She Lifts, has 6 points available" in response.data

    response = app.test_client().get("/logout")
    assert response.status_code == 302
    assert b"Redirecting..." in response.data

    response = app.test_client().get("/displayboard")
    assert response.status_code == 200
    assert b"She Lifts : 6 points" in response.data

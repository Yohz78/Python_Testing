from server import app, loadCompetitions, loadClubs


def test_loadCompetitions():
    """Test competitions loading."""
    competitions = loadCompetitions()
    assert competitions[0]["name"] == "Spring Festival"


def test_loadClubs():
    """Test clubs loading."""
    clubs = loadClubs()
    assert clubs[0]["name"] == "Simply Lift"


def test_index_route():
    """Test index route."""
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_success_showSummary_route():
    """Test the log in into the app with a known email."""
    response = app.test_client().post(
        "/showSummary", data=dict(email="admin@irontemple.com")
    )
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data


def test_fail_showSummary_route():
    """Test a fail to log in to the app (wrong email)"""
    response = app.test_client().post("/showSummary", data=dict(email="test@test.fr"))
    assert response.status_code == 200
    assert b"Unknown or invalid email." in response.data


def test_book():
    """Test the url to access the booking page for a given comp/club"""
    response = app.test_client().get("/book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 200
    assert b"Spring Festival" in response.data


def test_fail_book():
    """Test a failure to  access the booking page, providing a wrong comp."""
    response = app.test_client().get("/book/NotAClub/Iron%20Temple")
    assert response.status_code == 500


def test_fail_date_purchasePlaces():
    """Test a failure to purchase place due to a competition in the past."""
    places = 10
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[1]["name"], competition=competitions[0]["name"]
        ),
    )
    assert response.status_code == 200
    assert b"You can not book places for a competition in the past." in response.data


def test_success_purchasePlaces():
    """Test a correct place purchasing."""
    places = 4
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[0]["name"], competition=competitions[2]["name"]
        ),
    )
    print(response.data)
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert b"Your club, Simply Lift, has 1 points available" in response.data


def test_fail_excesscomplaces_purchasePlaces():
    """
    Test a failure to purchase place due to trying to book more place
    than available in the comp.
    """
    places = 13
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[0]["name"], competition=competitions[3]["name"]
        ),
    )
    assert response.status_code == 200
    assert (
        b"You can not book more places than available in the competition !"
        in response.data
    )


def test_fail_excessmax_purchasePlaces():
    """
    Test a failure to purchase place due to trying to book more place
    than a club should be able to book.
    """
    places = 13
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[0]["name"], competition=competitions[2]["name"]
        ),
    )
    assert response.status_code == 200
    assert b"You can not book more than 12 points !" in response.data


def test_fail_excess_self_points_purchasePlaces():
    """
    Test a failure to purchase place due to trying to book more place
    than the club's point count allow.
    """
    places = 10
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[1]["name"], competition=competitions[2]["name"]
        ),
    )
    assert response.status_code == 200
    assert b"You can not book more places than your points count" in response.data


def test_displayboard():
    """
    Test the offline display of the displayboard.
    """
    response = app.test_client().get("/displayboard")
    print(response.data)
    assert response.status_code == 200
    assert b"Point Display board :" in response.data
    assert b"She Lifts : 12 points" in response.data


def test_logout():
    """
    Test the log out URL.
    """
    response = app.test_client().get("/logout")
    assert response.status_code == 302
    assert b"Redirecting..." in response.data

import os
import tempfile

import pytest

from server import app, loadCompetitions, purchasePlaces, loadClubs


def test_index_route():
    response = app.test_client().get("/")

    assert response.status_code == 200


def test_showSummary_route():
    response = app.test_client().post(
        "/showSummary", data=dict(email="admin@irontemple.com")
    )
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data


def test_book():
    response = app.test_client().get("/book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 200
    assert b"Spring Festival" in response.data


def test_loadCompetitions():
    competitions = loadCompetitions()
    assert competitions[0]["name"] == "Spring Festival"


def test_loadClubs():
    clubs = loadClubs()
    assert clubs[0]["name"] == "Simply Lift"


def test_purchasePlaces():
    places = 10
    competitions = loadCompetitions()
    print(competitions)
    original_places = competitions[0]["numberOfPlaces"]
    clubs = loadClubs()
    original_points = clubs[0]["points"]
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[0]["name"], competition=competitions[0]["name"]
        ),
    )
    assert response.status_code == 200
    assert int(competitions[0]["numberOfPlaces"]) == int(original_places) - places
    assert b"Great-booking complete!" in response.data

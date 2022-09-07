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


def test_purchasePlaces(mocker):
    places = 10
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[0]["name"], competition=competitions[0]["name"]
        ),
    )
    assert response.status_code == 200
    assert b"Points available: 3" in response.data
    assert b"Number of Places: 15" in response.data
    assert b"Great-booking complete!" in response.data

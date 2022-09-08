import os
import tempfile

import pytest

from server import app, loadCompetitions, purchasePlaces, loadClubs
from datetime import datetime
import time


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


def test_success_purchasePlaces():
    places = 10
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = app.test_client().post(
        "/purchasePlaces",
        data=dict(
            places=places, club=clubs[0]["name"], competition=competitions[2]["name"]
        ),
    )
    assert response.status_code == 200
    assert b"Points available: 3" in response.data
    assert b"Number of Places: 15" in response.data
    assert b"Great-booking complete!" in response.data


def test_fail__excess_purchasePlaces():
    places = 13
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
    assert b"You can not book more than 12 points !" in response.data


def test_fail_excess_self_points_purchasePlaces():
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


def test_fail_purchasePlaces():
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

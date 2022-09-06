import os
import tempfile

import pytest

from server import app


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


# def test_book():
#     response = app.test_client().post(
#         "/book/Spring%20Festival/Iron%20Temple", data=dict(places="10")
#     )
#     assert response.status_code == 200

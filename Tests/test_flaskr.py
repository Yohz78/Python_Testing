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
    assert response["template"] == "welcome.html"

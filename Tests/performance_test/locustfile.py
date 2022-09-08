import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(5, 15)

    @task(1)
    def displayboard(self):
        response = self.client.get("/displayboard")

    @task(1)
    def updatePoints(self):
        response = self.client.post(
            "/purchasePlaces",
            data=dict(
                places=1,
                club="Simply Lift",
                competition="Test competition",
            ),
        )

    @task(1)
    def index(self):
        response = self.client.get("/")

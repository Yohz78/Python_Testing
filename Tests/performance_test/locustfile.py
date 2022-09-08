from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(5, 15)

    @task(1)
    def competitionDisplay(self):
        response = self.client.post(
            "/showSummary", data=dict(email="admin@irontemple.com")
        )

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

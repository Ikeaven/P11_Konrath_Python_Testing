from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def test_index(self):
        self.client.get("/")

    @task
    def test_clubs_list(self):
        self.client.get("/clubs_list")

    @task
    def test_showSummary(self):
        self.client.post("/showSummary", {"email": "test@test.com"})

    @task
    def test_purchase_places(self):
        data = {
            'club': "client_test",
            'competition': "Fall Classic",
            'places': 1
        }
        self.client.post("/purchasePlaces", data)

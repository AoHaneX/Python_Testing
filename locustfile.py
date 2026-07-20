from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    club_email = "performance@example.com"
    club_name = "Performance Club"
    competition_name = "Performance Competition"

    @task(3)
    def view_competitions(self):
        with self.client.post(
            "/showSummary",
            data={"email": self.club_email},
            name="/showSummary [competitions]",
            catch_response=True,
        ) as response:
            response_time = response.elapsed.total_seconds()

            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            elif response_time >= 5:
                response.failure(f"Competition list took {response_time:.3f} seconds")
            elif self.competition_name not in response.text:
                response.failure(
                    f"Competition '{self.competition_name}' was not displayed"
                )
            else:
                response.success()

    @task(1)
    def book_places(self):
        with self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club_name,
                "competition": self.competition_name,
                "places": "1",
            },
            name="/purchasePlaces [points update]",
            catch_response=True,
        ) as response:
            response_time = response.elapsed.total_seconds()

            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            elif response_time >= 2:
                response.failure(f"Points update took {response_time:.3f} seconds")
            elif "Great - booking complete!" not in response.text:
                response.failure("Booking was not completed")
            else:
                response.success()

import unittest
from fastapi.testclient import TestClient
from main import app  # replace with the actual name of your FastAPI app


class TestRouters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_login_form(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template.name, "login.html")

    def test_login(self):
        form_data = {"username": "test", "password": "test"}
        response = self.client.post("/login", data=form_data)
        self.assertEqual(response.history[0].status_code, 303)
        self.assertEqual(response.url.path, "/bookings")
        self.assertIsNotNone(response.cookies["token"])

    def test_booking_page(self):
        # Login a user to get a token
        form_data = {"username": "test", "password": "test"}
        login_response = self.client.post("/login", data=form_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.url.path, "/bookings")

        # Extract the token from the set-cookie header
        token = login_response.cookies["token"]

        # Make a request to the bookings page with the token
        response = self.client.get("/bookings", cookies={"token": token})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template.name, "booking.html")

    def test_make_booking(self):
        response = self.client.post("/booking", data={"date": "2022-12-01"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Booking successful"})


if __name__ == '__main__':
    unittest.main()

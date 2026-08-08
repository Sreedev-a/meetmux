import unittest

from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_prediction(self):
        response = self.client.post("/predict", json={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["species"], "setosa")

    def test_invalid_request(self):
        response = self.client.post("/predict", json={"sepal_length": -1})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["error"], "validation_error")

    def test_non_json_request(self):
        response = self.client.post("/predict", data="not json", content_type="text/plain")
        self.assertEqual(response.status_code, 415)


if __name__ == "__main__":
    unittest.main()

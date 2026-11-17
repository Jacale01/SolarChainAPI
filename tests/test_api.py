import unittest

from app import create_app


class ApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
        self.client = self.app.test_client()

    def test_register_login_and_paginated_traducoes(self):
        register_response = self.client.post(
            "/auth/register",
            json={"nome": "Ana", "email": "ana@email.com", "password": "123456"},
        )
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            "/auth/login",
            json={"email": "ana@email.com", "password": "123456"},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.get_json()["access_token"]
        self.assertTrue(token)

        create_response = self.client.post(
            "/traducao",
            headers={"Authorization": f"Bearer {token}"},
            json={"energiaGerada": 5000},
        )
        self.assertEqual(create_response.status_code, 201)

        list_response = self.client.get(
            "/traducao?page=1&per_page=10",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(list_response.status_code, 200)
        payload = list_response.get_json()
        self.assertIn("items", payload)
        self.assertIn("total_registros", payload)
        self.assertIn("pagina_atual", payload)


if __name__ == "__main__":
    unittest.main()

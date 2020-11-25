from django.test import TestCase
from django.contrib.auth import get_user_model

class Is_AuthenticatedViewTest(TestCase):
    def test_is_authenticated_when_unauthenticated(self):
        """
        Return a 401 if the user is not authenticated
        """

        self.client.logout()
        response = self.client.get('/auth/')
        self.assertEqual(response.status_code, 401)

    def test_is_authenticated_when_authenticated(self):
        """
        Return a 200 if the user is authenticated
        """

        UserModel = get_user_model()
        username = 'test_user'
        password = 'te$tp@ssw0rd'
        user = UserModel.objects.create_user(username,
                                             'test.email@example.com',
                                             password)
        self.client.login(username=username, password=password)
        response = self.client.get('/auth/')
        self.assertEqual(response.status_code, 200)

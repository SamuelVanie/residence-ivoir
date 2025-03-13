from django.test import TestCase
from .models import Residence, AdminProfile
from django.contrib.auth.models import User

class ResidenceModelTest(TestCase):

    def test_residence_creation(self):
        residence = Residence.objects.create(
            number_of_rooms=3,
            price=150000.00,
            location="123 Main St",
            description="A lovely family home."
        )
        self.assertTrue(isinstance(residence, Residence))
        self.assertEqual(residence.number_of_rooms, 3)

    def test_residence_str_representation(self):
        residence = Residence.objects.create(location="456 Elm St", price=25000.0, number_of_rooms=2)
        self.assertEqual(str(residence), "Residence at 456 Elm St - 2 rooms")

class ResidenceListViewTest(TestCase):
    def test_residence_list_view(self):
        # Create some residences for testing
        Residence.objects.create(number_of_rooms=2, price=100000.00, location="Test Location 1", description="Test description 1")
        Residence.objects.create(number_of_rooms=3, price=150000.00, location="Test Location 2", description="Test description 2")

        response = self.client.get('/residences/')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'residence/residence_list.html')

        # Check that 'residences' are passed in the context
        self.assertTrue('residences' in response.context)


class AdminProfileModelTest(TestCase):

    def test_admin_profile_creation(self):
        user = User.objects.create_user(username='testadmin', password='password123')
        admin_profile = AdminProfile.objects.create(user=user, phone_number="+1234567890")
        self.assertTrue(isinstance(admin_profile, AdminProfile))
        self.assertEqual(admin_profile.user.username, 'testadmin')

    def test_admin_profile_str_representation(self):
        user = User.objects.create_user(username='testadmin2', password='password123')
        admin_profile = AdminProfile.objects.create(user=user)
        self.assertEqual(str(admin_profile), "Admin Profile for testadmin2")

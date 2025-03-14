from django.test import TestCase
from .models import Residence, AdminProfile
from django.contrib.auth.models import User

class ResidenceModelTest(TestCase):

    def test_residence_creation(self):
        residence = Residence.objects.create(
            name="ideal",
            number_of_rooms=3,
            price=150000.00,
            location="123 Main St",
            description="A lovely family home."
        )
        self.assertTrue(isinstance(residence, Residence))
        self.assertEqual(residence.number_of_rooms, 3)

    def test_residence_str_representation(self):
        residence = Residence.objects.create(name="ideal", location="456 Elm St", price=25000.0, number_of_rooms=2)
        self.assertEqual(str(residence), "Residence ideal at 456 Elm St - 2 rooms")

class ResidenceListViewTest(TestCase):
    def test_residence_list_view(self):
        # Create some residences for testing
        Residence.objects.create(name="ideal1", number_of_rooms=2, price=100000.00, location="Test Location 1", description="Test description 1", image='test_image.jpg')
        Residence.objects.create(name="ideal2", number_of_rooms=3, price=150000.00, location="Test Location 2", description="Test description 2", image='test_image.jpg')

        response = self.client.get('/residences/')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'residence/residence_list.html')

        # Check that 'residences' are passed in the context
        self.assertTrue('residences' in response.context)

    def test_filter_residences_by_rooms_view(self):
        # Create residences with different numbers of rooms
        Residence.objects.create(name="ideal1", number_of_rooms=2, price=100000.00, location="Test Location 1", description="Test description 1")
        Residence.objects.create(name="ideal2", number_of_rooms=3, price=150000.00, location="Test Location 2", description="Test description 2")
        Residence.objects.create(name="ideal3", number_of_rooms=2, price=120000.00, location="Test Location 3", description="Test description 3")

        # Filter for residences with 2 rooms
        response_2_rooms = self.client.get('/residences/filter/2/')
        self.assertEqual(response_2_rooms.status_code, 200)
        self.assertEqual(response_2_rooms['content-type'], 'application/json')
        data_2_rooms = response_2_rooms.json()
        self.assertEqual(len(data_2_rooms), 2)
        for residence_data in data_2_rooms:
            self.assertEqual(residence_data['number_of_rooms'], 2)

        # Filter for residences with 3 rooms
        response_3_rooms = self.client.get('/residences/filter/3/')
        self.assertEqual(response_3_rooms.status_code, 200)
        self.assertEqual(response_3_rooms['content-type'], 'application/json')
        data_3_rooms = response_3_rooms.json()
        self.assertEqual(len(data_3_rooms), 1)
        for residence_data in data_3_rooms:
            self.assertEqual(residence_data['number_of_rooms'], 3)


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

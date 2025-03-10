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

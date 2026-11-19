from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactTests(TestCase):
    def test_contact_submission_validation_and_persistence(self):
        url = reverse("main:contact")
        self.assertContains(self.client.get(url), "Contact us")
        data = {"first_name": "Dana", "last_name": "Ali", "email": "invalid", "message": "A suggestion."}
        invalid = self.client.post(url, data)
        self.assertContains(invalid, "Enter a valid email address.")
        self.assertFalse(Contact.objects.exists())
        response = self.client.post(url, {**data, "email": "dana@example.com"}, follow=True)
        self.assertRedirects(response, url)
        self.assertContains(response, "Your message was received.")
        self.assertEqual(Contact.objects.get().email, "dana@example.com")

    def test_only_staff_can_read_the_inbox(self):
        Contact.objects.create(first_name="Dana", last_name="Ali", email="dana@example.com",
                               message="<script>alert(1)</script>")
        url = reverse("main:inbox")
        self.assertRedirects(self.client.get(url), reverse("admin:login") + "?next=" + url)
        user = get_user_model().objects.create_user(username="reader")
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, "dana@example.com", status_code=302)
        user.is_staff = True
        user.save(update_fields=["is_staff"])
        response = self.client.get(url)
        self.assertContains(response, "dana@example.com")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")

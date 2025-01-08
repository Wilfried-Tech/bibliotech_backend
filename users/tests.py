from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'Test',
            'password': 'fcgvhbjklmnkbj'
        }
        self.custom_user_data = {'username': 'custom', 'password': 'fgxfxghcvcghcg',
                                 'email': 'custom@gmail.com'}

        self.custom_user = User.objects.create_user(**self.custom_user_data)
        self.admin_user = User.objects.create_superuser(username='Admin', password='bjcgxfhxkgjxx',
                                                        email='admin@gmail.com')

    def test_create_user(self):
        response = self.client.post(reverse_lazy('users:users-list'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'User not created')
        self.assertFalse(response.data['is_staff'], 'User should not be an admin')

    def test_unique_username(self):
        response = self.client.post(reverse_lazy('users:users-list'), data={**self.user_data, 'username': 'custom'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Username should be unique')

    def test_rejected_weak_password(self):
        response = self.client.post(reverse_lazy('users:users-list'), data={**self.user_data, 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Weak password should be rejected')

    def test_not_admin_list_users(self):
        response = self.client.get(reverse_lazy('users:users-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Only admin can list users')

        self.client.force_authenticate(user=self.custom_user)

        response = self.client.get(reverse_lazy('users:users-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Only admin can list users')

    def test_only_admin_list_retrieve_users(self):
        self.client.force_authenticate(user=self.custom_user)

        response = self.client.get(reverse_lazy('users:users-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Only admin can list users')

        response = self.client.get(reverse_lazy('users:users-detail', kwargs={'pk': self.admin_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'Only admin can retrieve users')

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(reverse_lazy('users:users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Admin should list users')

    def test_only_admin_or_owner_can_retrieve_user(self):
        response = self.client.get(reverse_lazy('users:users-detail', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Only admin or owner can retrieve user')

        self.client.force_authenticate(user=self.custom_user)

        response = self.client.get(reverse_lazy('users:users-detail', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Admin or owner should retrieve user')

    def test_only_owner_can_update_his_profile(self):
        response = self.client.patch(reverse_lazy('users:users-detail', kwargs={'pk': self.custom_user.pk}),
                                     data={'username': 'new'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Only owner can update his profile')

        self.client.force_authenticate(user=self.custom_user)

        response = self.client.patch(reverse_lazy('users:users-detail', kwargs={'pk': self.custom_user.pk}),
                                     data={'username': 'new'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Owner should update his profile')

    def test_only_active_users_can_login(self):
        response = self.client.post(reverse_lazy('token_obtain_pair'), data=self.custom_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Active user should login')

        self.custom_user.is_active = False
        self.custom_user.save()

        response = self.client.post(reverse_lazy('token_obtain_pair'), data=self.custom_user_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Inactive user should not login')

    def test_admin_can_ban_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(reverse_lazy('users:users-ban', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Admin should ban user')

        self.custom_user.refresh_from_db()
        self.assertFalse(self.custom_user.is_active, 'User should be banned')

    def test_admin_can_unban_user(self):
        self.client.force_authenticate(user=self.admin_user)

        self.custom_user.is_active = False
        self.custom_user.save()

        response = self.client.delete(reverse_lazy('users:users-ban', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Admin should unban user')

        self.custom_user.refresh_from_db()
        self.assertTrue(self.custom_user.is_active, 'User should be unbanned')

    def test_admin_can_promote_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(reverse_lazy('users:users-promote', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Admin should promote user')

        self.custom_user.refresh_from_db()
        self.assertTrue(self.custom_user.is_staff, 'User should be promoted')

    def test_admin_can_demote_user(self):
        self.client.force_authenticate(user=self.admin_user)

        self.custom_user.is_staff = True
        self.custom_user.save()

        response = self.client.delete(reverse_lazy('users:users-promote', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Admin should demote user')

        self.custom_user.refresh_from_db()
        self.assertFalse(self.custom_user.is_staff, 'User should be demoted')

    def test_user_can_change_password(self):
        self.client.force_authenticate(user=self.custom_user)

        response = self.client.post(reverse_lazy('users:users-change-password', kwargs={'pk': self.custom_user.pk}),
                                    data={'password': 'newpassfdsword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'User should change password')

    def test_only_owner_can_change_password(self):
        response = self.client.post(reverse_lazy('users:users-change-password', kwargs={'pk': self.custom_user.pk}),
                                    data={'password': 'newpassfdsword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Only owner can change password')

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(reverse_lazy('users:users-change-password', kwargs={'pk': self.custom_user.pk}),
                                    data={'password': 'newpassfdsword'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Only owner can change password')

    def test_user_is_not_really_deleted(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(reverse_lazy('users:users-detail', kwargs={'pk': self.custom_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'User should be deleted')

        self.custom_user.refresh_from_db()
        self.assertFalse(self.custom_user.is_active, 'User should be banned')

    def test_list_inactive_users(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(reverse_lazy('users:users-inactive'))
        self.assertEqual(len(response.data['results']), 0, 'No inactive users should be listed')

        self.custom_user.is_active = False
        self.custom_user.save()

        response = self.client.get(reverse_lazy('users:users-inactive'))
        self.assertEqual(len(response.data['results']), 1, 'Only inactive users should be listed')
        self.assertTrue(all(not User.objects.get(pk=user['id']).is_active for user in response.data['results']),
                        'Only inactive users should be listed')

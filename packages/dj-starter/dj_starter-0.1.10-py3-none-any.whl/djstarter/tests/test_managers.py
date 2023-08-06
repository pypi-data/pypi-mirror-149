from django.test import TestCase

from djstarter.models import AuthUser, ListItem


class AuthManagerTests(TestCase):

    """
    AuthUser Manager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.auth_user_data = {
            'username': 'username_1',
            'password': 'password_1',
            'is_superuser': True,
        }

    def test_by_id(self):
        self.assertEquals(AuthUser.objects.count(), 0)
        with self.assertRaises(AuthUser.DoesNotExist):
            AuthUser.objects.by_id('68992415-fd80-49c4-8dbf-4b0d1e5bafb9')
        auth_user = AuthUser.objects.create_user(**self.auth_user_data)
        auth_user = AuthUser.objects.by_id(auth_user.id)
        self.assertIsInstance(auth_user, AuthUser)

    def test_get_service_user(self):
        user = AuthUser.objects.get_service_user()
        self.assertIsNone(user)

        AuthUser.objects.create_user(**self.auth_user_data)
        user = AuthUser.objects.get_service_user()
        self.assertIsInstance(user, AuthUser)


class ListItemManagerTests(TestCase):

    """
    List Item Manager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.list_item_data = {
            'group': 'group_1',
            'label': 'label_1',
            'value': 'value_1',
        }

    def test_list_item_str(self):
        list_item = ListItem.objects.create(**self.list_item_data)
        val = ListItem.objects.get_value(group=list_item.group, label=list_item.label)

        self.assertEquals(val, 'value_1')

    def test_get_by_oid(self):
        list_item_1 = ListItem.objects.create(**self.list_item_data)
        val = ListItem.objects.get_by_oid(oid=list_item_1.oid)

        self.assertEquals(list_item_1, val)

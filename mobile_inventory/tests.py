from datetime import datetime

from django.test import TestCase

from .models import ModelHelper

class MobiventoryTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(MobiventoryTestCase, cls).setUpClass()

        '''
            Every test instance instance will create is own database that is outside to the actual one.
        '''

        modelhelper = ModelHelper()

        # Populate dummy data for our testing.
        modelhelper.add_staff(
            emp_id=1,
            name='testing',
        )

        # Need to add user so that we can populate 'borrower'
        modelhelper.add_user(
            emp_id=2,
            name='user testing'
        )

        modelhelper.transact_add_device(
            staff_kwargs={'emp_id': 1},
            location_kwargs={'location': 'test_location'},
            barcode='test_barcode',
            category='test_category',
            health='Functional',
            image=None,
            is_available=True,
            model='test_model',
            notes='test_notes',
            serial_no='test_serial_no',
            service_tag='test_service_tag',
            transaction_date=datetime.now()
        )

        modelhelper.transact_add_device(
            staff_kwargs={'emp_id': 1},
            location_kwargs={'location': 'test_location'},
            barcode='test_barcode2',
            category='test_category',
            health='Functional',
            image=None,
            is_available=True,
            model='test_model2',
            notes='test_notes2',
            serial_no='test_serial_no2',
            service_tag='test_service_tag2',
            transaction_date=datetime.now()
        )

        modelhelper.transact_borrow_device(
            device_kwargs={'id': 2},
            staff_kwargs={'emp_id': 1},
            user_kwargs={'emp_id': 2},
            expected_return_date=datetime.now(),
            to_which_project='test'
        )

    def setUp(self):
        self.modelhelper = ModelHelper()
        self.today = datetime.now().date()

    '''
    =======================================================
        BEGIN TESTING
    =======================================================
    '''

    def test_get_all_categories(self):
        actual_categories = self.modelhelper.get_all_categories()
        expected_categories = [
            {
                'id': 1,
                'category': 'test_category'
            }
        ]

        assert expected_categories == list(actual_categories)

    def test_get_all_devices(self):
        actual_devices = self.modelhelper.get_all_devices()
        expected_devices = [
            {
                'status__barcode': 'test_barcode2',
                'status__is_available': False,
                'status__id': 3,
                'status__notes': 'test_notes2',
                'status__health': 'Functional',
                'status__location__location': 'test_location',
                'category__category': 'test_category',
                'category__id': 1,
                'model': 'test_model2',
                'serial_no': 'test_serial_no2',
                'id': 2,
                'status__location__id': 1,
                'service_tag': 'test_service_tag2'
            }, {
                'status__barcode': 'test_barcode',
                'status__is_available': True,
                'status__id': 1,
                'status__notes': 'test_notes',
                'status__health': 'Functional',
                'status__location__location': 'test_location',
                'category__category': 'test_category',
                'category__id': 1,
                'model': 'test_model',
                'serial_no': 'test_serial_no',
                'id': 1,
                'status__location__id': 1,
                'service_tag': 'test_service_tag'
            }
        ]

        assert list(expected_devices) == list(actual_devices)

    def test_get_all_available_devices(self):
        actual_devices = self.modelhelper.get_all_available_devices()
        expected_devices = [
            {
                'status__barcode': 'test_barcode',
                'status__is_available': True,
                'status__id': 1,
                'status__notes': 'test_notes',
                'status__health': 'Functional',
                'status__location__location': 'test_location',
                'category__category': 'test_category',
                'category__id': 1,
                'model': 'test_model',
                'serial_no': 'test_serial_no',
                'id': 1,
                'status__location__id': 1,
                'service_tag': 'test_service_tag'
            }
        ]

        assert expected_devices == list(actual_devices)

    def test_get_all_borrowed_devices(self):
        actual_devices = self.modelhelper.get_all_borrowed_devices()
        expected_devices = [
            {
                'status__barcode': 'test_barcode2',
                'status__is_available': False,
                'status__id': 3,
                'status__notes': 'test_notes2',
                'status__health': 'Functional',
                'status__location__location': 'test_location',
                'category__category': 'test_category',
                'category__id': 1,
                'model': 'test_model2',
                'serial_no': 'test_serial_no2',
                'id': 2,
                'status__location__id': 1,
                'service_tag': 'test_service_tag2',
                'borrower__name': 'user testing'
            }
        ]

        assert expected_devices == list(actual_devices)

    def test_get_all_locations(self):
        actual_locations = self.modelhelper.get_all_locations()
        expected_locations = [
            {
                'id': 1,
                'location': 'test_location',
            }
        ]

        assert expected_locations == list(actual_locations)

    def test_get_all_staffs(self):
        actual_staffs = self.modelhelper.get_all_staffs()
        expected_staffs = [
            {
                'id': 1,
                'emp_id': '1',
                'name': 'testing',
                'date_added': self.today,
                'added_by__name': None,
                'added_by__id': None,
                'added_by__emp_id': None
            }
        ]

        assert expected_staffs == list(actual_staffs)

    def test_get_all_staff_transactions(self):
        actual_staff_transactions = self.modelhelper.get_all_staff_transactions(staff_emp_id=1)
        expected_staff_transactions_sample = {
            'status__location__location': 'test_location',
            'device__category__id': 1,
            'staff__name': 'testing',
            'id': 1,
            'device__model': 'test_model',
            'device__id': 1,
            'device__category__category': 'test_category',
            'device__service_tag': 'test_service_tag',
            'staff__id': 1,
            'status__health': 'Functional',
            'status__image': None,
            'status__location__id': 1,
            'status__notes': 'test_notes',
            'status__is_available': True,
            'device__serial_no': 'test_serial_no',
            'staff__emp_id': '1',
            'status__barcode': 'test_barcode',
            'transaction_date': self.today,
            'status__id': 1,
            'transaction_type__transaction_type': 1
        }

        assert expected_staff_transactions_sample in list(actual_staff_transactions)

    def test_get_all_users(self):
        actual_users = self.modelhelper.get_all_users()
        expected_users = [
            {
                'id': 1,
                'emp_id': 2,
                'name': 'user testing'
            }
        ]

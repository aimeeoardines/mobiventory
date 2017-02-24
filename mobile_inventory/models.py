from django.db import models
from django.db.models import Q
from django.utils import timezone


class Category(models.Model):
    category = models.CharField('Category', max_length=100)

    def __str__(self):
        return self.category


class Location(models.Model):
    location = models.CharField('Location', max_length=100)

    def __str__(self):
        return self.location


class Status(models.Model):
    health = models.CharField(
        'Health',
        max_length=50,
        choices=([
            ('Functional', 'Functional'),
            ('Defective', 'Defective'),
        ]),
        default='Functional',
    )
    image = models.ImageField(upload_to='images', null=True, blank=True)
    is_available = models.BooleanField('is_available', default=True)
    notes = models.TextField('Notes', blank=True, null=True)
    barcode = models.CharField('Barcode', max_length=100)
    location = models.ForeignKey(Location, blank=True, null=True)

    def __str__(self):
        return 'health: {}, is_available: {}, notes: {}, barcode: {}, {}'.format(
            self.health,
            self.is_available,
            self.notes,
            self.barcode,
            self.location,
        )


class Device(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    model = models.CharField('Model', max_length=100)
    serial_no = models.CharField('Serial No.', max_length=50)
    service_tag = models.CharField('Service Tag', max_length=100)

    def __str__(self):
        return 'model: {}, serial no.: {}, service_tag: {}, category: {}, {}'.format(
            self.model,
            self.serial_no,
            self.service_tag,
            self.category,
            self.status,
        )


class Staff(models.Model):
    added_by = models.ForeignKey('self', blank=True, null=True)
    date_added = models.DateField(default=timezone.now)
    emp_id = models.CharField('Emp ID', max_length=50)
    name = models.CharField('Name', max_length=100)

    def __str__(self):
        return 'emp_id: {}, name: {}, added by: {}, date added: {}'.format(
            self.emp_id,
            self.name,
            self.added_by,
            self.date_added,
        )


class TransactionType(models.Model):
    transaction_type = models.IntegerField('Transaction Type')

    def __str__(self):
        transaction  = {1: 'Add', 2: 'Modify',3: 'Borrow', 4: 'Return'}
        if self.transaction_type in transaction:
            return transaction[self.transaction_type]
        return 'Invalid type: ' + self.transaction_type


class Transaction(models.Model):
    staff = models.ForeignKey(Staff)
    transaction_type = models.ForeignKey(TransactionType)
    device = models.ForeignKey(Device)
    status = models.ForeignKey(Status, blank=True, null=True)
    transaction_date = models.DateTimeField('Date', default=timezone.now, blank=True)

    def __str__(self):
        return 'id: {}, {}, {}, {}, transaction_date: {}'.format(
            self.id,
            self.staff,
            self.transaction_type,
            self.device,
            self.transaction_date,
        )


class Team(models.Model):
    name = models.CharField('Name', max_length=50)

    def __str__(self):
        return self.name


class User(models.Model):
    emp_id = models.CharField('Emp ID', max_length=50)
    name = models.CharField('Name', max_length=100)
    team = models.ForeignKey(Team, blank=True, null=True)

    def __str__(self):
        return 'emp_id: {}, name: {}'.format(self.emp_id, self.name)


class TransactionBorrow(models.Model):
    transaction = models.ForeignKey(Transaction)
    borrower = models.ForeignKey(User, default=15)
    to_which_project = models.CharField('Project', max_length=100, blank=True, null=True)
    expected_return_date = models.DateField('Expected return date', blank=True, null=True)

    def __str__(self):
        return 'id: {}, borrower: {}, to_which_project: {}, {}, expected_return_date: {}'.format(
            self.id,
            self.borrower,
            self.to_which_project,
            self.transaction,
            self.expected_return_date,
        )


class ModelHelper:
    '''
        Helpers class aid complex queries
    '''

    def __init__(self):
        self.transaction_types = {'add': 1, 'modify': 2, 'borrow': 3, 'return': 4}

    def add_staff(self, emp_id, name, added_by=None, date_added=timezone.now):
        staff = Staff.objects.create(emp_id=emp_id, name=name, added_by=added_by, date_added=date_added)
        return staff

    def add_user(self, emp_id, name):
        user =  User.objects.create(emp_id=emp_id, name=name)

    def is_barcode_existed(self, barcode):
        return Device.objects.filter(status__barcode=barcode).values()

    def is_serial_no_existed(self, serial_no):
        return Device.objects.filter(serial_no=serial_no).values()

    def is_service_tag_existed(self, service_tag):
        return Device.objects.filter(service_tag=service_tag).values()

    def get_all_available_devices(self, limit=0, offset=0):
        if limit:
            devices = Device.objects.filter(
                    status__is_available=True
                ).exclude(
                    status__health='Defective'
                ).exclude(
                    status__health='DEFECTIVE'
                ).exclude(
                    status__health='defective'
                ).order_by('-id').values(
                'id',
                'status__id',
                'status__barcode',
                'status__health',
                'status__is_available',
                'status__image',
                'status__notes',
                'status__location__id',
                'status__location__location',
                'category__id',
                'category__category',
                'model',
                'serial_no',
                'service_tag',
            )[offset:limit + offset]

        devices = Device.objects.filter(
                status__is_available=True
            ).exclude(
                status__health='Defective'
            ).exclude(
                status__health='DEFECTIVE'
            ).exclude(
                status__health='defective'
            ).order_by('-id').values(
            'id',
            'status__id',
            'status__barcode',
            'status__health',
            'status__is_available',
            'status__image',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'category__id',
            'category__category',
            'model',
            'serial_no',
            'service_tag',
        )

        # for device in devices:
        #     transaction = Transaction.objects.filter(device__id=device['id']).order_by('-transaction_date').first()
        return devices

    def get_all_borrowed_devices(self, limit=0, offset=0):
        if limit:
            borrowed_devices = Device.objects.filter(status__is_available=False).order_by('-id').values(
                'id',
                'status__id',
                'status__barcode',
                'status__health',
                'status__is_available',
                'status__image',
                'status__notes',
                'status__location__id',
                'status__location__location',
                'category__id',
                'category__category',
                'model',
                'serial_no',
                'service_tag',
            )[offset:limit + offset]
        else:
            borrowed_devices = Device.objects.filter(status__is_available=False).order_by('-id').values(
                'id',
                'status__id',
                'status__barcode',
                'status__health',
                'status__is_available',
                'status__image',
                'status__notes',
                'status__location__id',
                'status__location__location',
                'category__id',
                'category__category',
                'model',
                'serial_no',
                'service_tag',
            )

        for device in borrowed_devices:
            borrower = TransactionBorrow.objects.filter(transaction__device__id=device['id']).values('borrower__name')
            if borrower:
                device.update(borrower[0])

        return borrowed_devices

    def get_all_categories(self):
        return Category.objects.all().values()

    def get_all_devices(self, limit=0, offset=0):
        if limit:
            devices = Device.objects.all().order_by('-id').values(
                'id',
                'status__id',
                'status__barcode',
                'status__health',
                'status__is_available',
                'status__image',
                'status__notes',
                'status__location__id',
                'status__location__location',
                'category__id',
                'category__category',
                'model',
                'serial_no',
                'service_tag',
            )[offset:limit]

        devices = Device.objects.all().order_by('-id').values(
            'id',
            'status__id',
            'status__barcode',
            'status__health',
            'status__is_available',
            'status__image',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'category__id',
            'category__category',
            'model',
            'serial_no',
            'service_tag',
        )
        for device in devices:
            is_borrowed = self.is_device_borrowed(device['id'])
            device.update({'is_borrowed': is_borrowed})
        return devices

    def get_all_locations(self):
        return Location.objects.all().values()

    def get_all_staffs(self):
        return Staff.objects.all().values(
            'id',
            'emp_id',
            'name',
            'date_added',
            'added_by__id',
            'added_by__emp_id',
            'added_by__name',
        )

    def get_all_staff_transactions(self, staff_emp_id):
        all_transactions = []
        transactions = Transaction.objects.filter(staff__emp_id=staff_emp_id).order_by('-transaction_date').values(
            'id',
            'device__id',
            'device__model',
            'device__serial_no',
            'device__service_tag',
            'device__category__id',
            'device__category__category',
            'status__id',
            'status__health',
            'status__image',
            'status__is_available',
            'status__barcode',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'staff__id',
            'staff__emp_id',
            'staff__name',
            'transaction_date',
            'transaction_type__transaction_type',
        )
        for transaction in transactions:
            is_borrowed = self.is_device_borrowed(transaction['device__id'])
            if is_borrowed:
                transaction_borrow = self.get_borrowing_transaction(transaction['id'])
                if transaction_borrow:
                    transaction.update(transaction_borrow[0])
            all_transactions.append(transaction)

        return all_transactions

    def get_all_teams(self):
        teams = Team.objects.all().values(
            'id',
            'name',
        )

    def get_all_transactions(self, transaction_id):
        if transaction_id:
            transactions = Transaction.objects.filter(id=transaction_id).values(
            'id',
            'device__id',
            'device__model',
            'device__serial_no',
            'device__service_tag',
            'device__category__id',
            'device__category__category',
            'status__id',
            'status__health',
            'status__image',
            'status__is_available',
            'status__barcode',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'staff__id',
            'staff__emp_id',
            'staff__name',
            'transaction_date',
            'transaction_type__transaction_type',
        )
        transactions = Transaction.objects.all().values(
            'id',
            'device__id',
            'device__model',
            'device__serial_no',
            'device__service_tag',
            'device__category__id',
            'device__category__category',
            'status__id',
            'status__health',
            'status__image',
            'status__is_available',
            'status__barcode',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'staff__id',
            'staff__emp_id',
            'staff__name',
            'transaction_date',
            'transaction_type__transaction_type',
        )
        return transactions

    def get_all_users(self):
        return User.objects.all().values()

    def get_borrowing_transaction(self, transaction_id):
        return TransactionBorrow.objects.filter(transaction__id=transaction_id).values(
            'id',
            'borrower__id',
            'borrower__emp_id',
            'borrower__name',
            'to_which_project',
            'transaction__transaction_date',
            'transaction__transaction_type__transaction_type',
            'expected_return_date',
        )

    def get_instance_device(self, kwargs):
        keys = kwargs.keys()
        device = ''
        try:
            if keys.__contains__('id') and kwargs['id']:
                device = Device.objects.filter(id=kwargs['id']).first()
            elif keys.__contains__('barcode') and kwargs['barcode']:
                device = Device.objects.filter(status__barcode=kwargs['barcode']).first()
            elif keys.__contains__('serial_no') and kwargs['serial_no']:
                device = Device.objects.filter(serial_no=kwargs['serial_no']).first()
            else:
                device = Device.objects.filter(service_tag=kwargs['service_tag']).first()
        except Exception as e:
            raise e

        return device

    def get_instance_location(self, kwargs):
        keys = kwargs.keys()
        location = ''

        try:
            if keys.__contains__('location_id') and kwargs['location_id']:
                location = Location.objects.get(id=kwargs['location_id'])
            else:
                location = Location.objects.get_or_create(
                    location=kwargs['location'])[0]
                print(location)
        except:
            return 'Location does not exist'

        return location

    def get_instance_staff(self, kwargs):
        keys = kwargs.keys()
        staff = ''

        try:
            if keys.__contains__('id') and kwargs['id']:
                staff = Staff.objects.get(id=kwargs['id'])
            elif keys.__contains__('name') and kwargs['name']:
                staff = Staff.objects.get(name=kwargs['name'])
            else:
                staff = Staff.objects.get(emp_id=kwargs['emp_id'])
        except Exception:
            return 'Staff does not exist'

        return staff

    def get_instance_user(self, kwargs):
        keys = kwargs.keys()
        user = ''

        try:
            if keys.__contains__('borrower_id') and kwargs['borrower_id'] or keys.__contains__('id') and kwargs['id']:
                if kwargs['id']:
                    return User.objects.get(id=kwargs['borrower_id'])
                return User.objects.get(id=kwargs['borrower_id'])
            elif keys.__contains__('borrower_name') and kwargs['borrower_name'] or keys.__contains__('name') and kwargs['name']:
                if kwargs['name']:
                    return User.objects.get(name=kwargs['name'] )
                return User.objects.get(name=kwargs['borrower_name'] )
            else:
                try:
                    key = kwargs['emp_id']
                except:
                    key = kwargs['borrower_emp_id']
                return User.objects.get(emp_id=key)
        except Exception as e:
            raise e

    def is_device_borrowed(self, device_id):
        transaction = Transaction.objects.filter(device__id=device_id).order_by('-transaction_date').first()

        print(transaction.transaction_type)

        return bool(transaction.transaction_type.transaction_type == self.transaction_types['borrow'])

    def search_device(self, keyword):
        devices = Device.objects.filter(
            Q(serial_no__icontains=keyword) |
            Q(service_tag__icontains=keyword) |
            Q(model__icontains=keyword) |
            Q(category__category__icontains=keyword) |
            Q(status__barcode__icontains=keyword) |
            Q(status__health__icontains=keyword) |
            Q(status__notes__icontains=keyword) |
            Q(status__location__location__icontains=keyword)
        ).values(
            'id',
            'status__id',
            'status__barcode',
            'status__health',
            'status__is_available',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'category__id',
            'category__category',
            'model',
            'serial_no',
            'service_tag',
        )

        return devices

    def transact_add_device(self, staff_kwargs, location_kwargs, barcode, category, health, image, is_available, model, notes, serial_no, service_tag, transaction_date):
        staff = self.get_instance_staff(staff_kwargs)
        location_obj = self.get_instance_location(location_kwargs)
        status = Status.objects.create(
            barcode=barcode,
            health=health,
            image=image,
            is_available=is_available,
            notes=notes,
            location=location_obj,
        )
        status.save()

        category_obj, is_created = Category.objects.get_or_create(category=category)

        device = Device.objects.create(
            category=category_obj,
            model=model,
            serial_no=serial_no,
            service_tag=service_tag,
            status=status,
        )
        device.save()

        transaction_type, is_created = TransactionType.objects.get_or_create(
            transaction_type=self.transaction_types['add'],
        )

        transaction = Transaction.objects.create(
            staff=staff,
            device=device,
            transaction_type=transaction_type,
            status=status,
            transaction_date=transaction_date,
        )
        transaction.save()

        return Transaction.objects.filter(id=transaction.id).all().values(
            'id',
            'device__id',
            'device__model',
            'device__serial_no',
            'device__service_tag',
            'device__category__id',
            'device__category__category',
            'status__id',
            'status__health',
            'status__image',
            'status__is_available',
            'status__barcode',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'staff__id',
            'staff__emp_id',
            'staff__name',
            'transaction_date',
            'transaction_type__transaction_type',
        )[0]

    def transact_borrow_device(self, device_kwargs, staff_kwargs, user_kwargs, expected_return_date=None, to_which_project=''):
        device = self.get_instance_device(device_kwargs)
        staff = self.get_instance_staff(staff_kwargs)
        user = self.get_instance_user(user_kwargs)

        device_status = device.status
        status = Status.objects.get(id=device_status.id)

        new_status = Status.objects.create(
            health=status.health,
            image=status.image,
            is_available=False,
            notes=status.notes,
            barcode=status.barcode,
            location=status.location,
        )
        device.status = new_status
        device.save()

        transaction_type_obj, is_created = TransactionType.objects.get_or_create(
            transaction_type=self.transaction_types['borrow'],
        )

        transaction = Transaction.objects.create(
            staff=staff,
            transaction_type=transaction_type_obj,
            device=device,
            status=new_status,
        )
        transaction.save()
        transaction_obj = Transaction.objects.get(pk=transaction.pk)

        transaction_borrow = TransactionBorrow.objects.create(
            borrower=user,
            transaction=transaction_obj,
            to_which_project=to_which_project,
            expected_return_date=expected_return_date,
        )
        transaction_borrow.save()

        return TransactionBorrow.objects.filter(id=transaction_borrow.id).values(
            'id',
            'transaction__id',
            'transaction__device__id',
            'transaction__device__model',
            'transaction__device__serial_no',
            'transaction__device__service_tag',
            'transaction__device__category__id',
            'transaction__device__category__category',
            'transaction__status__id',
            'transaction__status__health',
            'transaction__status__image',
            'transaction__status__notes',
            'transaction__status__barcode',
            'transaction__status__location__id',
            'transaction__status__location__location',
            'transaction__staff__id',
            'transaction__staff__emp_id',
            'transaction__staff__name',
            'borrower__id',
            'borrower__emp_id',
            'borrower__name',
            'to_which_project',
            'transaction__transaction_date',
            'transaction__transaction_type__transaction_type',
            'expected_return_date',
        )

    def transact_modify_device(self, staff_kwargs, location_kwargs, device_id, barcode, category, health, image, is_available, model, notes,  serial_no, service_tag, transaction_date):
        location_obj = self.get_instance_location(location_kwargs)
        staff = self.get_instance_staff(staff_kwargs)

        status = Status.objects.create(
            barcode=barcode,
            health=health,
            image=image,
            is_available=is_available,
            notes=notes,
            location=location_obj,
        )
        status.save()

        category_obj, is_created = Category.objects.get_or_create(category=category)

        try:
            device = Device.objects.get(id=device_id)
            device.category = category_obj
            device.status = status
            device.model = model
            device.serial_no = serial_no
            device.service_tag = service_tag

            device.save()
        except Exception as e:
            raise e

        transaction_type, is_created = TransactionType.objects.get_or_create(transaction_type=self.transaction_types['modify'])

        transaction = Transaction.objects.create(
            staff=staff,
            device=device,
            status=device.status,
            transaction_type=transaction_type,
            transaction_date=transaction_date,
        )
        transaction.save()

        return Transaction.objects.filter(id=transaction.id).values(
            'id',
            'device__id',
            'device__model',
            'device__serial_no',
            'device__service_tag',
            'device__category__id',
            'device__category__category',
            'status__id',
            'status__health',
            'status__image',
            'status__barcode',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'staff__id',
            'staff__emp_id',
            'staff__name',
            'transaction_date',
            'transaction_type__transaction_type',
        )


    def transact_return_device(self, device_kwargs, staff_kwargs, health, notes, image, is_available, barcode, location, transaction_date):
        device = self.get_instance_device(device_kwargs)
        staff = self.get_instance_staff(staff_kwargs)

        transaction_type_obj, is_created = TransactionType.objects.get_or_create(
            transaction_type=self.transaction_types['return'],
        )

        location_obj, is_created = Location.objects.get_or_create(location=location)
        status = Status.objects.create(
            health=health,
            notes=notes,
            image=image,
            is_available=is_available,
            barcode=barcode,
            location=location_obj,
        )

        Device.objects.filter(id=device.id).update(
            status=status,
        )

        # Get the instance again since we update the status
        device = self.get_instance_device(device_kwargs)

        transaction = Transaction.objects.create(
            staff=staff,
            device=device,
            status=device.status,
            transaction_type=transaction_type_obj,
            transaction_date=transaction_date,
        )

        return Transaction.objects.filter(id=transaction.id).values(
            'id',
            'device__id',
            'device__model',
            'device__serial_no',
            'device__service_tag',
            'device__category__id',
            'device__category__category',
            'status__id',
            'status__health',
            'status__image',
            'status__barcode',
            'status__notes',
            'status__location__id',
            'status__location__location',
            'staff__id',
            'staff__emp_id',
            'staff__name',
            'transaction_date',
            'transaction_type__transaction_type',
        )

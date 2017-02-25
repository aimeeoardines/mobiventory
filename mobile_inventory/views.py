import base64
import json

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (
    AddCategoryForm,
    AddDeviceForm,
    AddLocationForm,
    AddStatusForm,
    BorrowForm,
    LoginForm,
    ModifyStatusForm,
    ModifyDeviceForm,
    ReturnForm,
    SearchForm,
)

from .models import (
    Category,
    Device,
    Location,
    Staff,
    Status,
    TransactionType,
    Transaction,
    User,
    # Add your model import here below

    # Additional classes/functions
    ModelHelper,  # A class that aids you to access models
)

from .reportmaker import Report


modelhelper = ModelHelper()


class AddStaffAPI(APIView):

    def get(self, request):
        try:
            emp_id = request.query_params['emp_id']
            name = request.query_params['name']
        except:
            return Response({'msg': 'Keys not sufficed'}, 406)

        added_by = None
        try:
            added_by = request.query_params['added_by']
        except:
            pass

        staff = modelhelper.add_staff(emp_id=emp_id, name=name, added_by=added_by)

        return Response({
            'id': staff.id,
            'emp_id': staff.emp_id,
            'name': staff.name,
        })


class DeleteStaffAPI(APIView):

    def get(self, request):
        if request.query_params.__contains__('id'):
            staff_id = request.query_params['id']
            count, obj = Staff.objects.filter(id=staff_id).delete()
        elif request.query_params.__contains__('emp_id'):
            emp_id = request.query_params['emp_id']
            count, obj = Staff.objects.filter(emp_id=emp_id).delete()
        else:
            return Response({'msg': 'Keys not sufficed'}, 406)

        # Deletion of an object returns the count on index 0
        return Response({'count': count, 'obj_related': obj})


class UpdateStaffAPI(APIView):

    def get(self, request):
        try:
            if request.query_params.__contains__('id'):
                staff_id = request.query_params['id']
                new_emp_id = request.query_params['new_emp_id']
                new_name = request.query_params['new_name']
                obj = Staff.objects.filter(id=staff_id).update(emp_id=new_emp_id, name=new_name)
            else:
                emp_id = request.query_params['emp_id']
                new_emp_id = request.query_params['new_emp_id']
                new_name = request.query_params['new_name']
                obj = Staff.objects.filter(emp_id=emp_id).update(emp_id=new_emp_id, name=new_name)
        except Exception as e:
            return Response({'msg': repr(e)}, 406)

        return Response({'updated': 'true' if obj else 'false'})


class GetStaffAPI(APIView):

    def get(self, request):
        if request.query_params.__contains__('emp_id'):
            emp_id = request.query_params['emp_id']
            obj = Staff.objects.filter(emp_id=emp_id)
        elif request.query_params.__contains__('name'):
            name = request.query_params['name']
            obj = Staff.objects.filter(name=name)
        else:
            return Response({'msg': 'Keys not sufficed'}, 406)

        return Response(obj.values())


class ValidateStaffAPI(APIView):

    def get(self, request):
        emp_id = request.query_params['emp_id']
        staff_obj = modelhelper.get_instance_staff({'emp_id':emp_id})
        try:
            staff = dict(Staff.objects.filter(id=staff_obj.id).values()[0])
            staff.update({'is_authorized': 'true'})
            return Response(staff)
        except:
            return Response({'is_authorized': 'false'})



class GetStaffTransactions(APIView):

    def get(self, request):
        try:
            staff_emp_id = request.query_params['staff_emp_id']
            if not staff_emp_id:
                raise
        except:
            return Response({'msg': '`staff_emp_id` not sufficed'}, 406)

        if not is_staff_authorized(staff_emp_id):
            return Response({'msg': 'Staff not authorized'}, 406)

        return Response(modelhelper.get_all_staff_transactions(staff_emp_id))



class GetAllUsers(APIView):
    def get(self, request):
        users = modelhelper.get_all_users()

        return Response(users)


class AddUserAPI(APIView):

    def get(self, request):
        emp_id = request.query_params['emp_id']
        name = request.query_params['name']

        user = User.objects.create(emp_id=emp_id, name=name)

        return Response({'id': user.id, 'emp_id': user.emp_id, 'name': user.name})


class UpdateUserAPI(APIView):

    def get(self, request):
        if request.query_params.__contains__('id'):
            user_id = request.query_params['id']
            new_emp_id = request.query_params['new_emp_id']
            new_name = request.query_params['new_name']
            obj = User.objects.filter(id=user_id).update(emp_id=new_emp_id, name=new_name)
        elif request.query_params.__contains__('emp_id'):
            emp_id = request.query_params['emp_id']
            new_emp_id = request.query_params['new_emp_id']
            new_name = request.query_params['new_name']
            obj = User.objects.filter(emp_id=emp_id).update(emp_id=new_emp_id, name=new_name)
        else:
            return Response({'msg': 'Keys not sufficed'}, 406)

        return Response({'updated': 'true' if obj else 'false'})


class DeleteUserAPI(APIView):

    def get(self, request):
        if request.query_params.__contains__('emp_id'):
            emp_id = request.query_params['emp_id']
            count, obj = User.objects.filter(emp_id=emp_id).delete()
        elif request.query_params.__contains__('id'):
            user_id = request.query_params['id']
            count, obj = User.objects.filter(id=user_id).delete()
        else:
            return Response({'msg': 'Keys not sufficed'}, 406)

        # Deletion of an object returns the count on index 0
        return Response({'count': count, 'obj_related': obj})


class GetUserAPI(APIView):

    def get(self, request):
        if request.query_params.__contains__('emp_id'):
            emp_id = request.query_params['emp_id']
            obj = User.objects.filter(emp_id=emp_id)
        elif request.query_params.__contains__('id'):
            user_id = request.query_params['id']
            obj = User.objects.filter(id=user_id)
        else:
            return Response({'msg': 'Keys not sufficed'}, 406)

        # Deletion of an object returns the count on index 0
        return Response(obj.values())


# Retrieval APIs of all devices per category
class AvailableDevicesAPI(APIView):

    def get(self, request):
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
            available_devices = modelhelper.get_all_available_devices(int(limit), int(offset))
            return Response(available_devices)
        except:
            pass

        available_devices = modelhelper.get_all_available_devices()
        return Response(available_devices)


class BorrowedDevicesAPI(APIView):

    def get(self, request):
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
            borrowed_devices = modelhelper.get_all_borrowed_devices(int(limit), int(offset))
            return Response(borrowed_devices)
        except:
            pass

        borrowed_devices = modelhelper.get_all_borrowed_devices()
        return Response(borrowed_devices)


class DevicesAPI(APIView):

    def get(self, request):
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
            devices = modelhelper.get_all_devices(int(limit), int(offset))
            return Response(devices)
        except:
            pass

        devices = modelhelper.get_all_devices()
        return Response(devices)


# Specialized device APIs
class BorrowDevicesAPI(APIView):

    def get(self, request):
        try:
            # validate the staff first
            staff_emp_id = request.query_params['staff_emp_id']
        except:
            return Response({'msg': 'staff_emp_id not sufficed'}, 406)

        if not is_staff_authorized(staff_emp_id):
                return Response({'msg': 'Not authorized user'}, 406)

        device_fields = ['id', 'name', 'barcode', 'serial_no', 'service_tag']
        device_kwargs = get_match(request.query_params, device_fields)
        if device_kwargs:
            device_kwargs = device_kwargs[0]
        else:
            return Response({'msg': 'Please provide device key: ' + ','.join(device_fields)}, 406)

        user_fields = ['borrower_id', 'borrower_emp_id', 'borrower_name']
        borrower_kwargs = get_match(request.query_params, user_fields)
        if borrower_kwargs:
            borrower_kwargs = borrower_kwargs[0]
        else:
            return Response({'msg': 'Please provide user key: ' + ','.join(user_fields)}, 406)

        try:
            to_which_project = request.query_params['to_which_project']
        except:
            return Response({'msg': 'to_which_project field not sufficed'}, 406)

        try:
            expected_return_date = request.query_params['expected_return_date']
            if not expected_return_date:
                raise
        except:
            expected_return_date = timezone.now

        query = modelhelper.transact_borrow_device(
            device_kwargs=device_kwargs,
            user_kwargs=borrower_kwargs,
            staff_kwargs={'emp_id': staff_emp_id},
            to_which_project=to_which_project,
            expected_return_date=expected_return_date,
        )

        return Response(query)


class ReturnDevicesAPI(APIView):

    def get(self, request):
        try:
            staff_emp_id = request.query_params['staff_emp_id']
            if not is_staff_authorized(staff_emp_id):
                raise
        except:
            return Response({'msg': 'Not authorized user'}, 406)

        device_fields = ['id', 'name', 'barcode', 'serial_no', 'service_tag']
        device_kwargs = get_match(request.query_params, device_fields)
        if device_kwargs:
            device_kwargs = device_kwargs[0]
        else:
            return Response({'msg': 'Please provide device key: ' + ','.join(device_fields)})

        previous_device = modelhelper.get_instance_device(device_kwargs)

        try:
            health = request.query_params['health']
            if not health:
                raise
        except:
            health = previous_device.status.health

        try:
            notes = request.query_params['notes']
            if not notes:
                raise
        except:
            notes = previous_device.status.notes

        try:
            barcode = request.query_params['barcode']
            if not barcode:
                raise
        except:
            barcode = previous_device.status.barcode

        try:
            location = request.query_params['location']
            if not location:
                raise
        except:
            location = previous_device.status.location.location

        try:
            transaction_date = request.query_params['transaction_date']
            if not transaction_date:
                raise
        except:
            transaction_date = timezone.now

        try:
            image = request.query_params['image']
            if not image:
                raise

            image = base64.base64decode(imagedata)
        except:
            image = previous_device.status.image

        try:
            is_available = request.query_params['is_available']
            if not is_available:
                raise
        except:
            is_available = previous_device.status.is_available

        query = modelhelper.transact_return_device(
            device_kwargs=device_kwargs,
            staff_kwargs={'emp_id': staff_emp_id},
            health=health,
            notes=notes,
            image=image,
            is_available=is_available,
            barcode=barcode,
            location=location,
            transaction_date=transaction_date,
        )

        return Response(query)


class UpdateDevicesAPI(APIView):

    def get(self, request):
        try:
            staff_emp_id = request.query_params['staff_emp_id']
        except:
            return Response({'msg': 'Key "staff_emp_id" not sufficed'}, 406)

        if not is_staff_authorized(staff_emp_id):
            return Response({'msg': 'Unauthorized staff access.'}, 406)

        try:
            device_id = request.query_params['id']
        except:
            return Response({'msg': 'Device `id` not sufficed'}, 406)

        try:
            barcode = request.query_params['barcode']
        except:
            return Response({'msg': 'Key "barcode" not sufficed'}, 406)

        try:
            category = request.query_params['category']
        except:
            return Response({'msg': 'Key "category" not sufficed'}, 406)

        try:
            health = request.query_params['health']
            if not health:
                raise
        except:
            health = 'Functional'

        try:
            image = request.query_params['image']
            if not image:
                raise

            image = base64.base64decode(imagedata)
        except:
            image = None

        try:
            is_available = request.query_params['is_available']
            if not is_available:
                raise
            is_available = True if is_available.lower() == 'true' else False
        except:
            is_available = True

        location_fields = ['location_id', 'location']
        location_kwargs = get_match(request.query_params, location_fields)
        if location_kwargs:
            location_kwargs = location_kwargs[0]
        else:
            return Response({'msg': 'Key "location" not sufficed'}, 406)

        try:
            model = request.query_params['model']
        except:
            return Response({'msg': 'Key "model" not sufficed'}, 406)

        try:
            notes = request.query_params['notes']
        except:
            notes = ''

        try:
            serial_no = request.query_params['serial_no']
        except:
            return Response({'msg': 'Key "serial_no" not sufficed'}, 406)

        try:
            service_tag = request.query_params['service_tag']
        except:
            return Response({'msg': 'Key "service_tag" not sufficed'}, 406)

        try:
            transaction_date = request.query_params['transaction_date']
            if not transaction_date:
                raise
        except:
            transaction_date = timezone.now

        transaction =  modelhelper.transact_modify_device(
            staff_kwargs={'emp_id': staff_emp_id},
            location_kwargs=location_kwargs,
            device_id=device_id,
            barcode=barcode,
            category=category,
            health=health,
            image=image,
            is_available=is_available,
            model=model,
            notes=notes,
            serial_no=serial_no,
            service_tag=service_tag,
            transaction_date=transaction_date,
        )

        return Response(transaction)


class AddDeviceAPI(APIView):

    def get(self, request):
        try:
            staff_emp_id = request.query_params['staff_emp_id']
        except:
            return Response({'msg': 'Key "staff_emp_id" not sufficed'}, 406)

        if not is_staff_authorized(staff_emp_id):
            return Response({'msg': 'Unauthorized staff access.'}, 406)

        try:
            barcode = request.query_params['barcode']
        except:
            return Response({'msg': 'Key "barcode" not sufficed'}, 406)

        if modelhelper.is_barcode_existed(barcode):
            return Response({'msg': 'Barcode already exists'}, 406)

        try:
            category = request.query_params['category']
        except:
            return Response({'msg': 'Key "category" not sufficed'}, 406)

        try:
            health = request.query_params['health']
            if not health:
                raise
        except:
            health = 'Functional'

        try:
            imagedata = request.query_params['image']
            if not image:
                raise

            # Process passed base64 image
            image = base64.base64decode(imagedata)
        except:
            image = None

        try:
            is_available = request.query_params['is_available']
            if not is_available:
                raise
            is_available = True if is_available.lower() == 'true' else False
        except:
            is_available = True

        location_fields = ['location_id', 'location']
        location_kwargs = get_match(request.query_params, location_fields)
        if location_kwargs:
            location_kwargs = location_kwargs[0]
        else:
            return Response({'msg': 'Key "location" not sufficed'}, 406)

        try:
            model = request.query_params['model']
        except:
            return Response({'msg': 'Key "model" not sufficed'}, 406)

        try:
            notes = request.query_params['notes']
        except:
            notes = ''

        try:
            serial_no = request.query_params['serial_no']
        except:
            return Response({'msg': 'Key "serial_no" not sufficed'}, 406)

        if modelhelper.is_serial_no_existed(serial_no):
            return Response({'msg': 'Serial Number already existed'}, 406)

        try:
            service_tag = request.query_params['service_tag']
        except:
            return Response({'msg': 'Key "service_tag" not sufficed'}, 406)

        if modelhelper.is_service_tag_existed(service_tag):
            return Response({'msg': 'Key Service Tag already existed'}, 406)

        try:
            transaction_date = request.query_params['transaction_date']
            if not transaction_date:
                raise
        except:
            transaction_date = timezone.now

        device = modelhelper.transact_add_device(
            staff_kwargs={'emp_id': staff_emp_id},
            location_kwargs=location_kwargs,
            barcode=barcode,
            category=category,
            health=health,
            image=image,
            is_available=is_available,
            model=model,
            notes=notes,
            serial_no=serial_no,
            service_tag=service_tag,
            transaction_date=transaction_date,
        )

        return Response(device)


class DeleteDevicesAPI(APIView):

    def get(self, request):
        return Response('not yet supported')


class GetDevice(APIView):

    def get(self, request):
        if request.query_params.__contains__('id') and request.query_params['id']:
            device_kwargs = {'id': request.query_params['id']}
        elif request.query_params.__contains__('barcode') and request.query_params['barcode']:
            device_kwargs = {'barcode': request.query_params['barcode']}
        elif request.query_params.__contains__('serial_no') and request.query_params['serial_no']:
            device_kwargs = {'serial_no': request.query_params['serial_no']}
        elif request.query_params.__contains__('service_tag') and request.query_params['service_tag']:
            device_kwargs = {'service_tag': request.query_params['service_tag']}
        else:
            return Response({'msg': 'No Device field sufficed: [id, barcode, serial_no, service_tag]'}, 406)

        try:
            device_obj = modelhelper.get_instance_device(device_kwargs)
            if not device_obj:
                raise
        except:
            return Response([])

        device = Device.objects.filter(id=device_obj.id).values(
            'id',
            'category__category',
            'serial_no',
            'service_tag',
            'model',
            'status__id',
            'status__health',
            'status__image',
            'status__is_available',
            'status__notes',
            'status__barcode',
            'status__location__location',
        )

        return Response(device[0])


class SearchDevices(APIView):

    def get(self, request):
        try:
            keyword = request.query_params['keyword']
        except:
            return Response({'msg': '`keyword` not sufficed'}, 406)

        device = modelhelper.search_device(keyword)
        return Response(device)


class CategoriesList(APIView):

    def get(self, request):
        categories = modelhelper.get_all_categories()
        return Response(categories)


class LocationsList(APIView):
    def get(self, request):
        locations = modelhelper.get_all_locations()
        return Response(locations)


class TransactionsRetriever(APIView):
    def get(self, request):
        transaction_id = 0
        try:
            transaction_id = request.query_params['id']
        except:
            pass
        transactions = modelhelper.get_all_transactions(transaction_id)

        return Response(transactions)
        # return Response({'msg': 'oh'})


class Home(View):

    def get(self, request):
        devices = modelhelper.get_all_devices()
        search_form = SearchForm()

        try:
            keyword = request.GET['keyword']
            searched_devices = modelhelper.search_device(keyword)
        except:
            searched_devices = []

        return render(request, 'bulkdevices/devices.html', {
            'devices': devices,
            'searched_devices': searched_devices,
            'search_form': search_form,
            }
        )


class BorrowedDevicesList(View):

    def get(self, request):
        devices = modelhelper.get_all_borrowed_devices()
        return render(request, 'bulkdevices/borroweddevices.html', {'devices': devices})


class DevicesUnique(View):

    def get(self, request):
        devices = modelhelper.get_all_devices_uniquely_by_name()
        return render(request, 'bulkdevices/uniquedevices.html', {'devices': devices})


class AvailableDevicesList(View):

    def get(self, request):
        devices = modelhelper.get_all_available_devices()
        return render(request, 'bulkdevices/availabledevices.html', {'devices': devices})


class GetAllAndManageDevices(View):

    def get(self, request, form_errors=''):
        borrow_form = BorrowForm()
        add_category_form = AddCategoryForm()
        add_device_form = AddDeviceForm()
        add_location_form = AddLocationForm()
        add_status_form = AddStatusForm()
        search_form = SearchForm()

        try:
            keyword = request.GET['keyword']
            searched_devices = modelhelper.search_device(keyword)
        except Exception as e:
            searched_devices = []

        devices = modelhelper.get_all_devices()

        return render(request, 'device/managedevices.html', {
            'devices': devices,
            'searched_devices': searched_devices,
            'borrow_form': borrow_form,
            'add_category_form': add_category_form,
            'add_device_form': add_device_form,
            'add_location_form': add_location_form,
            'add_status_form': add_status_form,
            'search_form': search_form,
            'form_errors': form_errors,
        })


def redirect_to_borrow_page(request, pk):
    form = BorrowForm()
    return render(request, 'device/borrowdevice.html', {'pk': pk, 'form': form})

def redirect_to_modify_page(request, device_pk, status_pk):
    device = Device.objects.get(pk=device_pk)
    status = Status.objects.get(pk=status_pk)
    device_form = AddDeviceForm(
        initial={
            'category': device.category,
            'serial_no': device.serial_no,
            'service_tag': device.service_tag,
            'model': device.model,
        }
    )
    status_form = ModifyStatusForm(
        initial={
            'health': status.health,
            'notes': status.notes,
            'barcode': status.barcode,
            'image': status.image,
            'is_available': status.is_available,
            'location': status.location,
        }
    )
    return render(
        request,
        'device/modifydevice.html', {
            'device_form': device_form,
            'status_form': status_form,
            'pk': device_pk,
        }
    )


def redirect_to_return_page(request, pk, status_pk):
    status = Status.objects.get(pk=status_pk)
    form = ReturnForm(initial={
        'health': status.health,
        'notes': status.notes,
        'barcode': status.barcode,
        'image': status.image,
        'is_available': True,
        'location': status.location,
    })
    return render(request, 'device/returndevice.html', {'pk': pk, 'form': form})


def delete_device(request, pk):
    Device.objects.get(pk=pk).delete()

    return redirect('manage_devices')


class AddDevice(View):
    def post(self, request):
        add_device_form = AddDeviceForm(request.POST)
        add_status_form = AddStatusForm(request.POST, request.FILES)

        if add_device_form.is_valid() and add_status_form.is_valid():

            # Prepare the model but don't commit/send it to the database yet
            device = add_device_form.save(commit=False)

            # Assign with the foreign key field
            device.status = add_status_form.save()

            # Save for real
            saved_device = device.save()

            staff_obj = Staff.objects.get(emp_id=request.session['emp_id'])
            device_obj = Device.objects.get(id=device.id)
            transaction_type, is_created = TransactionType.objects.update_or_create(transaction_type=3)
            Transaction.objects.create(
                staff=staff_obj,
                device=device_obj,
                transaction_type=transaction_type,
                status=device_obj.status,
                transaction_date=timezone.now,
            )
            return redirect('manage_devices')
        return redirect('manage_devices', kwargs={'form_errors': add_device_form.errors.update(add_status_form.errors)})


class AddCategory(View):
    def post(self, request):
        add_category_form = AddCategoryForm(request.POST)
        if add_category_form.is_valid():
            add_category_form.save()
            return redirect('manage_devices')
        return redirect('manage_devices', {'form_errors': add_category_form.errors})


class AddLocation(View):
    def post(self, request):
        add_location_form = AddLocationForm(request.POST)
        if add_location_form.is_valid():
            add_location_form.save()
            return redirect('manage_devices')
        return redirect('manage_devices', {'form_errors': add_location_form.errors})


class BorrowDevice(View):

    def post(self, request, pk):
        form = BorrowForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['borrower']
            to_which_project = form.cleaned_data['to_which_project']
            expected_return_date = form.cleaned_data['expected_return_date']
            query_response = modelhelper.transact_borrow_device(
                device_kwargs={'id': pk},
                staff_kwargs={'emp_id': request.session['emp_id']},
                user_kwargs={'emp_id': user.emp_id},
                to_which_project=to_which_project,
                expected_return_date=expected_return_date,
            )
            return redirect('manage_devices')

        return redirect('borrow_device')


class ReturnDevice(View):

    def post(self, request, pk):
        form = ReturnForm(request.POST)
        if form.is_valid():
            health = form.cleaned_data['health']
            notes = form.cleaned_data['notes']

            # image = form.cleaned_data['image']
            is_available = form.cleaned_data['is_available']
            barcode = form.cleaned_data['barcode']
            location = form.cleaned_data['location']

            modelhelper.transact_return_device(
                device_kwargs={'id': pk},
                staff_kwargs={'emp_id': request.session['emp_id']},
                health=health,
                notes=notes,
                image='',
                is_available=is_available,
                barcode=barcode,
                location=location,
                transaction_date=timezone.now
            )
            return redirect('manage_devices')
        return redirect('manage_devices', form_errors=form.errors)


class ModifyDevice(View):

    def post(self, request):
        device_form = ModifyDeviceForm(request.POST)
        status_form = ModifyStatusForm(request.POST, request.FILES)

        device_id = request.POST.get('device_id')

        if device_form.is_valid() and status_form.is_valid():
            category = device_form.cleaned_data['category']
            model = device_form.cleaned_data['model']
            serial_no = device_form.cleaned_data['serial_no']
            service_tag = device_form.cleaned_data['service_tag']

            health = status_form.cleaned_data['health']
            notes = status_form.cleaned_data['notes']
            barcode = status_form.cleaned_data['barcode']
            location = status_form.cleaned_data['location']
            image = status_form.cleaned_data['image']
            is_available = status_form.cleaned_data['is_available']

            modelhelper.transact_modify_device(
                staff_kwargs={'emp_id': request.session['emp_id']},
                location_kwargs={'location': location},
                device_id=device_id,
                barcode=barcode,
                category=category,
                health=health,
                image=image,
                is_available=is_available,
                model=model,
                notes=notes,
                serial_no=serial_no,
                service_tag=service_tag,
                transaction_date=timezone.now(),
            )
            return redirect('manage_devices')

        return redirect('manage_devices', form_errors=device_form.errors + status_form.errors)


class Users(View):

    def get(self, request):
        users = modelhelper.get_all_users()
        return render(request, 'staff/users.html', {'users': users})


def delete_user(request, pk):
    User.objects.get(pk=pk).delete()
    return redirect('users')


class Staffs(View):

    def get(self, request):
        staffs = modelhelper.get_all_staffs()
        return render(request, 'staff/staffs.html', {'staffs': staffs})


def delete_staff(request, pk):
    Staff.objects.get(pk=pk).delete()
    return redirect('staffs')


class Teams(View):
    def get(self, request):
        teams = modelhelper.get_all_teams()
        return render(request, 'staff/teams.html', {'teams': teams})


class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        loginform = LoginForm(request.POST)

        error_msg = ''
        if loginform.is_valid():
            emp_id = loginform.cleaned_data['emp_id']  # Gets cleaned data submitted by the form

            staff = get_staff(emp_id)
            if staff:
                staff = modelhelper.get_instance_staff({'emp_id': staff.emp_id})
                request.session.update({
                    'id': staff.id,
                    'emp_id': staff.emp_id,
                    'name': staff.name,
                })
                request.session.pop('date_added')
            else:
                loginform = LoginForm()
                error_msg = 'Staff does not exist.'

                return render(request, 'login.html', {'form': loginform, 'error_msg': error_msg})

        else:
            return render(request, 'login.html', {'form': loginform})

        return redirect('home')


class Logout(View):

    def get(self, request):
        try:
            del request.session['emp_id']
        except KeyError:
            pass

        return redirect('home')


class DownloadReport(View):
    def get(self, request):
        report = Report()
        return report.download
        # return redirect('manage_devices')


def is_staff_authorized(emp_id):
    return bool(Staff.objects.filter(emp_id=emp_id))


def get_staff(emp_id):
    return Staff.objects.filter(emp_id=emp_id).first()


def is_staff_logged_in(request):
    return bool(request.session['emp_id'])

def get_match(dict_to_iterrate, list_of_keywords):
    return [{key: value} for key, value in dict_to_iterrate.items() if key in list_of_keywords]

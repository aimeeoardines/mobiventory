from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    url(r'^api/staff/add/', views.AddStaffAPI.as_view()),
    url(r'^api/staff/delete/', views.DeleteStaffAPI.as_view()),
    url(r'^api/staff/update/', views.UpdateStaffAPI.as_view()),
    url(r'^api/staff/get/', views.GetStaffAPI.as_view()),
    url(r'^api/staff/validate/', views.ValidateStaffAPI.as_view()),
    url(r'^api/staff/transactions/', views.GetStaffTransactions.as_view()),

    # API for user accounts
    url(r'^api/users/', views.GetAllUsers.as_view()),
    url(r'^api/user/add/', views.AddUserAPI.as_view()),
    url(r'^api/user/update/', views.UpdateUserAPI.as_view()),
    url(r'^api/user/delete/', views.DeleteUserAPI.as_view()),
    url(r'^api/user/get/', views.GetUserAPI.as_view()),

    # API urls that would return all device based on specification
    url(r'^api/devices/available/', views.AvailableDevicesAPI.as_view()),
    url(r'^api/devices/borrowed/', views.BorrowedDevicesAPI.as_view()),
    url(r'^api/devices/', views.DevicesAPI.as_view()),

    # API urls that would possibly process a single device
    url(r'^api/borrow-device/', views.BorrowDevicesAPI.as_view()),
    url(r'^api/return-device/', views.ReturnDevicesAPI.as_view()),
    url(r'^api/update-device/', views.UpdateDevicesAPI.as_view()),
    url(r'^api/add-device/', views.AddDeviceAPI.as_view()),
    url(r'^api/delete-device/', views.DeleteDevicesAPI.as_view()),
    url(r'^api/get-device/', views.GetDevice.as_view()),
    url(r'^api/search-device/', views.SearchDevices.as_view()),

    url(r'^api/categories/', views.CategoriesList.as_view()),
    url(r'^api/locations/', views.LocationsList.as_view()),

    url(r'^api/shit/', views.TransactionsRetriever.as_view(), name='transactions-retriever'),

    # Add your urls below
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^availablelist/', views.AvailableDevicesList.as_view(), name='available_devices_list'),
    url(r'^borrowlist/', views.BorrowedDevicesList.as_view(), name='borrowed_devices_list'),

    url(r'^manage-devices/', views.GetAllAndManageDevices.as_view(), name='manage_devices'),
    url(r'^manage-devices/(?P<form_errors>.+)', views.GetAllAndManageDevices.as_view(), name='manage_devices'),
    url(r'^device-add', views.AddDevice.as_view(), name='device_add'),
    url(r'^borrow-redirect/(?P<pk>\d+)', views.redirect_to_borrow_page, name='redirect_to_borrow_page'),
    url(r'^modify-device/(?P<device_pk>\d+)/(?P<status_pk>\d+)', views.redirect_to_modify_page, name='redirect_to_modify_page'),
    url(r'^return-redirect/(?P<pk>\d+)/(?P<status_pk>\d+)', views.redirect_to_return_page, name='redirect_to_return_page'),
    url(r'^borrow-device/(?P<pk>\d+)', views.BorrowDevice.as_view(), name='borrow_device'),
    url(r'^return-device/(?P<pk>\d+)', views.ReturnDevice.as_view(), name='return_device'),
    url(r'^modify-device/', views.ModifyDevice.as_view(), name='modify_device'),
    url(r'^delete-device/(?P<pk>\d+)', views.delete_device, name='delete_device'),
    url(r'^category-add/', views.AddCategory.as_view(), name='category_add'),
    url(r'^location-add/', views.AddLocation.as_view(), name='location_add'),

    url(r'^staffs/delete/(?P<pk>\d+)', views.delete_staff, name='deletestaff'),
    url(r'^users/delete/(?P<pk>\d+)', views.delete_user, name='deleteuser'),
    url(r'^users/', views.Users.as_view(), name='users'),
    url(r'^staffs/', views.Staffs.as_view(), name='staffs'),
    url(r'^teams/', views.Teams.as_view(), name='teams'),

    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/', views.Logout.as_view(), name='logout'),

    url(r'^report/', views.DownloadReport.as_view(), name='report')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django import forms

from .models import Category, Device, Location, Staff, Status, User


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'emp_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Employee ID',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Staff Name',
            }),
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AddDeviceForm(forms.ModelForm):
     class Meta:
        model = Device
        fields = '__all__'
        exclude = ['status']


class AddLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class AddStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'
        exclude = ['is_available']


class ModifyStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class ModifyDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class LoginForm(forms.Form):

    emp_id = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Employee ID',
    }), label='')


class BorrowForm(forms.Form):

    # Change this to query from Users table
    borrower = forms.ModelChoiceField(
        label='Borrower',
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    to_which_project = forms.CharField(
        label='To which project',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    expected_return_date = forms.DateField(
        label='Expected return date',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class SearchForm(forms.Form):
    keyword = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Search'
            }
        )
    )

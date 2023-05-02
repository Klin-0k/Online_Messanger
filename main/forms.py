from django import forms

from .models import User, Message


class CreateUserForm(forms.ModelForm):
    Terms = forms.BooleanField(required=False)
    ConfirmPassword = forms.CharField()

    class Meta:
        model = User
        fields = ['FirstName', 'SecondName', 'UserName', 'Email', 'Birthday', 'Password']
        widgets = {
            'Password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if not User.is_valid_name(cleaned_data.get('FirstName')):
            self.add_error('FirstName', 'This is not valid first name')
        if not User.is_valid_name(cleaned_data.get('SecondName')):
            self.add_error('SecondName', 'This is not valid second name')
        if User.objects.filter(UserName=cleaned_data.get('UserName')).exists():
            self.add_error('UserName', 'This username is already taken!')
        if not User.is_valid_username(cleaned_data.get('UserName')):
            self.add_error('UserName', User.username_rules_description())
        if User.objects.filter(Email=cleaned_data.get('Email')).exists():
            self.add_error('Email', 'User with this Email already exists!')
        if cleaned_data.get('Password') != cleaned_data.get('ConfirmPassword'):
            if cleaned_data.get('ConfirmPassword'):
                self.add_error('ConfirmPassword', 'Your passwords didn\'t match!')
        if not cleaned_data.get('Terms'):
            self.add_error('Terms', 'You must agree with terms!')


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['UserName', 'Password']
        widgets = {
            'Password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if not User.objects.filter(UserName=cleaned_data.get('UserName')).exists():
            if cleaned_data.get('UserName'):
                self.add_error('UserName', 'User with this username does not exist!')
        else:
            user = User.objects.get(UserName=cleaned_data.get('UserName'))
            if not user.Password == cleaned_data.get('Password'):
                if cleaned_data.get('Password'):
                    self.add_error('Password', 'Wrong password')


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['Text']

    def clean(self):
        cleaned_data = super().clean()
        if not User.objects.filter(UserName=cleaned_data.get('Recipient')).exists():
            if cleaned_data.get('Recipient'):
                self.add_error('Recipient', 'User with this username does not exist!')


class ChangeProfileForm(forms.ModelForm):

    def __init__(self, current_user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    current_user = None
    CurrentPassword = forms.CharField(required=False)
    NewPassword = forms.CharField(required=False)
    ConfirmPassword = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['FirstName', 'SecondName', 'UserName', 'Email', 'Birthday']

    def clean(self):
        cleaned_data = super().clean()
        if not User.is_valid_name(cleaned_data.get('FirstName')):
            self.add_error('FirstName', 'This is not valid first name')
        if not User.is_valid_name(cleaned_data.get('SecondName')):
            self.add_error('SecondName', 'This is not valid second name')
        if not User.is_valid_username(cleaned_data.get('UserName')):
            self.add_error('UserName', User.username_rules_description())
        if User.objects.filter(
                UserName=cleaned_data.get('UserName')).exists() and self.current_user.UserName != cleaned_data.get(
                'UserName'):
            self.add_error('UserName', 'This username is already taken!')
        if User.objects.filter(
                Email=cleaned_data.get('Email')).exists() and self.current_user.Email != cleaned_data.get('Email'):
            self.add_error('Email', 'User with this Email already exists!')
        if cleaned_data.get('CurrentPassword') or cleaned_data.get('NewPassword') or cleaned_data.get('ConfirmPassword'):
            if self.current_user.Password != cleaned_data.get(
                    'CurrentPassword'):
                self.add_error('CurrentPassword', 'Wrong password!')
            else:
                if not cleaned_data.get('NewPassword'):
                    self.add_error('NewPassword', 'This field is requirement.')
            if cleaned_data.get('NewPassword') != cleaned_data.get('ConfirmPassword'):
                self.add_error('ConfirmPassword', 'Your passwords didn\'t match!')

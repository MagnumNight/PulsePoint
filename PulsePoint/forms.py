from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("That email address is already registered.")
        return email

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField()

    username = forms.CharField(
        max_length=150,
        help_text="",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    current_password = forms.CharField(
        label="Current password", widget=forms.PasswordInput, required=False
    )
    new_password1 = forms.CharField(
        label="New password", widget=forms.PasswordInput, required=False
    )
    new_password2 = forms.CharField(
        label="Confirm new password", widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "current_password",
            "new_password1",
            "new_password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        # Check if the username has changed
        if username != self.instance.username:
            if (
                User.objects.filter(username=username)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise forms.ValidationError("That username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Check if the email has changed
        if email != self.instance.email:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("That email already exists.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Check if user wants to change the password
        if current_password or new_password1 or new_password2:
            if not self.instance.check_password(current_password):
                self.add_error("current_password", "Incorrect current password")
            if new_password1 != new_password2:
                self.add_error("new_password2", "Passwords do not match")

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Project


class CustomRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label="Full name")
    email = forms.EmailField()
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial="user",
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "full_name", "email", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["full_name"]
        user.email = self.cleaned_data["email"]
        selected_role = self.cleaned_data["role"]
        user.role = selected_role
        user.is_staff = selected_role == "admin"
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial="user",
        label="Sign in as",
    )


class UploadForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("file_type", "file", "link_url")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        file_type = cleaned.get("file_type")
        file = cleaned.get("file")
        link = cleaned.get("link_url")

        if file_type in {"image", "video"} and not file:
            raise forms.ValidationError("Please attach a file for image/video uploads.")
        if file_type == "link" and not link:
            raise forms.ValidationError("Please include the URL for link uploads.")

        if file_type in {"image", "video"}:
            if not getattr(self.instance, "idea", None):
                if file:
                    self.instance.idea = file.name
                else:
                    self.instance.idea = "Untitled evidence"
            self.instance.description = ""
        elif file_type == "link":
            if not getattr(self.instance, "idea", None):
                self.instance.idea = cleaned.get("link_url") or "Link submission"
        return cleaned




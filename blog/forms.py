from django import forms
from.models import PhotoSubmission

class ExampleSignupForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(
        label='Gender',
        required=False,
        choices=[
            (None, '-------'),
            ('m', 'Male'),
            ('f', 'Female'),
            ('n', 'Non-binary'),
        ]
    )
    receive_newsletter = forms.BooleanField(
        required=False,
        label='Do you wish to receive our newsletter?'
    )

class PhotoSubmissionForm(forms.ModelForm):
    """
    Form for users to submit their photo contest entry.
    We use ModelForm here because:
    - It automatically generates form fields from the PhotoSubmission model
    - It simplifies validation and saving to the database
    - It avoids manual duplication of model logic

    """

    class Meta:
        # Connect the form to the PhotoSubmission model
        model = PhotoSubmission

        # Include these specific model fields in the form
        fields = ['first_name', 'last_name', 'email', 'image']
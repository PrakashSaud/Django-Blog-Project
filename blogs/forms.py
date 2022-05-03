from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea, required=True)
    sender = forms.EmailField(required=True)
    cc_myself = forms.BooleanField(required=False)
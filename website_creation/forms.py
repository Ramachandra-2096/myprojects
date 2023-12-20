from django import forms
class lang_selection(forms.Form):
    LANGUAGE_CHOICES = [('en', 'English'),('es', 'Española'),('de', 'Deutsch')]
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label='Select Language')
    

class submit_form(forms.Form):
    name = forms.CharField(label="College Name",max_length=250, required=True)
    template = forms.FileField(required=True)
    file = forms.FileField(required=True) 
    
    
from django import forms
from .models import ExcelDocument
#%%
class ExcelForm(forms.ModelForm):
    class Meta:
        model = ExcelDocument
        fields = ('upload',)

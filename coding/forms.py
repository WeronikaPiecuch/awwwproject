from django import forms
from .sdcc_options import *

class StandardForm(forms.Form):
    legend = "Wybierz standard kodu źródłowego:"
    standard = forms.ChoiceField(widget=forms.RadioSelect, choices=STANDARD_CHOICES)

class OptymalizacjeForm(forms.Form):
    legend = "Wybierz optymalizacje:"
    optymalizacje = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTYMALIZACJE_CHOICES, required=False)

class ProcesorForm(forms.Form):
    legend = "Wybierz procesor:"
    procesor = forms.ChoiceField(widget=forms.RadioSelect, choices=PROCESOR_CHOICES)

class MCS51Form(forms.Form):
    legend = "Wybierz opcje dla procesora MCS51:"
    mcs51 = forms.ChoiceField(widget=forms.RadioSelect, choices=MCS51_CHOICES)

class Z80Form(forms.Form):
    legend = "Wybierz opcje dla procesora Z80:"
    z80 = forms.ChoiceField(widget=forms.RadioSelect,choices=Z80_CHOICES)

class STM8Form(forms.Form):
    legend = "Wybierz opcje dla procesora STM8:"
    stm8 = forms.ChoiceField(widget=forms.RadioSelect, choices=STM8_CHOICES)

class FileUploadForm(forms.Form):
    file_name = forms.CharField(label='Nazwa pliku (opcjonalnie)', max_length=100, required=False, widget = forms.TextInput( attrs={'id': 'file_name'}))
    file = forms.FileField(label='Plik', widget = forms.FileInput( attrs={'class': 'file-input', 'accept': '.c', 'id': 'file_src'}))    

class FolderUploadForm(forms.Form):
    folder_name = forms.CharField(label='Nazwa folderu', max_length=100, widget = forms.TextInput( attrs={'id': 'folder_name'}))

class SectionUploadForm(forms.Form):
    section_name = forms.CharField(label='Nazwa sekcji', max_length=100, widget = forms.TextInput( attrs={'id': 'section_name'}), required=False)
    section_type = forms.CharField(label='Typ sekcji', max_length=100, widget = forms.TextInput( attrs={'id': 'section_type'}))
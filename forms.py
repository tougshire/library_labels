from django import forms
from django.urls import reverse_lazy

from touglates.widgets import TouglatesRelatedSelect
from .models import InsertTemplate

class BarcodeForm(forms.Form):
    CODE_CHOICES=[
        ("A","A"),
        ("B","B"),
        ("C","C"),
        ("D","D"),
    ]

    barcode_number = forms.CharField(label="barcode")
    show_barcode_number = forms.BooleanField(label="show barcode", required=False, initial=True )
    show_startstop = forms.BooleanField(label="show start/stop", required=False, initial=False )
    start_code = forms.ChoiceField(label="start_code", choices=CODE_CHOICES, initial="A")
    stop_code = forms.ChoiceField(label="stop_code", choices=CODE_CHOICES, initial="B")
    above_bar1_text = forms.CharField(label="Text line 1", max_length=60, required=False, initial="SUFFOLK PUBLIC LIBRARY")
    above_bar2_text = forms.CharField(label="Text line 2", max_length=60, initial="SUFFOLK, VA")
    barcode_height = forms.IntegerField(label="Barcode height",initial="400")
    barcode_width = forms.IntegerField(label="Barcode width",initial="2800")
    barcode_fontsize = forms.IntegerField(label="Barcode size",initial="128")
    barcode_fontfamily = forms.CharField(label="Barcode family", max_length=60, initial="LiberationSans-Regular.ttf")
    above_bar1_fontsize = forms.IntegerField(label="Text line 1 size",initial=96)
    above_bar2_fontsize = forms.IntegerField(label="Text line 2 size",initial=96)
    above_bar1_fontfamily = forms.CharField(label="Text line family", max_length=60, initial="LiberationSans-Bold.ttf")
    above_bar2_fontfamily = forms.CharField(label="Text line family", max_length=60, initial="LiberationSans-Bold.ttf")


class SSIDForm(forms.Form):
   ssid_text = forms.CharField(label="SSID", max_length=30)
   password_text = forms.CharField(label="Password", max_length=30)
   notice1_text = forms.CharField(label="Notice(line 1)", max_length=50, required=False, initial="Return with case, carger, and cable")
   notice2_text = forms.CharField(label="Notice(line 2)", max_length=50, required=False, initial="")
   ssid_fontsize = forms.IntegerField(label="SSID Font Size", initial=96)
   ssid_fontfamily = forms.CharField(label="SSID Font Family", max_length=60, initial="LiberationSans-Regular.ttf")
   password_fontsize = forms.IntegerField(label="Password Font Size", initial=108)
   password_fontfamily = forms.CharField(label="Password Font Family", max_length=60, initial="LiberationSans-Bold.ttf")
   notice1_fontsize = forms.IntegerField(label="Notice(line 1) Font Size", initial=76)
   notice1_fontfamily = forms.CharField(label="Notice(line 1) Font Family", max_length=60, initial="LiberationSans-Regular.ttf")
   notice2_fontsize = forms.IntegerField(label="Notice(line 2) Font Size", initial=76)
   notice2_fontfamily = forms.CharField(label="Notice(line 2) Font Family", max_length=60, initial="LiberationSans-Regular.ttf")

class InsertTemplateForm(forms.ModelForm):
    class Meta:
        model=InsertTemplate
        fields = [
            'template_title',
            'template_filename',
            'stylesheet_filename'
        ]

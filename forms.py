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
    above_bar1_fontsize = forms.IntegerField(label="Text line 1 size",initial="96")
    above_bar2_fontsize = forms.IntegerField(label="Text line 2 size",initial="96")
    above_bar1_fontfamily = forms.CharField(label="Text line family", max_length=60, initial="LiberationSans-Bold.ttf")
    above_bar2_fontfamily = forms.CharField(label="Text line family", max_length=60, initial="LiberationSans-Bold.ttf")


class InsertTemplateForm(forms.ModelForm):
    class Meta:
        model=InsertTemplate
        fields = [
            'template_title',
            'template_filename',
            'stylesheet_filename'
        ]

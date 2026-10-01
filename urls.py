from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = 'library_labels'
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('library_labels:barcode-create'))),
    path('barcode/create/', views.BarcodeLabelCreate.as_view(), name='barcode-create'),
    path('ssid/create/', views.SSIDLabelCreate.as_view(), name='ssid-create'),

]

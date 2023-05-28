from django import forms
from .models import *
from django.db import transaction
from django.views.generic import UpdateView
from leaflet.forms.widgets import LeafletWidget
from leaflet.forms.fields import *
from django.contrib.gis import forms

class SatSystemForm(forms.ModelForm):
    class Meta:
        model = SatSystem
        fields = "__all__"

class PointSearchForm(forms.ModelForm):
    class Meta:
        model = SearchPoint
        fields = ('name', 'loc')
        geom = forms.PointField()
class MyGeoForm(forms.Form):
    point = forms.PointField(widget=
        forms.OSMWidget(attrs={'map_width': 900, 'map_height': 500}))
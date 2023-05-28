from django.contrib import admin
from django.contrib.gis import admin
# Register your models here.
from .models import *
from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis.admin import OSMGeoAdmin


admin.site.register(Country)
admin.site.register(SpaceAgency)
admin.site.register(SatSystem)
admin.site.register(Satellite)
admin.site.register(Decoder)
admin.site.register(Decoder_antenna)
class TerminalAdmin(LeafletGeoAdmin):
    list_display = ('name', 'map_location')
admin.site.register(Terminal, TerminalAdmin)
class NKUAdmin(LeafletGeoAdmin):
    list_display = ('type', 'map_location')
admin.site.register(NKU, NKUAdmin)
class EarthStationAdmin(LeafletGeoAdmin):
    list_display = ('name', 'map_location')
admin.site.register(EarthStation, EarthStationAdmin)
class SearchPointAdmin(LeafletGeoAdmin):
    list_display = ('name', 'loc')
admin.site.register(SearchPoint, SearchPointAdmin)
class SearchMultiPointAdmin(LeafletGeoAdmin):
    list_display = ('name', 'loc')
admin.site.register(SearchMultiPoint, SearchMultiPointAdmin)

class SearchPoligonAdmin(OSMGeoAdmin):
    list_display = ('name', 'loc')
admin.site.register(SearchPoligon, SearchPoligonAdmin)
class SearchMultiPoligonAdmin(OSMGeoAdmin):
    list_display = ('name', 'loc')
admin.site.register(SearchMultiPoligon, SearchMultiPoligonAdmin)
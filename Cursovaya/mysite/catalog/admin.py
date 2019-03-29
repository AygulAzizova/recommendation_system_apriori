from django.contrib import admin
from. models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Country._meta.fields]
    class Meta:
        model = Country


admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]
    class Meta:
        model = City


admin.site.register(City, CityAdmin)




class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
    class Meta:
        model = Category



admin.site.register(Category, CategoryAdmin)

class HotelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hotel._meta.fields]
    class Meta:
        model = Hotel


admin.site.register(Hotel, HotelAdmin)

class TourAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tour._meta.fields]
    class Meta:
        model = Tour


admin.site.register(Tour, TourAdmin)



class PointAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Point._meta.fields]
    class Meta:
        model = Point


admin.site.register(Point, PointAdmin)

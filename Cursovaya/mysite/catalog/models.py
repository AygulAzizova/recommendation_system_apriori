from django.db import models

class Country(models.Model):
    CountryName = models.CharField(max_length=50)
    def __str__(self):
        return   (self.CountryName)

class City(models.Model):
    CityName = models.CharField(max_length=50)
    def __str__(self):
        return  (self.CityName)


class Category(models.Model):
    CategoryName = models.CharField(max_length=50)
    slug = models.CharField(max_length=200)
    def __str__(self):
        return   (self.CategoryName)

class Hotel(models.Model):
    HotelName = models.CharField(max_length=50)
    HotelStars = models.IntegerField()
    HotelFood = models.CharField(max_length=50)
    def __str__(self):
        return  (self.HotelName)

class Tour(models.Model):
    TourName = models.CharField(max_length=50)
    TourDateStart = models.DateField(auto_now=False, auto_now_add=False)
    TourDateEnd = models.DateField(auto_now=False, auto_now_add=False)
    TourDuration = models.IntegerField()
    ContactCount = models.IntegerField()
    PriceAdult = models.IntegerField()
    PriceChild = models.IntegerField()
    TourCountry = models.ForeignKey(Country,  on_delete = models.CASCADE,)
    TourCategory = models.ForeignKey(Category,  on_delete = models.CASCADE,)
    TourImage = models.ImageField(upload_to='media/catalog')
    Comments= models.TextField()
    slug = models.CharField(max_length=200)









class Point(models.Model):
    PointName = models.CharField(max_length=50)
    PointDuration = models.IntegerField()
    DateArrival = models.DateField(auto_now=False, auto_now_add=False)
    DateDeparture = models.DateField(auto_now=False, auto_now_add=False)
    PointCity = models.ForeignKey(City,  on_delete = models.CASCADE,)
    PointTour = models.ForeignKey(Tour,  on_delete = models.CASCADE,)
    PointHotel = models.ForeignKey(Hotel,  on_delete = models.CASCADE,)
    def __str__(self):
        return  (self.PointName)




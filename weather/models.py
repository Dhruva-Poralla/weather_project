from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class WeatherLog(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    response = models.JSONField(null=True)

    def __str__(self):
        return f"{self.city.name} - {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"

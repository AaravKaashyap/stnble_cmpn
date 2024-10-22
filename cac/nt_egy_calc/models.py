from django.db import models
from django.contrib.auth.models import User

"""
class EnergyUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    square_footage = models.FloatField()
    gas_usage = models.FloatField()
    electricity_usage = models.FloatField()
    total_co2 = models.FloatField()
    net_co2 = models.FloatField()

    def save(self, *args, **kwargs):
        # Calculate total CO2 based on some factors (example: 1 unit of gas = 11.7 pounds of CO2, 1 unit of electricity = 1.22 pounds of CO2)
        self.total_co2 = (self.gas_usage * 11.7) + (self.electricity_usage * 1.22)
        super(EnergyUsage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Energy Usage"
"""
"""from django.db import models
from django.contrib.auth.models import User

class EnergyUsageNew(models.Model):
    square_footage = models.FloatField(default=0)
    gas_usage = models.FloatField(default=0)
    electricity_usage = models.FloatField(default=0)
    net_co2 = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def calculate_co2(self):
        gas_co2 = self.gas_usage * 0.00053
        electricity_co2 = self.electricity_usage * 0.00092
        self.net_co2 = gas_co2 + electricity_co2
        return self.net_co2

    def save(self, *args, **kwargs):
        self.calculate_co2()
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag= models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    post_date = models.DateField(auto_now_add = True)
    def __str__(self):
        return self.title + ' | ' + str(self.author)"""

class Energy(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    square_footage = models.FloatField(default=0)
    gas_usage = models.FloatField(default=0)
    electricity_usage = models.FloatField(default=0)
    miles_driven = models.FloatField(default=0)
    net_co2 = models.FloatField(default=0)


  

    def calculate_co2(self):
        gas_co2 = self.gas_usage * 0.00053
        electricity_co2 = self.electricity_usage * 0.00092
        miles_co2 = self.miles_driven * 0.411  
        self.net_co2 = gas_co2 + electricity_co2
        return self.net_co2

    def save(self, *args, **kwargs):
        self.calculate_co2()
        super().save(*args, **kwargs)

class EnergyNew(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    square_footage = models.FloatField(default=0)
    gas_usage = models.FloatField(default=0)
    electricity_usage = models.FloatField(default=0)
    miles_driven = models.FloatField(default=0)
    net_co2 = models.FloatField(default=0)


  

    def calculate_co2(self):
        gas_co2 = self.gas_usage * 0.00053
        electricity_co2 = self.electricity_usage * 0.00092
        miles_co2 = self.miles_driven * 0.411  
        self.net_co2 = gas_co2 + electricity_co2
        return self.net_co2

    def save(self, *args, **kwargs):
        self.calculate_co2()
        super().save(*args, **kwargs)

class EnergyNew1(models.Model):
    
    square_footage = models.FloatField(default=0)
    gas_usage = models.FloatField(default=0)
    electricity_usage = models.FloatField(default=0)
    miles_driven = models.FloatField(default=0)
    net_co2 = models.FloatField(default=0)


  

    def calculate_co2(self):
        gas_co2 = self.gas_usage * 0.00053
        electricity_co2 = self.electricity_usage * 0.00092
        miles_co2 = self.miles_driven * 0.411  
        self.net_co2 = gas_co2 + electricity_co2
        return self.net_co2

    def save(self, *args, **kwargs):
        self.calculate_co2()
        super().save(*args, **kwargs)

from django.db import models

class UserInput(models.Model):
    question = models.CharField(max_length=255)  # The user's question
    response = models.TextField()  # The ChatGPT (or mock) response
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the question was asked

    def __str__(self):
        return f"Question: {self.question[:50]}..."  # For better admin display




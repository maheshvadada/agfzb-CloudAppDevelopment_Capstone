from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50, default='')
    description = models.CharField(null=False, max_length=50, default='')
    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    CAR_TYPES = (
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "WAGON")
    )
    name = models.CharField(null=False, max_length=50, default='')
    dealer_id = models.IntegerField()
    type = models.CharField(null=False, choices=CAR_TYPES, max_length=10, default='Sedan')
    year = models.DateField(null=True)
    carMake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Dealer Id: " + self.dealer_id + ", " + \
               "Type: " + self.type + ", " + \
               "Year: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

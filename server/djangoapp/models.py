from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):

    maker_name = models.CharField(null=False, max_length=30, default='make')
    description = models.CharField(null=False, max_length=200)

    def __str__(self):
        return "Name: " + self.maker_name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    carMake = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    car_name = models.CharField(null=False, max_length=20, default='name')
    id = models.IntegerField(default=1,primary_key=True)

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    HONDA = 'Honda'
    TOYOTA = 'Toyota'

    MODEL_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (TOYOTA, 'Toyota')
    ]
    
    car_model = models.CharField(
        null=False,
        max_length=20,
        choices=MODEL_CHOICES,
        default=SEDAN
    )

    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.car_name





# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

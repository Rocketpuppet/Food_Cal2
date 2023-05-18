from django.db import models
import csv

class BaseIng(models.Model):
    ing_name = models.CharField(max_length=200)
    measurement_type = models.CharField(max_length=200)
    package_price = models.FloatField()
    package_size = models.FloatField()

    def __str__(self):
        return self.ing_name


    def readCSV(self, file):
        csv_reader = csv.reader(file)

        for line in csv_reader:
            print(line['FoodDescription'])

    def price_per_unit(self):
        return round(self.package_price/self.package_size, 3)

    



class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    servings = models.IntegerField()
    descripton = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def parse_time(self):
        return self.time_created.strftime("%b. %d, %Y")

    def calulcate_price(self):
        total_price = 0
        servings_price = 0
        for ing in self.recipeing_set.all():
            total_price = total_price + ing.calulcate_price()

        final_price = total_price
        servings_price = total_price/self.servings
        return final_price, servings_price



    def __str__(self):
        return self.recipe_name

class RecipeIng(models.Model):
    item_mass = models.FloatField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    base_ing = models.ForeignKey(BaseIng, on_delete=models.CASCADE)

    def calulcate_price(self):
        return round(self.base_ing.price_per_unit()*self.item_mass, 2)

    def __str__(self):
        return self.base_ing.ing_name
    
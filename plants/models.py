from django.core.validators import MaxLengthValidator
from django.db import models
from django.urls import reverse


class Plant(models.Model):
    class Category(models.TextChoices):
        HOUSEPLANTS = "houseplants", "Houseplants"
        HERBS = "herbs", "Herbs"
        FLOWERS = "flowers", "Flowers"
        SUCCULENTS = "succulents", "Succulents"
        FRUIT_TREES = "fruit-trees", "Fruit trees"

    name = models.CharField(max_length=120)
    about = models.TextField(validators=[MaxLengthValidator(3000)])
    used_for = models.TextField(validators=[MaxLengthValidator(2000)])
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(max_length=24, choices=Category.choices, db_index=True)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plants:detail", kwargs={"plant_id": self.pk})


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100)
    content = models.TextField(validators=[MaxLengthValidator(1500)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return f"{self.full_name} on {self.plant}"

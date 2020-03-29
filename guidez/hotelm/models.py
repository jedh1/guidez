from django.db import models

# Create your models here.
class Search(models.Model):
    recipient = models.CharField(max_length=100, blank=True)
    destination = models.CharField(max_length=128)
    check_in = models.CharField(max_length=16)
    check_out = models.CharField(max_length=16)
    special_rates = models.CharField(max_length=32, blank=True)
    special_rates_code = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f"Search ID {self.id}, {self.destination}, {self.check_in}, {self.check_out}, {self.special_rates}, {self.special_rates_code}"

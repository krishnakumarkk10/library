from django.db import models

# Create your models here.


class LibraryRecords(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return self.name

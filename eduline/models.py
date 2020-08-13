from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20)
    program = models.CharField(max_length=100)
    outstanding_fine = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    class Meta:
        ordering = ['matric_number']

    def __str__(self):
        return self.matric_number

    def pay_fine(self, fine):
        self.outstanding_fine -= fine

    def increase_fine(self, fine):
        self.outstanding_fine += fine


def get_upload_path(instance, filename):
    return 'books/covers/' + filename


class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No information available about this author")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    quantity_total = models.IntegerField(default=0)
    quantity_collected = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    image = models.ImageField(upload_to=get_upload_path, default='book.gif')

    class Meta:
        ordering = ['quantity_collected', 'title']

    def __str__(self):
        return self.title + " by " + self.author.name

    def add_copies(self, quantity):
        self.quantity_total += quantity

    def reserve_book(self):
        self.quantity_reserved += 1

    def cancel_reservation(self):
        self.quantity_reserved -= 1

    def return_book(self):
        self.quantity_collected -= 1

    def collect_book(self, reserved):
        if reserved:
            self.quantity_reserved -= 1
            self.quantity_collected += 1
        else:
            self.quantity_collected += 1


class Checkout(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)
    collected = models.BooleanField(default=False)
    overdue = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    reserved_date = models.DateField(null=True, blank=True)
    collected_date = models.DateField(null=True, blank=True)
    closed_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(decimal_places=2, default=0, max_digits=10)

    class Meta:
        ordering = ['student']

    def __str__(self):
        return self.student.__str__() + " - " + self.book.__str__()

    def charge_initial_fine(self):
        self.fine = 500

    def charge_subsequent_fines(self, days):
        self.fine = ((days - 1) * 100) + 500

    def close(self):
        self.closed = True
        self.closed_date = datetime.today()

    def reserve(self):
        self.reserved = True
        self.reserved_date = datetime.today()

    def collect(self):
        self.collected = True
        self.collected_date = datetime.today()


class Message(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.subject + " -- " + self.email

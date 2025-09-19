from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from books.models import Book

class Student(models.Model):
    name = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"


class Borrow(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    from_date = models.DateField()
    to_date = models.DateField()
    returned = models.BooleanField(default=False)
    returned_on = models.DateField(blank=True, null=True)
    fine = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.book.title} -> {self.student.roll_no}"

    def calculate_fine(self, per_day_amount=10):
        """
        Calculates fine based on returned_on (if set) or today.
        per_day_amount is currency per day overdue (change as needed).
        """
        compare_date = self.returned_on or timezone.localdate()
        overdue_days = (compare_date - self.to_date).days
        return per_day_amount * overdue_days if overdue_days > 0 else 0

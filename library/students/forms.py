from django import forms
from .models import Student, Borrow
from books.models import Book

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','roll_no','email','department']

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book','from_date','to_date']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
    # restrict book choices to those with available_copies > 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(available_copies__gt=0)

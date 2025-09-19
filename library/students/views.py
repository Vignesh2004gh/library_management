from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Borrow
from .forms import StudentForm, BorrowForm
from books.models import Book
from django.utils import timezone

def super_only(user):
    return user.is_superuser

@login_required
@user_passes_test(super_only)
def student_list(request):
    q = request.GET.get('q','')
    students = Student.objects.filter(Q(name__icontains=q) | Q(roll_no__icontains=q)).order_by('name') if q else Student.objects.all().order_by('name')
    return render(request, "students/student_list.html", {"students":students, "query":q})

@login_required
@user_passes_test(super_only)
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added.")
            return redirect('students:student_list')
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form":form, "title":"Add Student"})

@login_required
@user_passes_test(super_only)
def student_delete_search(request):
    students = []
    q = request.GET.get('q','')
    if q:
        students = Student.objects.filter(Q(name__icontains=q) | Q(roll_no__icontains=q))
    if request.method == "POST":
        sid = request.POST.get('student_id')
        student = get_object_or_404(Student, pk=sid)
        # optional: prevent deletion if student has active borrows
        if student.borrows.filter(returned=False).exists():
            messages.error(request, "Can't delete: student has borrowed books.")
        else:
            student.delete()
            messages.success(request, "Student deleted.")
            return redirect('students:student_list')
    return render(request, "students/student_delete.html", {"students":students, "query":q})

@login_required
@user_passes_test(super_only)
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    borrows = student.borrows.select_related('book').order_by('-from_date')
    # update fines on display
    for b in borrows:
        b.fine = b.calculate_fine()
    return render(request, "students/student_detail.html", {"student": student, "borrows": borrows})


def delete_borrow_record(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    student = borrow.student
    book = borrow.book
    
    # restore the book copy
    book.available_copies += 1
    book.save()

    # delete the borrow record
    borrow.delete()
    messages.success(request, f"Borrow record for {book.title} removed.")
    return redirect('students:student_detail', pk=student.pk)


@login_required
@user_passes_test(super_only)
def borrow_book(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.student = student
            # basic validation: ensure book has available copies
            book = borrow.book
            if book.available_copies <= 0:
                messages.error(request, "Selected book has no available copies.")
            else:
                # decrease available copies
                book.available_copies -= 1
                book.save()
                borrow.save()
                messages.success(request, "Book borrowed to student.")
                return redirect('students:student_detail', pk=student.pk)
    else:
        form = BorrowForm()
    return render(request, "students/borrow_form.html", {"form":form, "student":student})

@login_required
@user_passes_test(super_only)
def return_borrowed_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, pk=borrow_id)
    if borrow.returned:
        messages.info(request, "Already returned.")
        return redirect('students:student_detail', pk=borrow.student.pk)
    # mark returned, set returned_on, compute fine, increment available copies
    borrow.returned = True
    borrow.returned_on = timezone.localdate()
    borrow.fine = borrow.calculate_fine()
    borrow.save()
    book = borrow.book
    book.available_copies = min(book.total_copies, book.available_copies + 1)
    book.save()
    messages.success(request, f"Book returned. Fine: {borrow.fine}")
    return redirect('students:student_detail', pk=borrow.student.pk)

"""@login_required
@user_passes_test(super_only)
def delete_borrow_record(request, borrow_id):
    borrow = get_object_or_404(Borrow, pk=borrow_id)
    # If borrow not returned, increment the available_copies so models stay consistent
    if not borrow.returned:
        book = borrow.book
        book.available_copies = min(book.total_copies, book.available_copies + 1)
        book.save()
    student_pk = borrow.student.pk
    borrow.delete()
    messages.success(request, "Borrow record deleted.")
    return redirect('students:student_detail', pk=student_pk)
"""
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .forms import BookForm
from django.db.models import Q

def super_only(user):
    return user.is_superuser

@login_required
@user_passes_test(super_only)
def book_list(request):
    query = request.GET.get('q','')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, "books/book_list.html", {"books":books, "query":query})

@login_required
@user_passes_test(super_only)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added.")
            return redirect('books:book_list')
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form":form, "title":"Add Book"})

@login_required
@user_passes_test(super_only)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect('books:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, "books/book_form.html", {"form":form, "title":"Update Book"})

@login_required
@user_passes_test(super_only)
def book_delete_search(request):
    """Search and delete a book"""
    books = []
    q = request.GET.get('q','')
    if q:
        books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(isbn__icontains=q))
    if request.method == "POST":
        bid = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=bid)
        # optional: prevent deletion if book has active borrows
        if book.borrows.filter(returned=False).exists():
            messages.error(request, "Can't delete: some copies are borrowed.")
        else:
            book.delete()
            messages.success(request, "Book deleted.")
            return redirect('books:book_list')
    return render(request, "books/book_delete.html", {"books":books, "query":q})

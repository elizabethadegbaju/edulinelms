from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.shortcuts import render, redirect

from .filters import BookFilter
from .models import *


# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about-us.html')


def faq(request):
    # TODO: Edit FAQ
    return render(request, 'faq.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def book(request, pk):
    book = Book.objects.get(id=pk)
    # similar_books = book.category.aggregate('')
    return render(request, 'book.html', context={'book': book})


def contact(request):
    return render(request, 'contact-us.html')


def register(request):
    if request.method == "GET":
        return render(request, 'registration/register.html')
    elif request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        matric_number = request.POST['matric_number']
        program = request.POST['program']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username, password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.is_active = True
        user.save()
        student = Student.objects.create(matric_number=matric_number, program=program, user=user)
        student.save()
        return redirect('login')


def search(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(book_filter.qs, 15)
    try:
        books = paginator.get_page(page)
    except PageNotAnInteger:
        books = paginator.get_page(1)
    except InvalidPage:
        books = paginator.get_page(paginator.num_pages)

    return render(request, 'books.html', context={'filter': book_filter, 'books': books})


def reserve(request, pk):
    book = Book.objects.get(id=pk)
    record = Checkout.objects.create(student=request.user.student, book=book, reserved=True, reserved_date=now())
    record.save()
    book.reserve_book()
    book.save()
    return render(request, 'index.html')

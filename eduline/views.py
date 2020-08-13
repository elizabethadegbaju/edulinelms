from datetime import timedelta

from django.contrib.auth.views import login_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .filters import BookFilter, MessageFilter, CheckoutFilter
from .forms import *
from .models import *


# Create your views here.
def home(request):
    return render(request, 'index.html')


def faq(request):
    return render(request, 'faq.html')


@login_required
def dashboard(request):
    if request.user.is_staff:
        today = datetime.today().date()
        seven_days_ago = today - timedelta(days=7)
        five_days_ago = today - timedelta(days=5)
        two_months_ago = today - timedelta(days=60)
        two_weeks_ago = today - timedelta(weeks=2)

        # number of students that registered in the last seven days:
        new_students = Student.objects.filter(
            user__date_joined__range=(seven_days_ago, today)).count()

        # number of book reservations in the last five days:
        reservations = Checkout.objects.filter(reserved=True).filter(
            reserved_date__range=(five_days_ago, today)).count()

        # number of book collections in the last five days:
        collections = Checkout.objects.filter(collected=True).filter(
            collected_date__range=(five_days_ago, today)).count()

        # number of overdue books in two months:
        overdue_books = Checkout.objects.filter(overdue=True).filter(
            collected_date__range=(two_months_ago, today)).count()

        # number of returned books in the last two weeks:
        closed_transactions = Checkout.objects.filter(closed=True).filter(
            closed_date__range=(two_weeks_ago, today)).count()

        # Total outstanding fines:
        outstanding_fines = Checkout.objects.aggregate(Sum('fine'))

        total_collections = Checkout.objects.filter(collected=True).count()
        total_overdue = Checkout.objects.filter(overdue=True).count()
        overdue_percentage = round(((total_overdue / total_collections) *
                                    100), 2)

        books = Book.objects.all()
        available = 0
        unavailable = 0
        for book in books:
            if book.quantity_total > (
                    book.quantity_collected + book.quantity_reserved):
                available += 1
            else:
                unavailable += 1

        return render(request, 'dashboard.html',
                      context={'new_students': new_students,
                               'reservations': reservations,
                               'collections': collections,
                               'overdue_books': overdue_books,
                               'closed_transactions': closed_transactions,
                               'books': books.count(), 'available': available,
                               'unavailable': unavailable,
                               'outstanding_fines': outstanding_fines,
                               'total_collections': total_collections,
                               'total_overdue': total_overdue,
                               'overdue_percentage': overdue_percentage})
    else:
        return redirect('profile', request.user.username)


@login_required
def book(request, pk):
    book = Book.objects.get(id=pk)
    categories = book.category.all()
    available = book.quantity_total > (
            book.quantity_collected + book.quantity_reserved)
    similar_books = Book.objects.filter(
        category__in=categories).distinct().exclude(id=pk)
    return render(request, 'book.html',
                  context={'book': book, 'similar_books': similar_books,
                           'available': available})


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

        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.is_active = True
        user.save()
        student = Student.objects.create(matric_number=matric_number,
                                         program=program, user=user)
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
    if request.user.is_staff:
        return render(request, 'books-staff.html',
                      context={'filter': book_filter, 'books': books})
    else:
        return render(request, 'books.html',
                      context={'filter': book_filter, 'books': books})


@login_required
def reserve(request, pk):
    # TODO: configure checks to ensure user cannot reserve books that they have reserved or collected.

    book = Book.objects.get(id=pk)
    record = Checkout.objects.create(student=request.user.student, book=book,
                                     reserved=True,
                                     reserved_date=datetime.today())
    record.save()
    book.reserve_book()
    book.save()
    return redirect('book', pk)


@login_required
def profile(request, username):
    if request.user.is_staff:
        if username == request.user.username:
            return redirect('dashboard')
        else:
            student = User.objects.get(username=username)
            pending_history = Checkout.objects.filter(student__user=student)
            return render(request, 'student.html',
                          context={'pending_history': pending_history})
    elif username == request.user.username:
        student = request.user
        pending_history = Checkout.objects.filter(student__user=student,
                                                  closed=False)
        return render(request, 'student.html',
                      context={'pending_history': pending_history})
    else:
        redirect('home')


def submit_message(request):
    name = request.POST['name']
    subject = request.POST['subject']
    email = request.POST['email']
    message = request.POST['message']

    user_message = Message.objects.create(name=name, subject=subject,
                                          email=email, message=message)
    user_message.save()

    return render(request, 'contact-us.html')


def update_student(id):
    student = Student.objects.get(id=id)
    pending = Checkout.objects.filter(student=student)
    fine = 0
    for item in pending:
        fine += item.fine
    student.outstanding_fine = fine
    student.save()


def check_due_dates(request):
    if request.META.get('HTTP_X_APPENGINE_CRON'):
        pending_history = Checkout.objects.filter(closed=False)
        if pending_history is None:
            return HttpResponse(status='200')
        else:
            for entry in pending_history:
                pickup_date = entry.collected_date
                reserved_date = entry.reserved_date
                if pickup_date is None:
                    duration_reserved = datetime.today().date() - reserved_date
                    if duration_reserved.days > 1:
                        entry.close()
                        entry.save()
                        book = Book.objects.get(entry.book)
                        book.cancel_reservation()
                        book.save()
                else:
                    duration_collected = datetime.today().date() - pickup_date
                    if duration_collected.days <= 10:
                        pass
                    elif duration_collected.days == 11:
                        entry.charge_initial_fine()
                        entry.overdue = True
                        entry.save()
                    else:
                        entry.charge_subsequent_fines(
                            duration_collected.days - 10)
                        entry.overdue = True
                        entry.save()
                    update_student(entry.student.id)
    else:
        return HttpResponse(status="403")
    return HttpResponse(status='200')


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(search)
    else:
        form = BookForm()
    return render(request, 'add-book.html', context={'form': form})


def edit_book(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect(book, pk)
    else:
        form = BookForm(instance=book)
        return render(request, 'edit-book.html', context={'form': form})


def defaulters(request):
    students = Student.objects.filter(outstanding_fine__gt=0)
    return render(request, 'defaulters.html', context={'students': students})


def messages(request):
    messages_list = Message.objects.order_by('-time')
    messages_filter = MessageFilter(request.GET, queryset=messages_list)
    return render(request, 'messages.html',
                  context={'filter': messages_filter})


def add_author(request):
    name = request.POST['name']
    description = request.POST['description']
    author = Author.objects.create(name=name, description=description)
    author.save()
    return redirect(add_book)


def add_category(request):
    name = request.POST['name']
    category = Category.objects.create(name=name)
    category.save()
    return redirect(add_book)


def history(request, pk):
    book = Book.objects.get(id=pk)
    history_list = Checkout.objects.filter(book__id=pk)
    history_filter = CheckoutFilter(request.GET, queryset=history_list)
    return render(request, 'history.html',
                  context={'filter': history_filter, 'book': book})


def update(request, pk):
    entry = Checkout.objects.get(id=pk)
    print(request.POST)
    if ('reserved' in request.POST) & (entry.reserved != True):
        entry.reserve()
    if ('collected' in request.POST) & (entry.collected != True):
        entry.collect()
    if ('closed' in request.POST) & (entry.closed != True):
        entry.close()
    entry.save()
    return redirect(history, entry.book.id)

from django.urls import path

from eduline import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('books/', views.search, name='books'),
    path('books/<int:pk>/', views.book, name='book'),
    path('books/<int:pk>/reserve/', views.reserve, name='reserve'),
    path('contact-us/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('users/<str:username>/', views.profile, name='profile'),
    path('submit/message/', views.submit_message, name='submit_message'),
    path('check-due-dates/', views.check_due_dates, name='check_due_dates'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-book/', views.add_book, name='add_book'),
    path('dashboard/add-author/', views.add_author, name="add_author"),
    path('dashboard/add-category/', views.add_category, name='add_category'),
    path('dashboard/defaulters/', views.defaulters, name='defaulters'),
    path('dashboard/messages/', views.messages, name='messages'),
    path('dashboard/books/', views.search, name='books_staff'),
    path('dashboard/books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('dashboard/books/<int:pk>/history/', views.history, name='history'),
    path('dashboard/history/<int:pk>/update/', views.update, name='update'),
]

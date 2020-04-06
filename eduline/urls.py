from django.urls import path

from eduline import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('books/<int:pk>/', views.book, name='book'),
    path('books/', views.search, name='books'),
    path('contact-us/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reserve/<int:pk>/', views.reserve, name='reserve'),
    path('users/<str:username>/', views.profile, name='profile'),
    path('submit/message/', views.submit_message, name='submit_message'),
    path('check-due-dates/', views.check_due_dates, name='check_due_dates'),
    path('add-book/', views.add_book, name='add_book'),
]

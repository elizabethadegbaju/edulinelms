from django.urls import path, include
from eduline import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('books/', views.books, name='books'),
    path('contact', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('books/<int:pk>', views.book, name='book')
]

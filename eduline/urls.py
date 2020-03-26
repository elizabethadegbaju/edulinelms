from django.urls import path

from eduline import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('books/<int:pk>/', views.book, name='book'),
    path('books/', views.search, name='books'),
    path('contact', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reserve/<int:pk>', views.reserve, name='reserve'),
]

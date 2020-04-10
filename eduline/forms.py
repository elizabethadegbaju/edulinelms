from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from eduline.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'category', 'description', 'quantity_total', 'image')
        error_messages = {
            'title': {
                'max_length': _('The title of this book is too long.'),
            },
        }
        labels = {
            'quantity_total': _('Quantity'),
            'image': _('Book Cover'),
        }

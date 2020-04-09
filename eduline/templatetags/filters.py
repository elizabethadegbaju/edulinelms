from django import template

register = template.Library()

# @register.filter
# def is_overdue(value):
#     item = Checkout.objects.get(id=value)
#     pickup_date = item.collected_date
#     today = now()
#     if pickup_date is None:
#         return False
#     else:
#         duration = today.date() - pickup_date.date()
#         return duration.days > 10

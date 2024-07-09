from django import template
from emu.models import Order

register = template.Library()

class update_cart_items:
    items = 0

@register.filter
def cart_items_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, is_complete=False)
        if qs.exists():
            return qs[0].items.count()
    else:
        return update_cart_items.items
    return 0
    
        

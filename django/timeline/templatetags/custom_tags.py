from django import template
from timeline.models import Notification
register = template.Library()


@register.inclusion_tag('timeline/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(
        to_user=request_user).exclude(user_has_seen=True)
    return {'notifications_num': len(notifications)}

@register.filter(name='times') 
def times(number):
    return range(number)
    
@register.filter(name='debug_print') 
def debug_print(text):
    return print(text+"\n")
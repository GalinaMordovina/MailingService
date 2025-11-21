from django import template
from users.utils import is_manager

register = template.Library()


@register.simple_tag(takes_context=True)
def user_is_manager(context):
    """
    Возвращает True, если текущий пользователь менеджер.
    Использование в шаблоне:
    {% user_is_manager as is_manager %}
    {% if is_manager %} ... {% endif %}
    """
    user = context.get('user')
    if not user:
        return False
    return is_manager(user)

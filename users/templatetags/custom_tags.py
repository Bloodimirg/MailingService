from django import template

register = template.Library()


@register.filter(name='is_moderator')
def is_blockable_user(user):
    # возвращает False, если пользователь не является superuser или не в группе Moderators
    return not user.is_superuser and not user.groups.filter(name='Moderators').exists()

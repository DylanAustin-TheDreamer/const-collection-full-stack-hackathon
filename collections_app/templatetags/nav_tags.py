from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context, url_name_or_path):
    """Return 'active' if the current request.path equals or starts with the
    resolved URL for url_name_or_path, or if url_name_or_path is a raw path
    prefix and request.path starts with it.

    Usage in template::
        {% load nav_tags %}
        {# example: add active when current path matches the named URL #}
        <a class="nav-link {% nav_active 'collections_app:artwork_list' %}"
           href="{% url 'collections_app:artwork_list' %}">Store</a>
    """
    request = context.get('request')
    if request is None:
        return ''

    try:
        target = reverse(url_name_or_path)
    except NoReverseMatch:
        # If it's not a URL name, treat it as a raw path prefix
        target = url_name_or_path

    path = request.path or ''

    # Exact match or parent route (prefix) match
    # Exact match
    if path == target:
        return 'active'

    # Parent route match (target is a prefix and not just '/')
    if target != '/' and path.startswith(target):
        return 'active'

    # Root path special case
    if target == '/' and path == '/':
        return 'active'

    return ''

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def message_count(context):
    """Return unread message count if available, otherwise total messages.

    This checks for a `Messages` model in `owner_app.models`. If that model
    has an `unread` boolean field, it returns the count of unread messages.
    Otherwise it falls back to the total count. Any import/DB errors return 0.
    """
    try:
        from owner_app.models import Messages as MsgModel

        # If we have a request/user in the context, show unread count for
        # that owner. Otherwise fall back to the global unread count.
        request = context.get('request')
        if (
            request
            and getattr(request, 'user', None)
            and request.user.is_authenticated
        ):
            return (
                MsgModel.objects.filter(owner=request.user, unread=True).count()
            )

        # Prefer unread count if the field exists.
        if hasattr(MsgModel, 'unread'):
            return MsgModel.objects.filter(unread=True).count()
        return MsgModel.objects.count()
    except Exception:
        return 0

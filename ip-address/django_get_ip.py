def get_request_ip(request) -> Union[str, None]:
    """Get user ip."""

    meta_dict = request.META
    x_forwarded_for = meta_dict.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = next(iter(x_forwarded_for.split(',')), None)
    else:
        ip = meta_dict.get('REMOTE_ADDR')
    return ip

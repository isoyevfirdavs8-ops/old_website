def get_client_ip(request):

    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded:

        return forwarded.split(",")[0].strip()

    return request.META.get(
        "REMOTE_ADDR"
    )

def get_request_headers(request):

    return {

        key: value

        for key, value in request.headers.items()

    }
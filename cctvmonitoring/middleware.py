class RemoveCrossOriginOpenerPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Remove or modify the header
        if "Cross-Origin-Opener-Policy" in response.headers:
            del response.headers["Cross-Origin-Opener-Policy"]
        return response

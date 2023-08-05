from django.core.exceptions import ImproperlyConfigured


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Any site, even the Django admin, must have a corresponding `Site` and `TenantSite` model.
        # Thay are created automatically (by fixture) at the `manage.py initialize` run.
        if not hasattr(request.site, "tenantsite"):
            raise ImproperlyConfigured(
                f"No tenants found for site '{request.site}'. Please run 'manage.py initialize' first."
            )

        request.tenant = request.site.tenantsite.tenant
        request.tenantsite = request.site.tenantsite
        response = self.get_response(request)

        return response

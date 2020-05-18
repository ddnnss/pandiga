from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from staticPage.models import City
import settings

class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.get_host())
        domain_parts = request.get_host().split('.')
        domain_parts[0] = domain_parts[0].lower()
        subDomain = None
        wwwPresent = False
        try:
            domain_parts.remove('www')
            wwwPresent = True
        except:
            pass
        if wwwPresent:
            if domain_parts[0] != settings.MAIN_DOMAIN:
                subdomain = domain_parts[0]
            else:
                subdomain = None
        else:
            if domain_parts[0] != settings.MAIN_DOMAIN:
                subdomain = domain_parts[0]
            else:
                subdomain = None

        if not subdomain:
            try:
                subDomain = City.objects.get(is_default=True)
            except:
                subDomain = None
            homeDomain = True
        else:
            try:
                subDomain = City.objects.get(sub_domain=subdomain)
                homeDomain = False
            except:
                return HttpResponseRedirect(settings.PROTOCOL + settings.MAIN_DOMAIN + '.ru')

        request.subdomain = subDomain
        request.homedomain = homeDomain


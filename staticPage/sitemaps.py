from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import *
from technique.models import *
from techniqueOrder.models import *

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['login_page','forpartners','index','about',
                'servicerules','licenzionnoe_soglashenie','privacypolicy','publichnyj_agentskij_dogovor',
                'usloviya_ispolzovaniya','vacancies','servicerules','fortechniqueowners','tariff',
                'questions','contacts','technique_catalog','technique_all_orders']

    def location(self, item):
        return reverse(item)


class TechniqueSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    def items(self):
        return TechniqueItem.objects.all()


class TypeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    def items(self):
        return TechniqueType.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class SectionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    def items(self):
        return TechniqueSection.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class SubSectionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    def items(self):
        return TechniqueSubSection.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class OrdersSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    def items(self):
        return TechniqueOrder.objects.all()

    def lastmod(self, obj):
        return obj.created_at
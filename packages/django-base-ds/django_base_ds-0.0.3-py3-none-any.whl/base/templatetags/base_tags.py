import os
from django.template import Library

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.inclusion_tag("base/seo.html", takes_context=True)
def make_seo(context):
    return context


@register.inclusion_tag("base/vendor_css.html", takes_context=True)
def make_vendor_css(context):
    return {
        'vendor_css': make_up_vendor_css(context['theme']),
    }


@register.inclusion_tag("base/vendor_js.html", takes_context=True)
def make_vendor_js(context):
    return {
        'vendor_js': make_up_vendor_js(context['theme']),
    }


def make_up_vendor_css(theme=None) -> list:
    animate = os.path.join('vendor', 'animate.css', 'animate.min.css')
    bootstrap = os.path.join('vendor', 'bootstrap', 'css', 'bootstrap.min.css')
    bi = os.path.join('vendor', 'bootstrap-icons', 'bootstrap-icons.css')
    bx = os.path.join('vendor', 'boxicons', 'css', 'boxicons.min.css')
    fontawesome = os.path.join('vendor', 'fontawesome-free', 'css', 'all.min.css')
    glightbox = os.path.join('vendor', 'glightbox', 'css', 'glightbox.min.css')
    remixicon = os.path.join('vendor', 'remixicon', 'remixicon.css')
    swiper = os.path.join('vendor', 'swiper', 'swiper-bundle.min.css')
    aos = os.path.join('vendor', 'aos', 'aos.css')

    if theme == 'mentor_ds':
        return [animate, aos, bootstrap, bi, bx, remixicon, swiper]
    if theme == 'medilab_ds':
        return [animate, bootstrap, bi, bx, fontawesome, glightbox, remixicon, swiper]
    elif theme == 'bethany_ds':
        return [aos, bootstrap, bi, bx, glightbox, remixicon, swiper]
    else:
        return [aos, bootstrap, bi, bx, glightbox, remixicon, swiper, aos]


def make_up_vendor_js(theme=None) -> list:
    bootstrap = os.path.join('vendor', 'bootstrap', 'js', 'bootstrap.bundle.min.js')
    glightbox = os.path.join('vendor', 'glightbox', 'js', 'glightbox.min.js')
    phpemailform = os.path.join('vendor', 'php-email-form', 'validate.js')
    purecounter = os.path.join('vendor', 'purecounter', 'purecounter.js')
    swiper = os.path.join('vendor', 'swiper', 'swiper-bundle.min.js')
    aos = os.path.join('vendor', 'aos', 'aos.js')
    isotope = os.path.join('vendor', 'isotope-layout', 'isotope.pkgd.min.js')

    if theme == 'mentor_ds':
        return [aos, bootstrap, phpemailform, swiper, purecounter]
    if theme == 'medilab_ds':
        return [bootstrap, glightbox, isotope, phpemailform, swiper, purecounter]
    elif theme == 'bethany_ds':
        return [aos, bootstrap, glightbox, isotope, phpemailform, swiper, purecounter]
    else:
        return [aos, bootstrap, glightbox, isotope, phpemailform, swiper, purecounter]
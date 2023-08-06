import gettext
import locale as lib_locale
import logging

from typing import Union

logger = logging.getLogger("cytra")


def get_request_locales(headers):
    # e.g. 'es,en-US;q=0.8,en;q=0.6'
    locale_header = headers.get("accept-language", "").strip()
    if not locale_header:
        return

    if ";q=" in locale_header:
        # Extract all locales and their preference (q)
        locales = set()  # e.g. [('es', 1.0), ('en-US', 0.8), ('en', 0.6)]
        for locale_str in locale_header.split(","):
            locale_parts = locale_str.split(";q=")
            locales.add(
                (
                    locale_parts[0],
                    float(locale_parts[1]) if len(locale_parts) > 1 else 1.0,
                )
            )
        locales = map(
            lambda x: x[0],
            sorted(locales, key=lambda x: x[1], reverse=True),
        )
    else:
        locales = locale_header.split(",")

    # Sort locales according to preference
    for locale in locales:
        parts = locale.strip().split("-")
        if len(parts) == 1:
            yield parts[0], None
        else:
            yield parts[0], parts[1].upper()


class LocaleManager:
    def __init__(self, app, locales, domain, localedir):
        self.app = app
        self.locales = tuple(locales)
        self.locales_tuple = tuple(map(lambda x: tuple(x.split("_")), locales))
        self.translations = {}
        self.default = locales[0]
        self.set_locale(self.default)

        # load translations
        for locale in locales:
            self.translations[locale] = gettext.translation(
                domain=domain,
                localedir=localedir,
                languages=[locale],
            )

    def find_locale_from_request(self):
        request_locales = tuple(get_request_locales(self.app.request.headers))
        if request_locales:
            # find exact match
            for locale in request_locales:
                for locale_ in self.locales_tuple:
                    if locale == locale_:
                        return locale_

            # find by language match
            for lang, region in request_locales:
                for lang_, region_ in self.locales_tuple:
                    if lang == lang_:
                        return lang_, region_

        return self.default.split("_")

    def set_locale_from_request(self):
        lang, region = self.find_locale_from_request()
        self.set_locale(f"{lang}_{region}")
        self.app.response.headers["content-language"] = f"{lang}-{region}"

    def set_locale(self, locale):
        self.locale = locale
        try:
            lib_locale.setlocale(lib_locale.LC_ALL, locale)
        except lib_locale.Error:
            logger.exception("Locale error (%s)" % locale)

    def translate(self, word, plural=None, n=None):
        translation = self.translations[self.locale]
        if plural is not None:
            return translation.ngettext(word, plural, n)
        return translation.gettext(word)


class I18nAppMixin:
    """
    Internationalization Mixin

    Configuration:

    Example configuration in YAML:
        i18n:
          locales:
            - en_US
            - fa_IR
          localedir: myapp/i18n
          domain: app

    Note: First locale will set as default.

    Change locale:
        >>> app.i18n.set_locale('en_US')

    Translate:
        >>> app.i18n.translate('HelloWorld')
    """
    i18n = None

    def setup(self):
        super().setup()
        if "i18n" not in self.config:  # pragma: nocover
            return

        self.i18n = LocaleManager(self, **dict(self.config.i18n))

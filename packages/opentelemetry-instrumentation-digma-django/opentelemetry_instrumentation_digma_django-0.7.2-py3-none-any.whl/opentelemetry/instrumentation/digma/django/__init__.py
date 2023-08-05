from os import environ
from django import VERSION as django_version
from django.conf import settings
from opentelemetry.instrumentation.django.environment_variables import OTEL_PYTHON_DJANGO_INSTRUMENT
from opentelemetry.instrumentation.django.middleware import _DjangoMiddleware
from opentelemetry.instrumentation.digma.django.digma_middleware import _DigmaMiddleware

DJANGO_2_0 = django_version >= (2, 0)

def _get_django_middleware_setting() -> str:
# In Django versions 1.x, setting MIDDLEWARE_CLASSES can be used as a legacy
# alternative to MIDDLEWARE. This is the case when `settings.MIDDLEWARE` has
# its default value (`None`).
    if not DJANGO_2_0 and getattr(settings, "MIDDLEWARE", None) is None:
        return "MIDDLEWARE_CLASSES"
    return "MIDDLEWARE"

class DigmaIntrumentor:
    _digma_middleware = ".".join(
        [_DigmaMiddleware.__module__, _DigmaMiddleware.__qualname__]
    )
    _opentelemetry_middleware = ".".join(
        [_DjangoMiddleware.__module__, _DjangoMiddleware.__qualname__]
    )

    def instrument():
        
        if environ.get(OTEL_PYTHON_DJANGO_INSTRUMENT) == "False":
            return

        _middleware_setting = _get_django_middleware_setting()
        settings_middleware = getattr(settings, _middleware_setting, [])
        if isinstance(settings_middleware, tuple):
            settings_middleware = list(settings_middleware)

        index = settings_middleware.index(DigmaIntrumentor._opentelemetry_middleware)
        # If the otel middleware is not present, it may be that its instrumentation will happen later in the flow
        # in which case it will already inject itself later before the Digma middleware
        if (index<0):
            settings_middleware.insert(0, DigmaIntrumentor._digma_middleware)
        # If the otel middleware is present we want to make sure Digma's middleware runs later in the chain
        # so that the span context is already initialized
        else:
            settings_middleware.insert(index+1, DigmaIntrumentor._digma_middleware)
        
        setattr(settings, _middleware_setting, settings_middleware)
        


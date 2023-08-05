from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
# Using the OTEL implementation for a Mixin that already takes into account different Django versions
from opentelemetry.instrumentation.django.middleware import MiddlewareMixin

class _DigmaMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # This code is executed just before the view is called
        span = trace.get_current_span()
        if span and span.is_recording():
            if (view_func):
                span.set_attribute(SpanAttributes.CODE_NAMESPACE, view_func.__module__)
                span.set_attribute(SpanAttributes.CODE_FUNCTION, view_func.__qualname__)
                span.set_attribute(SpanAttributes.CODE_FILEPATH, view_func.__code__.co_filename)
                span.set_attribute(SpanAttributes.CODE_LINENO, view_func.__code__.co_firstlineno)


    
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        return response




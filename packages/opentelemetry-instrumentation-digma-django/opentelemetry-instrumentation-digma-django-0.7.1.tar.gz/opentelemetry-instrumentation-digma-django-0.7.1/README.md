# opentelemetry-instrumenation-digma
[![PyPI version](https://badge.fury.io/py/opentelemetry-instrumentation-digma-django.svg)](https://badge.fury.io/py/opentelemetry-instrumentation-digma-django)

This package provides instrumentation for additional span attributes provided on top of the [opentelmetery-instrumentation-django](https://pypi.org/project/opentelemetry-instrumentation-django/) package. 

In order to be able to effectively glean code-object based insights for continuous feedback and map them back in the IDE, Digma inserts additional attribute into the OTEL resource attributes. 

### Installing the package
```bash
pip install opentelemetry-instrumentation-digma-django
```

Via pip, or add to your requirements/toml file and update your environment.

### Building the package from source

```bash
python -m build
```

### Instrumenting your Django project

The Digma instrumentation depends on the official opentelemetry instrumentation or some other middleware to create and manage span lifecycle for each request.

It can be used alongside the generic [Digma Instrumentation helpers](https://github.com/digma-ai/opentelemetry-instrumentation-digma) to quickly set up your OTEL configuration

```python
digma_opentelmetry_boostrap(service_name='django-ms',
                            digma_backend='http://localhost:5050',
                            configuration=DigmaConfiguration().trace_this_package())
DjangoInstrumentor().instrument()
DigmaIntrumentor.instrument()
```

The Digma django instrumentation will simply add the view function and namespace using the Opentelemtry [semantic convention](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/span-general.md). We have requested to include this functionality as a part of the more general [opentelemetry-instrumenation-django](https://pypi.org/project/opentelemetry-instrumentation-django/) package. Help us by upvoting this [FR](https://github.com/open-telemetry/opentelemetry-python-contrib/issues/1074)!

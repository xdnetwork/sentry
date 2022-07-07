from typing import Iterable

"""Survey codebase for applicaton of ModeLimited decorators.

To use: From project root, do
    sentry shell < ./scripts/mode_limit_survey.py
"""


def seek_classes(root_module, base_class: type = None) -> Iterable[type]:
    def reflectively_import(root, next):
        import itertools

        module = None
        for part in root.split("."):
            if module is None:
                module = __import__(part)
            else:
                module = getattr(module, part)
            print(f"{module=}; {module.__name__=}")
        last = __import__(f"{module.__name__}.{next}")
        print(f"{last=}")
        print()
        return last
        # return module

    import pkgutil
    import pydoc

    for module_info in pkgutil.iter_modules(root_module.__path__):
        # module = reflectively_import(root_module.__name__, module_info.name)
        # module = __import__(root_module.__name__, fromlist=[module_info.name])
        module = pydoc.locate(f"{root_module.__name__}.{module_info.name}")
        print(f"{module=}")
        __import__(module.__name__)
    print(dir())


def all_model_classes() -> Iterable[type]:
    import sentry.models
    from sentry.db.models import BaseModel

    for name in dir(sentry.models):
        value = eval(f"sentry.models.{name}")
        if isinstance(value, type) and issubclass(value, BaseModel):
            yield value


def all_endpoint_classes() -> Iterable[type]:

    import sentry.api.endpoints
    from sentry.api.base import Endpoint

    for endpoint_module in pkgutil.iter_modules(sentry.api.endpoints.__path__):
        if endpoint_module.ispkg:
            print(endpoint_module)
    for name in dir(sentry.api.endpoints):
        value = eval(f"sentry.models.{name}")
        if isinstance(value, type) and issubclass(value, Endpoint):
            yield value


import sentry.api.endpoints

seek_classes(sentry.api.endpoints)
# for x in all_model_classes():
#     print(x.__name__)

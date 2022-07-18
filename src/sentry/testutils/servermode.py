import functools
from contextlib import contextmanager

from django.test import override_settings

from sentry.servermode import ServerComponentMode


class ServerModeTest:
    def __init__(self, *modes) -> None:
        super().__init__()
        self._modes = modes

    @property
    def modes(self):
        yield ServerComponentMode.MONOLITH
        yield from self._modes

    def _create_mode_test_method(self, test_method):
        def replacement_test_method(*args, **kwargs):
            for mode in self.modes:
                with override_settings(SERVER_COMPONENT_MODE=mode):
                    test_method(*args, **kwargs)

        functools.update_wrapper(replacement_test_method, test_method)
        return replacement_test_method

    def _apply_modes_to_all_methods(self, test_class):
        test_cases = {}
        for attr_name in dir(test_class):
            if not attr_name.startswith("test_"):
                continue
            attr = getattr(test_class, attr_name)
            if not callable(attr):
                continue
            test_cases[attr_name] = self._create_mode_test_method(attr)

        return type(test_class.__name__, (test_class,), test_cases)

    def __call__(self, decorated_test_obj):
        """Apply to a test case method to run in the given server mode.

        Also runs the method in monolith mode.
        """
        if isinstance(decorated_test_obj, type):
            return self._apply_modes_to_all_methods(decorated_test_obj)
        return self._create_mode_test_method(decorated_test_obj)


@contextmanager
def mode_exempt_setup():
    with override_settings(SERVER_COMPONENT_MODE=ServerComponentMode.MONOLITH):
        yield

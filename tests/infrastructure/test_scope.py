from pytest import raises

from gitstats.infrastructure.scope import Scope
from tests.infrastructure import an_instance
from tests.infrastructure import an_interface


def test_scope():
    interface = an_interface()
    instance = an_instance()

    scope = Scope()
    scope.register(interface, instance)

    assert scope.resolve(interface) == instance


def test_scope_resolve_with_error():
    scope = Scope()
    with raises(KeyError):
        scope.resolve(an_interface())

# five way to create a singleton class instance
# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
from typing import Dict, Optional, Type, TypeVar


class SingletonMeta(type):
    """Meta class to create singleton instance in default container."""
    def __call__(cls, *args, **kwargs):
        return add_type(cls, container=DEFAULT_CONTAINER_NAME, *args, **kwargs)


class Singleton(metaclass=SingletonMeta):
    """Create a singleton class with :class:`SingletonMeta`."""
    pass


def singleton(cls):
    """
    Singleton decorator but wrapped as function.

    ⚠WARN
    --------------
    This will wrapped :param:`cls` as function.
    >>> assert type(cls)==FunctionType # not cls
    """
    def getinstance(*args, **kwargs):
        return add_type(cls, container=DEFAULT_CONTAINER_NAME, *args, **kwargs)
    return getinstance


_containers: Dict[str, Dict[type, object]] = {"default": {}}
_T = TypeVar('_T')
DEFAULT_CONTAINER_NAME = 'default'


def add(obj: _T, container=DEFAULT_CONTAINER_NAME) -> Optional[_T]:
    """
    Add and :param:`obj` instance to singleton :param:`container`.

    :param obj: An object instance.
    :param container: name of container
    :returns: Added object or None obj is None.
    """
    if obj == None:
        return None
    container = container or DEFAULT_CONTAINER_NAME
    if container not in _containers:
        _containers[container] = {}
    c = _containers[container]
    t = type(obj)
    if t not in c:
        c[t] = obj
    # return c[t] instead of obj. obj may be another t instance if already exists.
    return c[t]


def add_type(t: Type[_T], *args,  container=DEFAULT_CONTAINER_NAME, **kwargs) -> Optional[_T]:
    """
    Create a :param:`t` instance to the container

    :param t: instance type.
    :param container: name of the container.
    :param args: arguments to init the instance.
    :param kwargs: additional arguments to init the instance.
    """
    if t == type(None):
        return None
    container = container or DEFAULT_CONTAINER_NAME
    if container not in _containers:
        _containers[container] = {}
    c = _containers[DEFAULT_CONTAINER_NAME]
    if t not in c:
        c[t] = super(
            SingletonMeta, t).__call__(*args, **kwargs)
    return c[t]


def resolve(t: Type[_T], container=DEFAULT_CONTAINER_NAME) -> Optional[_T]:
    """
    Get a stored singleton instance from :param:`container`

    :param t: object type to resolve.
    :param container: name of the container.
    :returns: a singleton instance if found, otherwise None.
    """
    if t == None:
        return None
    container = container or DEFAULT_CONTAINER_NAME
    if container not in _containers:
        return None
    return _containers[container].get(t)


get = resolve

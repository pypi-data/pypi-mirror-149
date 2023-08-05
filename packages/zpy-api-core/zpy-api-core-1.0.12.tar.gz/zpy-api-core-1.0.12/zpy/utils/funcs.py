from typing import Any, Callable, List, Optional
from functools import reduce
import logging
import time
import inspect
from zpy.utils.values import if_null_get
from zpy.app import zapp_context as ctx


def safely_exec(callable_fn: Callable, args=None) -> Optional[Any]:
    """
    Execute provided function in try:except block
    @param callable_fn:
    @param args:
    @return: value returned of execution or none
    """
    if args is None:
        args = []
    try:
        return callable_fn(*args)
    except Exception as e:
        logging.exception(e)
    return None


def safe_exec_wrapper(target: Callable, args=None, kwargs: dict = None,
                      msg: str = None,
                      notifier: Optional[Callable] = None,
                      default_ret=None):
    logg = ctx().logger
    if args is None:
        args = []
    if not kwargs:
        kwargs = {}
    try:
        return target(*args, **kwargs)
    except Exception as e:
        msg = if_null_get(msg, f"An error occurred while try execute: {target.__name__} with: {args} and {kwargs}.")
        logg.exception(msg)
        if notifier:
            notifier(f"Fatal: {msg}\n{str(e)}")
    return default_ret


def exec_if_nt_null(callable_fn: Callable, args: Optional[List[Any]] = None) -> object:
    """
    Execute function if args not null
    """
    if args is None:
        args = []
    for arg in args:
        if arg is None:
            return False
    return callable_fn(*args)


def safely_exec_with(callable_fn: Callable, default_value: Any = None, args=None) -> Optional[Any]:
    """
    Execute provided function in try:except block
    @param default_value:
    @param callable_fn:
    @param args:
    @return: value returned of execution or none
    """
    if args is None:
        args = []
    try:
        return callable_fn(*args)
    except Exception as e:
        logging.exception(e)
    return default_value


def get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.im_self):
        if meth.__name__ in cls.__dict__:
            return cls
    return None


def timeit(msg: str = None):
    def _timeit_(method):
        def timed(*args, **kw):
            logg = ctx().logger
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()

            method_name = ('{} -> {}'.format(method.__module__, method.__name__)) if not msg else msg
            if 'log_time' in kw:
                name = kw.get('log_name', method.__name__.upper())
                kw['log_time'][name] = int((te - ts) * 1000)
            else:
                logg.info(f"Time Execution: {method_name} :: {(te - ts) * 1000:2.2f} ms.")

            return result

        return timed

    return _timeit_


def fn_composite(*func):
    """
    Function composition
    @param func: functions
    @return: composition
    """

    def compose(f, g):
        return lambda x: f(g(x))

    return reduce(compose, func, lambda x: x)

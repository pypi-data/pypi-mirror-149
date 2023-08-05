""" Decorator. Add mongodb signals capability.
"""
from signals_utils.signals.mongo.connector import connect


def receiver(signal, sender):
    """A decorator for connecting receivers to signals. Used by passing in the signal (or list of signals) and the
    sender (class to watch).

    Example::

        @receiver(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs):
            ...

        @receiver([post_save, post_delete], sender=MyModel)
        def signals_receiver(sender, **kwargs):
            ...

    Args:
        signal: signal (or list of signals).
        sender: Class to watch.

    Returns:
         The decorator.
    """

    def _decorator(func):
        connect(func, signal, sender)
        return func

    return _decorator

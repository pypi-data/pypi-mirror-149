""" Connect a signal/signals to a receiver.
"""
from signals_utils.commons.exceptions import SignalsError


def connect(receiver, signal, sender):
    """Connecting receiver to signals. Used by passing in the receiver (method/function), signal (or list of signals)
    and the sender (class to watch).

    Example::

        connector.connect(receiver, signals.post_save, MyModel)
        connector.connect(receiver, [signals.post_save, signals.post_delete], MyModel)

        def receiver(sender, document, **kwargs):
            ...

    Args:
        receiver: Method/Function to receive the signal/signals.
        signal: Signal or list of signals.
        sender: Class to watch.

    Raises:
        SignalsError: Error(s) during the connection.

    """
    try:
        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(receiver=receiver, sender=sender)
        else:
            signal.connect(receiver=receiver, sender=sender)
    except Exception as e:
        raise SignalsError(e)

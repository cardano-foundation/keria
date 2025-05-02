class HumanMessagingHandler:
    """ Processor of `exn` human messaging exn messages.

    """

    def __init__(self, notifier):
        """ Initialize instance

        Parameters:
            notifier (Notifier): outbound notifications

        """
        self.resource = "/hmessage"
        self.notifier = notifier

    def verify(self, serder, attachments=None):
        """  Do route specific processsing of human messaging exn messages

        Parameters:
            serder (Serder): Serder of the human readable exn message
            attachments (list): list of tuples of pather, CESR SAD path attachments to the exn event

        Returns:
            bool: True means the exn passed behaviour specific verification for remote signing protocol messages

        """
        return True

    def handle(self, serder, attachments=None):
        """  Do route specific processsing of human messaging exn messages

        Parameters:
            serder (Serder): Serder of the human readable exn message
            attachments (list): list of tuples of pather, CESR SAD path attachments to the exn event

        """
        data = dict(
            r=f"/exn{serder.ked['r']}",
            d=serder.said,
        )

        self.notifier.add(attrs=data)


def loadHandlers(exc, notifier):
    """ Load handlers for the human messaging protocol

    Parameters:
        exc (Exchanger): Peer-to-peer message router
        notifier (Notifier): outbound notifications

    """
    exc.addHandler(HumanMessagingHandler(notifier=notifier))

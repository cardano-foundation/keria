from keri.peer import exchanging


class RemoteSigningHandler:
    """ Processor of `exn` remote signing messages.

    """

    def __init__(self, resource, hby, notifier):
        """ Initialize instance

        Parameters:
            resource (str): route of messages for this handler
            hby (Habery): local identifier environment
            notifier (Notifier): outbound notifications

        """
        self.resource = resource
        self.hby = hby
        self.notifier = notifier

    def verify(self, serder, attachments=None):
        """  Do route specific processsing of remote signing protocol exn messages

        Parameters:
            serder (Serder): Serder of the Remote Signing protocol exn message
            attachments (list): list of tuples of pather, CESR SAD path attachments to the exn event

        Returns:
            bool: True means the exn passed behaviour specific verification for remote signing protocol messages

        """
        route = serder.ked['r']
        dig = serder.ked['p']

        match route.split("/"):
            case["", "remotesign", "ixn", "req"]:
                if not dig:  # Apply messages can only start an IPEX exchange
                    return True
            case["", "remotesign", "ixn", "ref"]:
                if not dig:
                    return False

                pserder, _ = exchanging.cloneMessage(self.hby, said=dig)
                if pserder is None:  # previous reference message does not exist
                    return False

                return self.response(pserder) is None

        return False

    def response(self, serder):
        saider = self.hby.db.erpy.get(keys=(serder.said,))
        if saider:
            rserder, _ = exchanging.cloneMessage(self.hby, saider.qb64)  # Clone previous so we reverify the sigs
            return rserder

        return None

    def handle(self, serder, attachments=None):
        """  Do route specific processsing of remote signing protocol exn messages

        Parameters:
            serder (Serder): Serder of the remote signing protocol exn message
            attachments (list): list of tuples of pather, CESR SAD path attachments to the exn event

        """
        data = dict(
            r=f"/exn{serder.ked['r']}",
            d=serder.said,
        )

        self.notifier.add(attrs=data)


def loadHandlers(hby, exc, notifier):
    """ Load handlers for the Remote Signing protocol

    Parameters:
        hby (Habery): Database and keystore for environment
        exc (Exchanger): Peer-to-peer message router
        notifier (Notifier): outbound notifications

    """
    exc.addHandler(RemoteSigningHandler(resource="/remotesign/ixn/req", hby=hby, notifier=notifier))
    exc.addHandler(RemoteSigningHandler(resource="/remotesign/ixn/ref", hby=hby, notifier=notifier))

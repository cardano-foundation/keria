from keri.peer import exchanging


class RemoteCoordinationHandler:
    """ Processor of `exn` remote coordination messages for credential sharing and issuance.

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
        """  Do route specific processsing of remote coordination protocol exn messages

        Parameters:
            serder (Serder): Serder of the Remote Coordination protocol exn message
            attachments (list): list of tuples of pather, CESR SAD path attachments to the exn event

        Returns:
            bool: True means the exn passed behaviour specific verification for remote coordination protocol messages

        """
        route = serder.ked['r']
        dig = serder.ked['p']
        attrs = serder.ked.get('a', {})

        match route.split("/"):
            case["", "coordination", "credentials", "info", "req"]:
                if not dig:
                    if 's' not in attrs:
                        return False
                    return True
                    
            case["", "coordination", "credentials", "info", "resp"]:
                if not dig:
                    return False

                if 'sads' not in attrs:
                    return False

                pserder, _ = exchanging.cloneMessage(self.hby, said=dig)
                if pserder is None:
                    return False

                return self.response(pserder) is None

            case["", "coordination", "credentials", "issue", "prop"]:
                if not dig:
                    if not all(field in attrs for field in ['s', 'a', 'e']):
                        return False
                    return True
                    
            case["", "coordination", "credentials", "issue", "resp"]:
                if not dig:
                    return False

                if any(key != 'd' for key in attrs.keys()):
                    return False

                pserder, _ = exchanging.cloneMessage(self.hby, said=dig)
                if pserder is None:
                    return False

                return self.response(pserder) is None

        return False

    def response(self, serder):
        saider = self.hby.db.erpy.get(keys=(serder.said,))
        if saider:
            rserder, _ = exchanging.cloneMessage(self.hby, saider.qb64)
            return rserder

        return None

    def handle(self, serder, attachments=None):
        """  Do route specific processsing of remote coordination protocol exn messages

        Parameters:
            serder (Serder): Serder of the remote coordination protocol exn message
            attachments (list): list of tuples of pather, CESR SAD path attachments to the exn event

        """
        data = dict(
            r=f"/exn{serder.ked['r']}",
            d=serder.said,
        )

        self.notifier.add(attrs=data)


def loadHandlers(hby, exc, notifier):
    """ Load handlers for the Remote Coordination protocol

    Parameters:
        hby (Habery): Database and keystore for environment
        exc (Exchanger): Peer-to-peer message router
        notifier (Notifier): outbound notifications

    """
    exc.addHandler(RemoteCoordinationHandler(resource="/coordination/credentials/info/req", hby=hby, notifier=notifier))
    exc.addHandler(RemoteCoordinationHandler(resource="/coordination/credentials/info/resp", hby=hby, notifier=notifier))
    exc.addHandler(RemoteCoordinationHandler(resource="/coordination/credentials/issue/prop", hby=hby, notifier=notifier))
    exc.addHandler(RemoteCoordinationHandler(resource="/coordination/credentials/issue/resp", hby=hby, notifier=notifier))
def loadHandlers(exc, notifier):
    twHandler = TunnelWalletHandler(notifier=notifier)
    wsHandler = WalletServerHandler(notifier=notifier)
    pingHandler = PingHandler(notifier=notifier)
    pongHandler = PongHandler(notifier=notifier)
    exc.addHandler(twHandler)
    exc.addHandler(wsHandler)
    exc.addHandler(pingHandler)
    exc.addHandler(pongHandler)

class TunnelWalletHandler:
    resource = "/tunnel/wallet/request"

    def __init__(self, notifier):
        self.notifier = notifier

    def handle(self, serder, attachments=None):
        data = dict(
            r=TunnelWalletHandler.resource,
            d=serder.said,
        )
        self.notifier.add(attrs=data)

class WalletServerHandler:
    resource = "/tunnel/server/request"

    def __init__(self, notifier):
        self.notifier = notifier
    
    def handle(self, serder, attachments=None):
        data = dict(
            r=WalletServerHandler.resource,
            d=serder.said,
        )
        self.notifier.add(attrs=data)

# Just to check if the other person has resolved our OOBIs.
class PingHandler:
    resource = "/tunnel/ping"

    def __init__(self, notifier):
        self.notifier = notifier
    
    def handle(self, serder, attachments=None):
        data = dict(
            r=PingHandler.resource,
            d=serder.said,
        )
        self.notifier.add(attrs=data)

class PongHandler:
    resource = "/tunnel/pong"

    def __init__(self, notifier):
        self.notifier = notifier
    
    def handle(self, serder, attachments=None):
        data = dict(
            r=PongHandler.resource,
            d=serder.said,
        )
        self.notifier.add(attrs=data)

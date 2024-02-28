def loadHandlers(exc, notifier):
    twHandler = TunnelWalletHandler(notifier=notifier)
    wsHandler = WalletServerHandler(notifier=notifier)
    exc.addHandler(twHandler)
    exc.addHandler(wsHandler)

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

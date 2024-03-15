from hio.base import doing
from keri import kering
from keri.app import forwarding, agenting, habbing
from keri.app.delegating import DelegateRequestHandler, delegateRequestExn
from keri.app.notifying import Notifier
from keri.core import coring, serdering
from keri.db import dbing


class Sealer(doing.DoDoer):
    """
    Sends messages to Delegator of an identifier and wait for the anchoring event to
    be processed to ensure the inception or rotation event has been approved by the delegator.

    Removes all Doers and exits as Done once the event has been anchored.

    """

    def __init__(self, hby, proxy=None, **kwa):
        """
        For the current event, gather the current set of witnesses, send the event,
        gather all receipts and send them to all other witnesses

        Parameters:
            hab (Hab): Habitat of the identifier to populate witnesses
            msg (bytes): is the message to send to all witnesses.
                 Defaults to sending the latest KEL event if msg is None
            scheme (str): Scheme to favor if available

        """
        self.hby = hby
        self.postman = forwarding.Poster(hby=hby)
        self.witq = agenting.WitnessInquisitor(hby=hby)
        self.witDoer = agenting.Receiptor(hby=self.hby)
        self.proxy = proxy

        super(Sealer, self).__init__(doers=[self.witq, self.witDoer, self.postman, doing.doify(self.escrowDo)],
                                     **kwa)

    def delegation(self, pre, sn=None, proxy=None):
        if pre not in self.hby.habs:
            raise kering.ValidationError(f"{pre} is not a valid local AID for delegation")

        # load the hab of the delegated identifier to anchor
        hab = self.hby.habs[pre]
        delpre = hab.kever.delegator  # get the delegator identifier
        if delpre not in hab.kevers:
            raise kering.ValidationError(f"delegator {delpre} not found, unable to process delegation")

        sn = sn if sn is not None else hab.kever.sner.num

        # load the event and signatures
        evt = hab.makeOwnEvent(sn=sn)

        if isinstance(hab, habbing.GroupHab):
            phab = hab.mhab
        elif hab.kever.sn > 0:
            phab = hab
        elif proxy is not None:
            phab = proxy
        elif self.proxy is not None:
            phab = self.proxy
        else:
            raise kering.ValidationError("no proxy to send messages for delegation")

        srdr = serdering.SerderKERI(raw=evt)
        del evt[:srdr.size]
        self.postman.send(hab=phab, dest=delpre, topic="delegate", serder=srdr, attachment=evt)

        self.hby.db.dune.pin(keys=(srdr.pre, srdr.said), val=srdr)

    def complete(self, prefixer, seqner, saider=None):
        """ Check for completed delegation protocol for the specific event

        Parameters:
            prefixer (Prefixer): qb64 identifier prefix of event to check
            seqner (Seqner): sequence number of event to check
            saider (Saider): optional digest of event to verify

        Returns:

        """
        csaider = self.hby.db.cdel.get(keys=(prefixer.qb64, seqner.qb64))
        if not csaider:
            return False
        else:
            if saider and (csaider.qb64 != saider.qb64):
                raise kering.ValidationError(f"invalid delegation protocol escrowed event {csaider.qb64}-{saider.qb64}")

        return True

    def escrowDo(self, tymth, tock=1.0):
        """ Process escrows of group multisig identifiers waiting to be compeleted.

        Steps involve:
           1. Sending local event with sig to other participants
           2. Waiting for signature threshold to be met.
           3. If elected and delegated identifier, send complete event to delegator
           4. If delegated, wait for delegator's anchored seal
           5. If elected, send event to witnesses and collect receipts.
           6. Otherwise, wait for fully receipted event

        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value.  Default to 1.0 to slow down processing

        """
        # enter context
        self.wind(tymth)
        self.tock = tock
        _ = (yield self.tock)

        while True:
            self.processEscrows()
            yield 0.5

    def processEscrows(self):
        self.processUnanchoredEscrow()
        self.processPartialWitnessEscrow()

    def processUnanchoredEscrow(self):
        """
        Process escrow of partially signed multisig group KEL events.  Message
        processing will send this local controllers signature to all other participants
        then this escrow waits for signatures from all other participants

        """
        for (pre, said), serder in self.hby.db.dune.getItemIter():  # group partial witness escrow
            kever = self.hby.kevers[pre]
            dkever = self.hby.kevers[kever.delegator]

            seal = dict(i=serder.pre, s=serder.snh, d=serder.said)
            if dserder := self.hby.db.findAnchoringSealEvent(dkever.prefixer.qb64, seal=seal):
                seqner = coring.Seqner(sn=dserder.sn)
                couple = seqner.qb64b + dserder.saidb
                dgkey = dbing.dgKey(kever.prefixer.qb64b, kever.serder.saidb)
                self.hby.db.setAes(dgkey, couple)  # authorizer event seal (delegator/issuer)
                self.witDoer.msgs.append(dict(pre=pre, sn=serder.sn))

                # Move to escrow waiting for witness receipts
                print(f"Waiting for fully signed witness receipts for {serder.sn}")
                self.hby.db.dpwe.pin(keys=(pre, said), val=serder)
                self.hby.db.dune.rem(keys=(pre, said))

    def processPartialWitnessEscrow(self):
        """
        Process escrow of delegated events that do not have a full compliment of receipts
        from witnesses yet.  When receipting is complete, remove from escrow and cue up a message
        that the event is complete.

        """
        for (pre, said), serder in self.hby.db.dpwe.getItemIter():  # group partial witness escrow
            kever = self.hby.kevers[pre]
            dgkey = dbing.dgKey(pre, serder.said)
            seqner = coring.Seqner(sn=serder.sn)

            # Load all the witness receipts we have so far
            wigs = self.hby.db.getWigs(dgkey)
            if len(wigs) == len(kever.wits):  # We have all of them, this event is finished
                if len(kever.wits) > 0:
                    witnessed = False
                    for cue in self.witDoer.cues:
                        if cue["pre"] == serder.pre and cue["sn"] == seqner.sn:
                            witnessed = True
                    if not witnessed:
                        continue
                print(f"Witness receipts complete, {pre} confirmed.")

                hab = self.hby.habs[pre]
                if isinstance(hab, habbing.GroupHab):
                    phab = hab.mhab
                elif hab.kever.sn > 0:
                    phab = hab
                elif self.proxy is not None:
                    phab = self.proxy
                else:
                    raise kering.ValidationError("no proxy to send messages for delegation")

                delpre = hab.kever.delegator  # get the delegator identifier
                if delpre not in hab.kevers:
                    raise kering.ValidationError(f"delegator {delpre} not found, unable to process delegation")
                smids = []
                sn = hab.kever.sner.num
                evt = hab.makeOwnEvent(sn=sn)

                exn, atc = delegateRequestExn(phab, delpre=pre, evt=bytes(evt), aids=smids)

                notifier = Notifier(hby=self.hby)
                handler = DelegateRequestHandler(hby=self.hby, notifier=notifier)
                handler.handle(serder=exn)

                self.hby.db.dpwe.rem(keys=(pre, said))
                self.hby.db.cdel.put(keys=(pre, seqner.qb64), val=coring.Saider(qb64=serder.said))

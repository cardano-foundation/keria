# -*- encoding: utf-8 -*-
"""
tests.app.remotesigning module

"""

from keri import core
from keri.core import parsing, coring
from keri.peer import exchanging
from keri.app import habbing, notifying

from keria.app import remotesigning


def test_remotesigning(mockHelpingNowIso8601):
    """ Test Remote Signing exchange protocol """

    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)

    salt2 = b'0123456789abcdeg'
    salter2 = core.Salter(raw=salt2)

    with (habbing.openHby(name="requester", temp=True, salt=salter.qb64) as reqHby,
          habbing.openHby(name="responder", temp=True, salt=salter2.qb64) as repHby):
        reqHab = reqHby.makeHab(name="requester")
        repHab = repHby.makeHab(name="responder")

        parsing.Parser().parse(ims=reqHab.makeOwnInception(), kvy=repHby.kvy)
        parsing.Parser().parse(ims=repHab.makeOwnInception(), kvy=reqHby.kvy)

        reqhandler = remotesigning.RemoteSigningHandler(resource="/remotesign/ixn/req", hby=repHby, notifier=notifying.Notifier(hby=repHby))
        refhandler = remotesigning.RemoteSigningHandler(resource="/remotesign/ixn/ref", hby=reqHby, notifier=notifying.Notifier(hby=reqHby))

        _, sad = coring.Saider.saidify(dict(m="Test", d=""))
        reqExn, reqEnd = exchanging.exchange(route="/remotesign/ixn/req", payload=sad, sender=reqHab.pre)
        reqIms = reqHab.endorse(serder=reqExn, last=False, pipelined=False)

        assert reqExn.raw == (b'{"v":"KERI10JSON00012c_","t":"exn","d":"EMB8Xdz_poAwR0TcZH8d6dMyCdwY3yxvEFrm'
                              b'1P4oncXf","i":"EOHgKQX82ThrwoNPEplEOAOKiiMhWPH4lrD0sjWwPvsx","rp":"","p":"",'
                              b'"dt":"2021-06-27T21:26:21.233257+00:00","r":"/remotesign/ixn/req","q":{},"a"'
                              b':{"m":"Test","d":"ENUVkgRudIEzxcwY7zDlPCn6mrXYw-1tUTxUSv5iUbWB"},"e":{}}')

        assert reqhandler.verify(serder=reqExn) is True

        data = dict(sn="1")
        badRepExn, _ = exchanging.exchange(route="/remotesign/ixn/ref", payload=data, sender=repHab.pre)
        assert refhandler.verify(serder=badRepExn) is False

        repExn, repEnd = exchanging.exchange(route="/remotesign/ixn/ref", payload=data, sender=repHab.pre, dig=reqExn.said)
        repIms = repHab.endorse(serder=repExn, last=False, pipelined=False)
        assert refhandler.verify(serder=repExn) is False

        assert repExn.raw == (b'{"v":"KERI10JSON000123_","t":"exn","d":"EP2o-Hh2BhofrQRYySb4-z3c4CBinfCCA6KA'
                              b'AHmolB4D","i":"EC7lREWxUkE6cuoPPOVKQfghCykscUolL9iojT3TyybR","rp":"","p":"EM'
                              b'B8Xdz_poAwR0TcZH8d6dMyCdwY3yxvEFrm1P4oncXf","dt":"2021-06-27T21:26:21.233257'
                              b'+00:00","r":"/remotesign/ixn/ref","q":{},"a":{"sn":"1"},"e":{}}')

        parsing.Parser().parse(ims=bytes(reqIms), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        assert refhandler.verify(serder=repExn) is True
        assert refhandler.verify(serder=badRepExn) is False

        # Ensure can only be one response
        parsing.Parser().parse(ims=bytes(repIms), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        assert refhandler.verify(serder=repExn) is False

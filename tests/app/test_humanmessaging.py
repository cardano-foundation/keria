# -*- encoding: utf-8 -*-
"""
tests.app.humanmessaging module

"""

from keri import core
from keri.core import coring
from keri.peer import exchanging
from keri.app import habbing, notifying

from keria.app import humanmessaging


def test_humanmessaging(mockHelpingNowIso8601):
    """ Test Remote Signing exchange protocol """

    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)

    salt2 = b'0123456789abcdeg'
    salter2 = core.Salter(raw=salt2)

    with (habbing.openHby(name="sender", temp=True, salt=salter.qb64) as senHby,
          habbing.openHby(name="receiver", temp=True, salt=salter2.qb64) as recHby):
        senHab = senHby.makeHab(name="sender")
        hmHandler = humanmessaging.HumanMessagingHandler(notifier=notifying.Notifier(hby=recHby))

        _, sad = coring.Saider.saidify(dict(m="Test", d=""))
        exn, end = exchanging.exchange(route="/hmessage", payload=sad, sender=senHab.pre)

        assert exn.raw == (b'{"v":"KERI10JSON000122_","t":"exn","d":"EHWFypgBR_QgFPP_H3BHaSxziwsqTMXDchgE'
                           b'h2LAE0bz","i":"EDCgRlPAn6VpNC_TitIudT5Z-8UgS-8a8tJ1eAYmdKj3","rp":"","p":"",'
                           b'"dt":"2021-06-27T21:26:21.233257+00:00","r":"/hmessage","q":{},"a":{"m":"Tes'
                           b't","d":"ENUVkgRudIEzxcwY7zDlPCn6mrXYw-1tUTxUSv5iUbWB"},"e":{}}')

        assert hmHandler.verify(serder=exn) is True

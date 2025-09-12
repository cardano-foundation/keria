# -*- encoding: utf-8 -*-
"""
test_remotecoordination.py module

Test Remote Coordination exchange protocol
"""

from keri import core
from keri.core import parsing, coring
from keri.peer import exchanging
from keri.app import habbing, notifying

from keria.app import remotecoordination


def test_coordination_info_request_handler(mockHelpingNowIso8601):
    """ Test Remote Coordination Info Request Handler """
    
    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)

    with habbing.openHby(name="test", temp=True, salt=salter.qb64) as hby:
        hab = hby.makeHab(name="test")
        handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/info/req",
            hby=hby,
            notifier=notifying.Notifier(hby=hby)
        )

        # Test GOOD data: Info request with required 's' field
        _, good_sad = coring.Saider.saidify({"s": "ECR_credential_schema_SAID", "holder": "did:example:123", "d": ""})
        good_exn, _ = exchanging.exchange(route="/coordination/credentials/info/req", payload=good_sad, sender=hab.pre)
        
        # Verify good request passes
        assert handler.verify(serder=good_exn) is True
        
        # Assert exact raw message format
        assert good_exn.raw == (b'{"v":"KERI10JSON00016c_","t":"exn","d":"ELv0Z9IZHItVxWKIFu9tPdiIY1Xde4aCylmknas23wRM",'
                               b'"i":"EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3","rp":"","p":"","dt":"2021-06-27T21:26:21.233257+00:00",'
                               b'"r":"/coordination/credentials/info/req","q":{},"a":{"s":"ECR_credential_schema_SAID",'
                               b'"holder":"did:example:123","d":"EFIf7LJpfe6YQuH9kSPTOjfmdYFwS1QBaJ6f0yJPaCal"},"e":{}}')

        # Test BAD data: Info request missing required 's' field
        _, bad_sad = coring.Saider.saidify({"holder": "did:example:123", "description": "Missing schema", "d": ""})
        bad_exn, _ = exchanging.exchange(route="/coordination/credentials/info/req", payload=bad_sad, sender=hab.pre)
        
        # Verify bad request fails
        assert handler.verify(serder=bad_exn) is False
        
        # Test handle method (should not raise exceptions)
        handler.handle(serder=good_exn)


def test_coordination_info_response_handler(mockHelpingNowIso8601):
    """ Test Remote Coordination Info Response Handler """
    
    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)
    salt2 = b'0123456789abcdeg'
    salter2 = core.Salter(raw=salt2)

    with (habbing.openHby(name="requester", temp=True, salt=salter.qb64) as reqHby,
          habbing.openHby(name="responder", temp=True, salt=salter2.qb64) as repHby):
        reqHab = reqHby.makeHab(name="requester")
        repHab = repHby.makeHab(name="responder")

        # Setup cross-visibility of identifiers
        parsing.Parser().parse(ims=reqHab.makeOwnInception(), kvy=repHby.kvy)
        parsing.Parser().parse(ims=repHab.makeOwnInception(), kvy=reqHby.kvy)

        resp_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/info/resp", 
            hby=reqHby, 
            notifier=notifying.Notifier(hby=reqHby)
        )

        # Create a request first to reference
        _, req_sad = coring.Saider.saidify({"s": "ECR_credential_schema_SAID", "holder": "did:example:123", "d": ""})
        req_exn, _ = exchanging.exchange(route="/coordination/credentials/info/req", payload=req_sad, sender=reqHab.pre)
        req_ims = reqHab.endorse(serder=req_exn, last=False, pipelined=False)

        # Test BAD data: Response without prior reference
        _, bad_sad = coring.Saider.saidify({"sads": ["cred1_SAID", "cred2_SAID"], "available": True, "d": ""})
        bad_resp_exn, _ = exchanging.exchange(route="/coordination/credentials/info/resp", payload=bad_sad, sender=repHab.pre)
        assert resp_handler.verify(serder=bad_resp_exn) is False

        # Test BAD data: Response missing required 'sads' field
        _, bad_sads_sad = coring.Saider.saidify({"available": True, "schemas": ["schema1"], "d": ""})
        bad_sads_exn, _ = exchanging.exchange(route="/coordination/credentials/info/resp", payload=bad_sads_sad, sender=repHab.pre, dig=req_exn.said)
        assert resp_handler.verify(serder=bad_sads_exn) is False

        # Test GOOD data: Response with required 'sads' field and prior reference
        _, good_sad = coring.Saider.saidify({"sads": ["cred1_SAID", "cred2_SAID"], "available": True, "schemas": ["schema1"], "d": ""})
        good_resp_exn, _ = exchanging.exchange(route="/coordination/credentials/info/resp", payload=good_sad, sender=repHab.pre, dig=req_exn.said)
        resp_ims = repHab.endorse(serder=good_resp_exn, last=False, pipelined=False)
        
        # Should fail until request is parsed
        assert resp_handler.verify(serder=good_resp_exn) is False

        # Parse request message to enable response verification
        parsing.Parser().parse(ims=bytes(req_ims), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        
        # Now response should be valid
        assert resp_handler.verify(serder=good_resp_exn) is True
        
        # Assert exact raw message format
        assert good_resp_exn.raw == (b'{"v":"KERI10JSON0001a7_","t":"exn","d":"EIYiQGgTvV8-MiU6LkYeKDBFyBBGlSKU7lD27NDjVe6C",'
                                    b'"i":"EC7lREWxUkE6cuoPPOVKQfghCykscUolL9iojT3TyybR","rp":"","p":"ECWABeAAolwYkU4Jz__HHmxebihg0HeVra2kXNCOr3J9",'
                                    b'"dt":"2021-06-27T21:26:21.233257+00:00","r":"/coordination/credentials/info/resp","q":{}'
                                    b',"a":{"sads":["cred1_SAID","cred2_SAID"],"available":true,"schemas":["schema1"],'
                                    b'"d":"EAeStSM7UbOq3wWY3e2mto4rzg_ipk9S0Q3y-41EurzN"},"e":{}}')

        # Ensure only one response is allowed
        parsing.Parser().parse(ims=bytes(resp_ims), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        assert resp_handler.verify(serder=good_resp_exn) is False


def test_coordination_issue_proposal_handler(mockHelpingNowIso8601):
    """ Test Remote Coordination Issue Proposal Handler """
    
    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)

    with habbing.openHby(name="test", temp=True, salt=salter.qb64) as hby:
        hab = hby.makeHab(name="test")
        handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/issue/prop",
            hby=hby,
            notifier=notifying.Notifier(hby=hby)
        )

        # Test GOOD data: Issue proposal with all required fields (s, a, e)
        good_data = {
            "s": "ECR_credential_schema_SAID",
            "a": {"name": "John Doe", "age": 30, "email": "john@example.com"},
            "e": [{"n": "issuer_edge", "s": "issuer_SAID"}],
            "holder": hab.pre,
            "d": ""
        }
        _, good_sad = coring.Saider.saidify(good_data)
        good_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/prop", payload=good_sad, sender=hab.pre)
        
        # Verify good proposal passes
        assert handler.verify(serder=good_exn) is True
        
        # Assert exact raw message format
        assert good_exn.raw == (b'{"v":"KERI10JSON0001f3_","t":"exn","d":"EJNgfUdEdKiYH9TtI2X9V4GUKhsZMbeo1iFt0GDjvwj7",'
                               b'"i":"EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3","rp":"","p":"","dt":"2021-06-27T21:26:21.233257+00:00",'
                               b'"r":"/coordination/credentials/issue/prop","q":{},"a":{"s":"ECR_credential_schema_SAID",'
                               b'"a":{"name":"John Doe","age":30,"email":"john@example.com"},"e":[{"n":"issuer_edge","s":"issuer_SAID"}],'
                               b'"holder":"EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3","d":"EIcMY92VGgeZFxL6rS4tsIjSVlP7iY8iewk04jSfAzV2"},"e":{}}')        # Test BAD data: Issue proposal missing 's' field
        bad_data_no_s = {
            "a": {"name": "John Doe", "age": 30},
            "e": [{"n": "issuer_edge"}],
            "holder": hab.pre,
            "d": ""
        }
        _, bad_sad_no_s = coring.Saider.saidify(bad_data_no_s)
        bad_exn_no_s, _ = exchanging.exchange(route="/coordination/credentials/issue/prop", payload=bad_sad_no_s, sender=hab.pre)
        assert handler.verify(serder=bad_exn_no_s) is False

        # Test BAD data: Issue proposal missing 'a' field
        bad_data_no_a = {
            "s": "ECR_credential_schema_SAID",
            "e": [{"n": "issuer_edge"}],
            "holder": hab.pre,
            "d": ""
        }
        _, bad_sad_no_a = coring.Saider.saidify(bad_data_no_a)
        bad_exn_no_a, _ = exchanging.exchange(route="/coordination/credentials/issue/prop", payload=bad_sad_no_a, sender=hab.pre)
        assert handler.verify(serder=bad_exn_no_a) is False

        # Test BAD data: Issue proposal missing 'e' field
        bad_data_no_e = {
            "s": "ECR_credential_schema_SAID",
            "a": {"name": "John Doe", "age": 30},
            "holder": hab.pre,
            "d": ""
        }
        _, bad_sad_no_e = coring.Saider.saidify(bad_data_no_e)
        bad_exn_no_e, _ = exchanging.exchange(route="/coordination/credentials/issue/prop", payload=bad_sad_no_e, sender=hab.pre)
        assert handler.verify(serder=bad_exn_no_e) is False

        # Test handle method (should not raise exceptions)
        handler.handle(serder=good_exn)


def test_coordination_issue_response_handler(mockHelpingNowIso8601):
    """ Test Remote Coordination Issue Response Handler """
    
    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)
    salt2 = b'0123456789abcdeg'
    salter2 = core.Salter(raw=salt2)

    with (habbing.openHby(name="requester", temp=True, salt=salter.qb64) as reqHby,
          habbing.openHby(name="responder", temp=True, salt=salter2.qb64) as repHby):
        reqHab = reqHby.makeHab(name="requester")
        repHab = repHby.makeHab(name="responder")

        # Setup cross-visibility of identifiers
        parsing.Parser().parse(ims=reqHab.makeOwnInception(), kvy=repHby.kvy)
        parsing.Parser().parse(ims=repHab.makeOwnInception(), kvy=reqHby.kvy)

        resp_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/issue/resp", 
            hby=reqHby, 
            notifier=notifying.Notifier(hby=reqHby)
        )

        # Create an issue proposal first to reference
        prop_data = {
            "s": "ECR_credential_schema_SAID",
            "a": {"name": "John Doe", "age": 30},
            "e": [{"n": "issuer_edge"}],
            "holder": reqHab.pre,
            "d": ""
        }
        _, prop_sad = coring.Saider.saidify(prop_data)
        prop_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/prop", payload=prop_sad, sender=reqHab.pre)
        prop_ims = reqHab.endorse(serder=prop_exn, last=False, pipelined=False)

        # Test BAD data: Response without prior reference
        _, bad_sad = coring.Saider.saidify({"d": ""})
        bad_resp_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/resp", payload=bad_sad, sender=repHab.pre)
        assert resp_handler.verify(serder=bad_resp_exn) is False

        # Test BAD data: Response with extra fields (only 'd' allowed)
        _, bad_extra_sad = coring.Saider.saidify({"accepted": True, "credential_id": "cred123", "d": ""})
        bad_extra_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/resp", payload=bad_extra_sad, sender=repHab.pre, dig=prop_exn.said)
        assert resp_handler.verify(serder=bad_extra_exn) is False

        # Test GOOD data: Response with only 'd' field and prior reference
        _, good_sad = coring.Saider.saidify({"d": ""})
        good_resp_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/resp", payload=good_sad, sender=repHab.pre, dig=prop_exn.said)
        resp_ims = repHab.endorse(serder=good_resp_exn, last=False, pipelined=False)
        
        # Should fail until proposal is parsed
        assert resp_handler.verify(serder=good_resp_exn) is False

        # Parse proposal message to enable response verification
        parsing.Parser().parse(ims=bytes(prop_ims), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        
        # Now response should be valid
        assert resp_handler.verify(serder=good_resp_exn) is True
        
        # Assert exact raw message format
        assert good_resp_exn.raw == (b'{"v":"KERI10JSON00015e_","t":"exn","d":"EKCLXYP2mCEL1kmgdlpCFs5_nYeJz7hJLEOe1_gFH_Kr",'
                                    b'"i":"EC7lREWxUkE6cuoPPOVKQfghCykscUolL9iojT3TyybR","rp":"","p":"EP8SsjuIyLLDyHJemJ8cWprD8veR6rAZhDOP72vtbQIL",'
                                    b'"dt":"2021-06-27T21:26:21.233257+00:00","r":"/coordination/credentials/issue/resp","q":{}'
                                    b',"a":{"d":"EIeKlm9B5ul5vsHu_-OpjNmSf1kn1iMsyTb7rpuE4Ylc"},"e":{}}')        # Ensure only one response is allowed
        parsing.Parser().parse(ims=bytes(resp_ims), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        assert resp_handler.verify(serder=good_resp_exn) is False


def test_all_coordination_handlers_integration(mockHelpingNowIso8601):
    """ Test all 4 coordination handlers working together end-to-end """
    
    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)
    salt2 = b'0123456789abcdeg'
    salter2 = core.Salter(raw=salt2)

    with (habbing.openHby(name="requester", temp=True, salt=salter.qb64) as reqHby,
          habbing.openHby(name="responder", temp=True, salt=salter2.qb64) as repHby):
        reqHab = reqHby.makeHab(name="requester")
        repHab = repHby.makeHab(name="responder")

        # Setup cross-visibility of identifiers
        parsing.Parser().parse(ims=reqHab.makeOwnInception(), kvy=repHby.kvy)
        parsing.Parser().parse(ims=repHab.makeOwnInception(), kvy=reqHby.kvy)

        # Test handler loading
        exc = exchanging.Exchanger(hby=reqHby, handlers=[])
        remotecoordination.loadHandlers(hby=reqHby, exc=exc, notifier=notifying.Notifier(hby=reqHby))
        
        # Verify all 4 handlers are loaded
        assert len(exc.routes) == 4
        expected_routes = [
            "/coordination/credentials/info/req",
            "/coordination/credentials/info/resp",
            "/coordination/credentials/issue/prop", 
            "/coordination/credentials/issue/resp"
        ]
        for route in expected_routes:
            assert route in exc.routes

        # Test complete info exchange flow
        info_req_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/info/req", hby=repHby, notifier=notifying.Notifier(hby=repHby)
        )
        info_resp_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/info/resp", hby=reqHby, notifier=notifying.Notifier(hby=reqHby)
        )

        # 1. Info Request
        _, info_req_sad = coring.Saider.saidify({"s": "ECR_credential_schema_SAID", "holder": "did:example:123", "d": ""})
        info_req_exn, _ = exchanging.exchange(route="/coordination/credentials/info/req", payload=info_req_sad, sender=reqHab.pre)
        info_req_ims = reqHab.endorse(serder=info_req_exn, last=False, pipelined=False)
        
        assert info_req_handler.verify(serder=info_req_exn) is True

        # 2. Info Response
        _, info_resp_sad = coring.Saider.saidify({"sads": ["cred1_SAID", "cred2_SAID"], "available": True, "d": ""})
        info_resp_exn, _ = exchanging.exchange(route="/coordination/credentials/info/resp", payload=info_resp_sad, sender=repHab.pre, dig=info_req_exn.said)
        info_resp_ims = repHab.endorse(serder=info_resp_exn, last=False, pipelined=False)
        
        # Parse request to enable response verification
        parsing.Parser().parse(ims=bytes(info_req_ims), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        assert info_resp_handler.verify(serder=info_resp_exn) is True

        # Test complete issue exchange flow
        issue_prop_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/issue/prop", hby=repHby, notifier=notifying.Notifier(hby=repHby)
        )
        issue_resp_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/issue/resp", hby=reqHby, notifier=notifying.Notifier(hby=reqHby)
        )

        # 3. Issue Proposal
        issue_prop_data = {
            "s": "ECR_credential_schema_SAID",
            "a": {"name": "John Doe", "age": 30},
            "e": [{"n": "issuer_edge"}],
            "holder": reqHab.pre,
            "d": ""
        }
        _, issue_prop_sad = coring.Saider.saidify(issue_prop_data)
        issue_prop_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/prop", payload=issue_prop_sad, sender=reqHab.pre)
        issue_prop_ims = reqHab.endorse(serder=issue_prop_exn, last=False, pipelined=False)
        
        assert issue_prop_handler.verify(serder=issue_prop_exn) is True

        # 4. Issue Response
        _, issue_resp_sad = coring.Saider.saidify({"d": ""})
        issue_resp_exn, _ = exchanging.exchange(route="/coordination/credentials/issue/resp", payload=issue_resp_sad, sender=repHab.pre, dig=issue_prop_exn.said)
        issue_resp_ims = repHab.endorse(serder=issue_resp_exn, last=False, pipelined=False)
        
        # Parse proposal to enable response verification
        parsing.Parser().parse(ims=bytes(issue_prop_ims), exc=exchanging.Exchanger(hby=reqHby, handlers=[]))
        assert issue_resp_handler.verify(serder=issue_resp_exn) is True

        # Verify raw message structures
        assert info_req_exn.ked["r"] == "/coordination/credentials/info/req"
        assert info_resp_exn.ked["r"] == "/coordination/credentials/info/resp"
        assert issue_prop_exn.ked["r"] == "/coordination/credentials/issue/prop"
        assert issue_resp_exn.ked["r"] == "/coordination/credentials/issue/resp"
        
        # Verify response messages reference their requests
        assert info_resp_exn.ked["p"] == info_req_exn.said
        assert issue_resp_exn.ked["p"] == issue_prop_exn.said
        
        # Verify request messages have no prior reference
        assert info_req_exn.ked["p"] == ""
        assert issue_prop_exn.ked["p"] == ""


def test_coordination_handler_error_cases(mockHelpingNowIso8601):
    """ Test error cases and edge conditions for coordination handlers """
    
    salt = b'0123456789abcdef'
    salter = core.Salter(raw=salt)

    with habbing.openHby(name="test", temp=True, salt=salter.qb64) as hby:
        hab = hby.makeHab(name="test")
        
        # Test unknown route
        handler = remotecoordination.RemoteCoordinationHandler(
            resource="/unknown/route",
            hby=hby,
            notifier=notifying.Notifier(hby=hby)
        )
        
        _, sad = coring.Saider.saidify({"test": "data", "d": ""})
        exn, _ = exchanging.exchange(route="/unknown/route", payload=sad, sender=hab.pre)
        
        # Unknown routes should fail verification
        assert handler.verify(serder=exn) is False
        
        # Test response method with non-existent message
        assert handler.response(exn) is None
        
        # Test empty attributes
        info_handler = remotecoordination.RemoteCoordinationHandler(
            resource="/coordination/credentials/info/req",
            hby=hby,
            notifier=notifying.Notifier(hby=hby)
        )
        
        _, empty_sad = coring.Saider.saidify({"d": ""})  # No required 's' field
        empty_exn, _ = exchanging.exchange(route="/coordination/credentials/info/req", payload=empty_sad, sender=hab.pre)
        
        assert info_handler.verify(serder=empty_exn) is False

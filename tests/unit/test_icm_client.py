from icm_python_client.icm_client import ICMClient
import httpretty
import unittest
from sure import expect
import json


USER = {'createdAt': '2015-01-12T16:52:47.614+0000',
        'email': 'a@aol.com',
        'id': '6fd989e0-9a7b-11e4-a6d1-c22f013130a9',
        'locations': [],
        'lock': None,
        'name': 'a',
        'permissions': ['delete' 'put' 'get'],
        'securityGroups': [],
        'subscriptions': []}


def path(trailing_path):
    return 'https://api.icmobile.singlewire.com/api/v1-DEV' + trailing_path


class TestICMClient(unittest.TestCase):
    def test_creation(self):
        ICMClient.create.when.called_with().should.throw(ValueError, 'Access token must be supplied')
        ICMClient.create.when.called_with('my-access-token', url=None).should.throw(ValueError, 'URL must be supplied')
        expect(ICMClient.create('my-access-token')).should_not.be.none

    def test_getattr_no_arg(self):
        client = ICMClient.create('my-access-token')
        expect(str(client.users())).should.equal(path('/users'))
        expect(str(client.message_templates())).should.equal(path('/message-templates'))
        expect(str(client.distribution_lists())).should.equal(path('/distribution-lists'))

    def test_getattr_single_arg(self):
        client = ICMClient.create('my-access-token')
        expect(str(client.users('user_id').subscriptions())).should.equal(path('/users/user_id/subscriptions'))
        expect(str(client.message_templates('msg_id').audio)).should.equal(path('/message-templates/msg_id/audio'))
        expect(str(client.distribution_lists('dist_id').user_subscriptions)).should.equal(
            path('/distribution-lists/dist_id/user-subscriptions'))

    @httpretty.activate
    def test_get_not_found(self):
        not_found = '{"status": 404,"message": "Not Found"}'
        httpretty.register_uri(httpretty.GET, path('/users/user_id'), status=404, body=not_found)
        client = ICMClient.create('my-access-token')
        response = client.users('user_id').GET()
        expect(response.status_code).should.equal(404)
        expect(response.text).should.equal(not_found)

    @httpretty.activate
    def test_get_not_unauthorized(self):
        unauthorized = '{"type": "unauthorized","status": 401,"message": "Unauthorized"}'
        httpretty.register_uri(httpretty.GET, path('/users/user_id'), status=401, body=unauthorized)
        client = ICMClient.create('my-access-token')
        response = client.users('user_id').GET()
        expect(response.status_code).should.equal(401)
        expect(response.text).should.equal(unauthorized)

    @httpretty.activate
    def test_get_single_user(self):
        httpretty.register_uri(httpretty.GET, path('/users/user_id'), body=json.dumps(USER))
        client = ICMClient.create('my-access-token')
        response = client.users('user_id').GET()
        expect(response.status_code).should.equal(200)
        expect(response.json()).should.equal(USER)

    @httpretty.activate
    def test_list_not_unauthorized(self):
        unauthorized = '{"type": "unauthorized","status": 401,"message": "Unauthorized"}'
        httpretty.register_uri(httpretty.GET, path('/users'), status=401, body=unauthorized)
        client = ICMClient.create('my-access-token')
        client.users().LIST().next.when.called_with().should.throw(Exception, 'Received an invalid status code')

    @httpretty.activate
    def test_list_can_get_empty_page_of_data(self):
        empty_page = json.dumps({'total': 0, 'next': None, 'previous': None, 'data': []})
        httpretty.register_uri(httpretty.GET, path('/users'), body=empty_page)
        client = ICMClient.create('my-access-token')
        client.users().LIST().next.when.called_with().should.throw(StopIteration)

    @httpretty.activate
    def test_list_can_full_page_of_data(self):
        empty_page = json.dumps({'total': 1, 'next': None, 'previous': None, 'data': [USER]})
        httpretty.register_uri(httpretty.GET, path('/users'), body=empty_page)
        client = ICMClient.create('my-access-token')
        users = client.users().LIST()
        expect(users.next()).should.equal(USER)
        users.next.when.called_with().should.throw(StopIteration)

    @httpretty.activate
    def test_list_can_get_multiple_pages_of_data(self):
        httpretty.register_uri(httpretty.GET, path('/users'),
                               responses=[
                                   httpretty.Response(body=json.dumps(
                                       {'total': 3, 'next': 'first', 'previous': None, 'data': [USER]})),
                                   httpretty.Response(body=json.dumps(
                                       {'total': 3, 'next': 'second', 'previous': 'first', 'data': [USER]})),
                                   httpretty.Response(body=json.dumps(
                                       {'total': 3, 'next': None, 'previous': 'second', 'data': [USER]}))
                               ])
        client = ICMClient.create('my-access-token')
        users = client.users().LIST(params={'limit': 10})
        expect(users.next()).should.equal(USER)
        expect(users.next()).should.equal(USER)
        expect(users.next()).should.equal(USER)
        users.next.when.called_with().should.throw(StopIteration)

    @httpretty.activate
    def test_post_unauthorized(self):
        unauthorized = '{"type": "unauthorized","status": 401,"message": "Unauthorized"}'
        httpretty.register_uri(httpretty.POST, path('/users'), status=401, body=unauthorized)
        client = ICMClient.create('my-access-token')
        response = client.users().POST(params={'name': 'Craig Smith', 'email': 'craig.smith@acme.com'})
        expect(response.status_code).should.equal(401)
        expect(response.text).should.equal(unauthorized)

    @httpretty.activate
    def test_post_creates_new_user(self):
        httpretty.register_uri(httpretty.POST, path('/users'), body=json.dumps(USER))
        client = ICMClient.create('my-access-token')
        response = client.users().POST(params={'name': 'a', 'email': 'a@aol.com'})
        expect(response.status_code).should.equal(200)
        expect(response.json()).should.equal(USER)

    @httpretty.activate
    def test_put_unauthorized(self):
        unauthorized = '{"type": "unauthorized","status": 401,"message": "Unauthorized"}'
        httpretty.register_uri(httpretty.PUT, path('/users/user_id'), status=401, body=unauthorized)
        client = ICMClient.create('my-access-token')
        response = client.users('user_id').PUT(params={'name': 'Craig Smith', 'email': 'craig.smith@acme.com'})
        expect(response.status_code).should.equal(401)
        expect(response.text).should.equal(unauthorized)

    @httpretty.activate
    def test_put_updates_existing_user(self):
        httpretty.register_uri(httpretty.PUT, path('/users/user_id'), body=json.dumps(USER))
        client = ICMClient.create('my-access-token')
        response = client.users('user_id').PUT(params={'name': 'a'})
        expect(response.status_code).should.equal(200)
        expect(response.json()).should.equal(USER)


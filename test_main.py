from urlShort import create_app

def test_short(client):
    response = client.get('/')
    assert b'Shorten' in response.data

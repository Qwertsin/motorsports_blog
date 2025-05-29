"""Tests for the motorsports_blog views."""




def test_index_ok(client):
    """Test that the index view returns a 200 status code."""
    response = client.get('/')
    assert response.status_code == 200

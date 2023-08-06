import locatieserver.client.suggest


def test_suggest():

    response = locatieserver.client.suggest("Westerein")

    assert response
    assert response.response.num_found == 140

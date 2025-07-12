async def test_get_uslugi(ac):
    response = await ac.get("/uslugi")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_uslugi(ac):
    uslugi_title = "БАНЬКА-ПАРИЛКА"
    response = await ac.post("/uslugi", json={"title": uslugi_title})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == uslugi_title
    assert "data" in res
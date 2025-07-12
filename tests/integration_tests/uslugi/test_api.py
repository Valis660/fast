async def test_get_uslugi(ac):
    response = await ac.get(
        "/uslugi"
    )
    print(f"{response.json()=}")

    assert response.status_code == 200
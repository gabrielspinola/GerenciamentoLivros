from src.main import app


def test_cadastro_page_is_available():
    client = app.test_client()
    response = client.get('/cadastro')

    assert response.status_code == 200
    assert b'Criar conta' in response.data

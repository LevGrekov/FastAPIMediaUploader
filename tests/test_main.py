from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_file():
    file_path = "D:\YDXJ0552.jpg"
    with open(file_path, "rb") as f:
        response = client.put("/api/upload/", files={"file": f})

    assert response.status_code == 200
    json_response = response.json()
    assert "file_id" in json_response
    assert "type" in json_response


def test_get_file_content():
    # Пример теста для эндпоинта получения содержимого файла
    file_id = "08a925d9-3bc3-4a17-8d7d-b2f5094253b6"
    response = client.get(f"/api/{file_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] in ["image/jpeg", "video/mp4"]


def test_get_file_content_with_params():
    # Пример теста для эндпоинта получения содержимого файла с параметрами
    file_id = "08a925d9-3bc3-4a17-8d7d-b2f5094253b6"
    params = {"width": 300, "height": 200}
    response = client.get(f"/api/{file_id}", params=params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"

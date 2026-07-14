import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"


def test_crear_tarea():
    payload = {
        "titulo": "Estudiar para el reto",
        "contenido": "Repasar POO y FastAPI",
        "deadline": str(date.today() + timedelta(days=7)),
    }
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)
    assert response.status_code == 201, f"Esperado 201, recibido {response.status_code}"
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["completada"] is False
    print("test_crear_tarea OK ->", data)
    return data["id"]


def test_obtener_tarea(task_id):
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200, f"Esperado 200, recibido {response.status_code}"
    data = response.json()
    assert data["id"] == task_id
    print("test_obtener_tarea OK ->", data)


def test_obtener_tarea_inexistente():
    response = requests.get(f"{BASE_URL}/tasks/999999")
    assert response.status_code == 404, f"Esperado 404, recibido {response.status_code}"
    print("test_obtener_tarea_inexistente OK ->", response.json())


def test_marcar_completada(task_id):
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/completar")
    assert response.status_code == 200, f"Esperado 200, recibido {response.status_code}"
    data = response.json()
    assert data["completada"] is True
    print("test_marcar_completada OK ->", data)


def test_marcar_completada_dos_veces_da_400(task_id):
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/completar")
    assert response.status_code == 400, f"Esperado 400, recibido {response.status_code}"
    print("test_marcar_completada_dos_veces_da_400 OK ->", response.json())


def test_obtener_tareas_caducadas():
    response = requests.get(f"{BASE_URL}/tasks/caducadas")
    assert response.status_code == 200, f"Esperado 200, recibido {response.status_code}"
    print("test_obtener_tareas_caducadas OK ->", response.json())


def test_datos_incorrectos():
    payload = {
        "titulo": "",
        "contenido": "Contenido de prueba",
        "deadline": str(date.today() + timedelta(days=1)),
    }
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)
    assert response.status_code == 422, f"Esperado 422, recibido {response.status_code}"
    print("test_datos_incorrectos OK ->", response.status_code)


if __name__ == "__main__":
    print("Ejecutando tests...")
    task_id = test_crear_tarea()
    test_obtener_tarea(task_id)
    test_obtener_tarea_inexistente()
    test_marcar_completada(task_id)
    test_marcar_completada_dos_veces_da_400(task_id)
    test_obtener_tareas_caducadas()
    test_datos_incorrectos()
    print("Tests completados")
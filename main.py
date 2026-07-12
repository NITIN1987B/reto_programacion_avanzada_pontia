from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import List

app = FastAPI(title="Task Management API", version="1.0.0")

# Modelos Pydantic
class TaskCreate(BaseModel):
    titulo: str = Field(min_length=1, description="Título de la tarea")
    contenido: str = Field(min_length=1, description="Contenido de la tarea")
    deadline: date = Field(description="Fecha de vencimiento")
    #Añadimos validacion deadline 
    @field_validator("deadline")
    def deadline_no_puede_ser_pasado(cls,value):
        if value < date.today():
            raise ValueError("La fecha de vencimiento no puede ser anterior a la de hoy")
        return value

class TaskUpdate(BaseModel):
    completada: bool = Field(description="Estado de completado")

class TaskResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    deadline: date
    completada: bool
    fecha_creacion: datetime

class Task:
    """Representa una tarea individual del dominio, con su propio estado y comportamiento."""

    def __init__(self, id: int, titulo: str, contenido: str, deadline: date):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.deadline = deadline
        self.completada = False
        self.fecha_creacion = datetime.now()

    def marcar_completada(self):
        """Cambia el estado de la tarea a completada."""
        self.completada = True

    def esta_caducada(self) -> bool:
        """Devuelve True si el deadline ya pasó y la tarea sigue sin completar."""
        return not self.completada and self.deadline < date.today()

    def __repr__(self):
        return f"Task(id={self.id}, titulo='{self.titulo}', completada={self.completada})"
    

# Almacenamiento en memoria
class TaskManager:
    """Clase de servicio que encapsula la lógica de negocio y gestiona la colección de tareas en memoria."""

    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.contador = 0

    def crear_tarea(self, titulo: str, contenido: str, deadline: date) -> Task:
        """Crea una nueva tarea, le asigna un id autoincremental y la guarda en memoria."""

        self.contador += 1
        nueva_tarea = Task(self.contador, titulo, contenido, deadline)
        self.tasks[nueva_tarea.id] = nueva_tarea
        return nueva_tarea

    def obtener_tarea(self, task_id: int) -> Task | None:
        """Devuelve la tarea con ese id, o None si no existe."""        
        return self.tasks.get(task_id)

    def marcar_completada(self, task_id: int) -> Task | None:
        """Marca una tarea como completada. Devuelve None si el id no existe."""        
        tarea = self.obtener_tarea(task_id)
        if tarea is None:
            return None
        tarea.marcar_completada()
        return tarea

    def obtener_caducadas(self) -> list[Task]:
        """Devuelve todas las tareas caducadas (deadline pasado y no completadas)."""
        return [t for t in self.tasks.values() if t.esta_caducada()]





# TODO: Implementar endpoints
# @app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
# def crear_tarea(task: TaskCreate):
#     ...

# @app.get("/tasks/{task_id}", response_model=TaskResponse)
# def obtener_tarea(task_id: int):
#     ...

# @app.put("/tasks/{task_id}/completar", response_model=TaskResponse)
# def marcar_completada(task_id: int):
#     ...

# @app.get("/tasks/caducadas", response_model=List[TaskResponse])
# def obtener_tareas_caducadas():
#     ...

@app.get("/")
def root():
    return {"message": "Task Management API"}

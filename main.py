from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from database import users_container, projects_container
from models import Proyecto, Usuario
from azure.cosmos import exceptions
from datetime import datetime

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "projects",
        "description": "Operations with projects.",
    },
]

app = FastAPI(title='API de Gestion de Evnetos y Participantes',openapi_tags=tags_metadata)

#### Endpoint de Usuarios

@app.get("/")
def home():
    return "Hola Mundo"

# Listar usuarios
@app.get("/users/", response_model=List[Usuario], tags=["users"])
def list_users():
    
    query = "SELECT * FROM c WHERE 1=1"
    items = list(users_container.query_items(query=query, enable_cross_partition_query=True))
    return items


# Crear usuario
@app.post("/users/", response_model=Usuario, status_code=201, tags=["users"])
def create_user(user: Usuario):
    try:
        # Si el usuario existe lanza un CosmosResourceExistsError
        users_container.create_item(body=user.dict())
        return user
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El usuario con este ID ya existe.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Actualizar usuario
@app.put("/users/{user_id}", response_model=Usuario, tags=["users"])
def update_user(user_id: str, updated_user: Usuario):

    try:
        # Si el usuario no existe lanza un CosmosResourceNotFoundError
        usuario = users_container.read_item(item=user_id, partition_key=user_id)
        
        # Actualizar campos
        usuario.update(updated_user.dict(exclude_unset=True))        
        users_container.replace_item(item=user_id, body=usuario)
        return usuario
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="El usuario con este ID no existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Eliminar usuario
@app.delete("/users/{user_id}", status_code=204, tags=["users"])
def delete_user(user_id: str):
    try:
        # Si el usuario no existe lanza un CosmosResourceNotFoundError
        users_container.delete_item(item=user_id, partition_key=user_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="El usuario con este ID no existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))



#### Endpoints de Proyectos

# Listar proyectos
@app.get("/projects/", response_model=List[Proyecto], tags=["projects"])
def list_projects():
    
    query = "SELECT * FROM c WHERE 1=1"
    items = list(projects_container.query_items(query=query, enable_cross_partition_query=True))
    return items


# Crear proyecto
@app.post("/projects/", response_model=Proyecto, status_code=201, tags=["projects"])
def add_project(project: Proyecto):
    try:
        # Si el usuario no existe lanza un CosmosResourceNotFoundError
        usuario = users_container.read_item(item=project.id_usuario, partition_key=project.id_usuario)

        # Si el proyecto existe lanza un CosmosResourceExistsError
        projects_container.create_item(body=project.dict())
        return project
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="El usuario con este ID no existe")
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El proyecto con este ID ya existe.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Obtener proyectos por usuario
@app.get("/users/{user_id}/projects",response_model=List[Proyecto], tags=["projects"])
def get_project_by_user(user_id: str):

    try:
        # Si el usuario no existe lanza un CosmosResourceNotFoundError
        usuario = users_container.read_item(item = user_id, partition_key = user_id)

        query = f"SELECT * FROM c WHERE c.id_usuario='{user_id}'"
        items = list(projects_container.query_items(query=query, enable_cross_partition_query=True))
        return items
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="El usuario con este ID no existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener proyectos por id
@app.get("/projects/{project_id}",response_model=Proyecto, tags=["projects"])
def get_project_by_id(project_id: str):

    try:
        # Si el proyecto no existe lanza un CosmosResourceNotFoundError
        project = projects_container.read_item(item = project_id, partition_key = project_id)
        return project
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Actualizar la informacion de un proyecto
@app.put("/projects/{project_id}", response_model=Proyecto, tags=["projects"])
def update_project(project_id: str, updated_project: Proyecto):

    try:
        # Si el proyecto no existe lanza un CosmosResourceNotFoundError
        flag_proy_user = 'Proyecto'
        proyecto = projects_container.read_item(item = project_id, partition_key = project_id)

        # Si el usuario no existe lanza un CosmosResourceNotFoundError
        flag_proy_user = 'Usuario'
        usuario = users_container.read_item(item = updated_project.id_usuario, partition_key = updated_project.id_usuario)
        

        # Si el usuario que modifica no es el creador del proyecto
        if updated_project.id_usuario != proyecto['id_usuario']:
            raise HTTPException(status_code=404, detail="El usuario no es owner de este proyecto. No puede modificar informacion")

        proyecto.update(updated_project.dict(exclude_unset=True))
        projects_container.replace_item(item=project_id, body=proyecto)

        return proyecto

    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail=flag_proy_user + ' no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
        

# Eliminar proyecto por id
@app.delete("/projects/{project_id}", status_code=204, tags=["projects"])
def delete_project(project_id: str):
    try:
        # Si el proyecto no existe lanza un CosmosResourceNotFoundError
        projects_container.delete_item(item = project_id, partition_key = project_id)
        return 
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
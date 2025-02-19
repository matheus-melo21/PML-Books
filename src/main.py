import sys 
import os
from fastapi import FastAPI, Response, status, Query
from utils.db.database import *
from queryApi import *
from utils.utils import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

tags_metadata = [
    {
        "name": "Livros",
        "description": "Operações com livros. Gerencie os livros da sua biblioteca.",
    },
    {
        "name": "Autores",
        "description": "Gerencie os autores dos livros.",
    },
]

description = """
## PML-BOOKS

"""

app = FastAPI(
    title="PML-BOOKS",
    summary="Pesquisa de Livros. 📖",
    version="0.0.1",
)

if not os.path.exists('database.db'):
    SQLModel.metadata.create_all(database)


#======= Consultar todos os livros - Get =======
@app.get("/listar/livros", tags=["Livros"], status_code=200)
def ListarTodosLivros(response: Response, page: int = Query(1, alias="pagina", ge=1), per_page: int = Query(10, alias="por_pagina", ge=1, le=10)):

    with Session(database) as session:

        result = paginacao(session, Livros, page, per_page)

    response.status_code = result["status"]

    return result


#======= Consultar ID Livro - Get =======
@app.get("/consultar/id={idLivro}", tags=["Livros"], status_code=200)
def consultarId(idLivro: uuid.UUID, response: Response):
    # Execute a função e chame-a de result
    result = consultarIdLivro(idLivro)
    # Pegue a variável status e atribua a response
    response.status_code = result["status"]
    return result


#======= Consultar ID ISBN - Get =======
@app.get("/consultar/isbn={idIsbn}", tags=["Livros"], status_code=200)
def consultarIsbn(idIsbn, response: Response):
     
    result = consultarLivroIsbn(idIsbn)

    response.status_code = result["status"]

    return result

#======= Listar Autores - Get =======
@app.get("/listar/autores", tags=["Autores"], status_code=200)
def listarTodosAutores(response: Response, page: int = Query(1, alias="pagina", ge=1), per_page: int = Query(10, alias="por_pagina", ge=1, le=10)):

    with Session(database) as session:
        result = paginacao(session, Autores, page, per_page)

    response.status_code = result["status"]

    return result


#======= Consultar Autor - Get =======
@app.get("/consultar/autor={idAutor}", tags=["Autores"], status_code=200)
def consultarAutoridAutor(idAutor: uuid.UUID, response: Response):
     
    result = consultaridAutor(idAutor)

    response.status_code = result["status"]

    return result


#======= Consultar Editora - Get =======
@app.get("/consultar/editora={editora}", tags=["Editora"], status_code=200)
def consultarEditora(editora: str, response: Response):
    # Execute a função e chame-a de result
    result = consultarLivroEditora(editora)
    # Pegue a variável status e atribua a response
    response.status_code = result["status"]
    return result


#======= Consultar Título - Get =======
@app.get("/consultar/titulo={titulo}", tags=["Titulo"], status_code=200)
def consultarTitulo(titulo: str, response: Response):
    # Execute a função e chame-a de result
    result = consultarLivroTitulo(titulo)
    # Pegue a variável status e atribua a response
    response.status_code = result["status"]
    return result


#======= Adicionar um livro - Post =======
@app.post("/adicionar/isbn={idIsbn}", tags=["Livros"], status_code=200)
def adicionarLivroIsbn(idIsbn: str, response: Response):

    result = cadastrarLivroIsbn(idIsbn)

    response.status_code = result["status"]

    return result


#======= Atualizar um livro - Put =======
@app.put("/atualizar/isbn={idIsbn}", tags=["Livros"], status_code=200)
# Defina o endpoint recebendo uma str e a resposta como Response
def atualizarIdLivro(idIsbn: str, response: Response):
    # Execute a função e chame-a de result
    result = atualizarLivro(idIsbn)
    # Pegue a variável status e atribua a response
    response.status_code = result["status"]
    return result


#======= Atualizar - Patch =======

#TODO - Criar endpoint patch para atualizar apenas um campo do livro


#======= Excluir um livro - Delete =======
@app.delete("/excluir/id={idLivro}", tags=["Livros"], status_code=200)
def excluirIdLivro(idLivro: uuid.UUID, response: Response):
    
    result = deletarIdLivro(idLivro)

    response.status_code = result["status"]

    return result
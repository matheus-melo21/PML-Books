import sys 
import os
from fastapi import FastAPI, Response, status
from utils.db.database import *
from queryApi import *

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
@app.get("/consultar", tags=["Livros"], status_code=200)
def consultar(response: Response):

    result = consultarLivros()

    response.status_code = result["status"]

    return result


#======= Consultar ID Livro - Get =======
@app.get("/consultar/id={idLivro}", tags=["Livros"])
def consultarId(idLivro: uuid.UUID, response: Response):
    result = consultarIdLivro(idLivro)
    return result


#======= Consultar ID ISBN - Get =======
@app.get("/consultar/isbn={idIsbn}", tags=["Livros"], status_code=200)
def consultarIsbn(idIsbn, response: Response):
     
    result = consultarLivroIsbn(idIsbn)

    response.status_code = result["status"]

    return result


#======= Consultar Autor - Get =======
'''
@app.get("/consultar/autor={autor}", tags=["Autores"])
def consultarAutor(autor: str):
    #return {"message": f"Estes são os livros do autor {autor}: \n {db}""}}
    return consultarLivroAutor(autor)
'''
# TODO - Como faer o db armazenar os autores do livro?

#======= Consultar Editora - Get =======

# TODO - Criar endpoint para consultar livros por editora


#======= Adicionar um livro - Post =======
@app.post("/adicionar/isbn={idIsbn}", tags=["Livros"], status_code=200)
def adicionarLivroIsbn(idIsbn: str, response: Response):

    result = cadastrarLivroIsbn(idIsbn)

    response.status_code = result["status"]

    return result


#======= Atualizar um livro - Put =======
@app.put("/atualizar/isbn={idIsbn}", tags=["Livros"])
# Defina o endpoint recebendo uma str e a resposta como Response
def atualizarIdLivro(idIsbn: str, response: Response):
    # Execute a função e chame-a de result
    result = atualizarLivro(idIsbn)
    # Retorne o resultado e/ou a response
    return result


#======= Atualizar - Patch =======

#TODO - Criar endpoint patch para atualizar apenas um campo do livro


#======= Excluir um livro - Delete =======
@app.delete("/excluir/id={idLivro}", tags=["Livros"], status_code=200)
def excluirIdLivro(idLivro: uuid.UUID, response: Response):
    
    result = deletarIdLivro(idLivro)

    response.status_code = result["status"]

    return result
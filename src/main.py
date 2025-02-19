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

app = FastAPI()

if not os.path.exists('database.db'):
    SQLModel.metadata.create_all(database)



#======= Adicionar - Post =======
@app.post("/adicionar/isbn={idIsbn}", tags=["Livros"], status_code=200)
def adicionarLivroIsbn(idIsbn: str, response: Response):

    result = cadastrarLivroIsbn(idIsbn)

    response.status_code = result["status"]

    return result

#======= Consultar - Get =======
@app.get("/consultar", tags=["Livros"], status_code=200)
def consultar(response: Response):

    result = consultarLivros()

    response.status_code = result["status"]

    return result

#======= Atualizar - Put =======
@app.put("/atualizar", tags=["Livros"])
def atualizarIdLivro():
    #
    return {"message": "Livro atualizado com sucesso."}

#======= Atualizar - Patch =======

#======= Excluir - Delete =======
@app.delete("/excluir/id={idLivro}", tags=["Livros"], status_code=200)
def excluirIdLivro(idLivro: uuid.UUID, response: Response):
    
    result = deletarIdLivro(idLivro)

    response.status_code = result["status"]

    return result


#======= Consultar ID Livro - Get =======
@app.get("/consultar/id={idLivro}", tags=["Livros"])
def consultarId(idLivro):
    #for id in db:
    #    if id == idLivro:
    #       return id
    return {"message": f"Esse é o livro {idLivro}"}

#======= Consultar ID ISBN - Get =======
@app.get("/consultar/isbn={idIsbn}", tags=["Livros"], status_code=200)
def consultarIsbn(idIsbn, response: Response):
     
    result = consultarLivroIsbn(idIsbn)

    response.status_code = result["status"]

    return result

#======= Consultar Autor - Get =======
@app.get("/consultar/autor={autor}", tags=["Autores"])
def consultarAutor(autor: str):
    #return {"message": f"Estes são os livros do autor {autor}: \n {db}""}}
    return consultarLivroAutor(autor)

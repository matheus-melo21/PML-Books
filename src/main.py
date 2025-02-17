import sys 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI
from utils.db.database import *

app = FastAPI()
database = engine


#======= Adicionar - Post =======
@app.post("/adicionar")
def adicionar():
   #database.append(engine)
    return {"message": "O livro foi adicionado com sucesso."}

#======= Consultar - Get =======
@app.get("/consultar")
def consultar():
    return {"message": f"Estes são os livros disponíveis: \n {database}", }

#======= Atualizar - Put =======
@app.put("/atualizar")
def atualizarIdLivro():
    #
    return {"message": "Livro atualizado com sucesso."}

#======= Excluir - Delete =======
@app.delete("/excluir")
def excluirIdLivro():
    #
    return {"message": "Livro excluído com sucesso."}

#======= Consultar ID Livro - Get =======
@app.get("/consultar/id={idLivro}")
def consultarId(idLivro):
    #
    return {"message": f"Esse é o livro {idLivro}"}

#======= Consultar ID ISBN - Get =======
@app.get("/consultar/isbn={idIsbn}")
def consultarIsbn(idIsbn):
    #
    return {"message": f"Esse é o livro {idIsbn}"}
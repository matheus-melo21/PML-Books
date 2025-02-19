import requests
from sqlmodel import *
from utils.db.database import *
from fastapi import status

#==================================== Get ISBN ==============================

def consultarLivroIsbn(idIsbn: str):
    
    try:
        # Verificando se o livro já está no banco de dados
        with Session(database) as session:
            query = select(Livros).where(Livros.isbn == idIsbn)
            result = session.exec(query).first()

            if result:
                return {"status": status.HTTP_200_OK, "livro": result}
            
            if result is None:
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Livro não foi encontrado no banco de dados."}

            else:
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno no servidor."}
    except Exception as e:
        print(f"Erro na consulta do livro: {str(e)}")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}

#==================================== Get Livros ==============================
    
def consultarLivros():
    try:
        # Cria uma sessão com o db
        with Session(database) as session:
            # Faz a consulta de todos os livros
            query = select(Livros)
            # Armazena o resultado em uma lista
            result = session.exec(query).all()
            # Retorna erros e o db em caso de sucesso
            if result:
                return {"status": status.HTTP_200_OK, "livro": result}
            if not result:
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "O banco de dados está vazio."}

            else:
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno no servidor."}
    except Exception as e:
        print(f"Erro na consulta do livro: {str(e)}")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}

#================================== Post ==============================

def cadastrarLivroIsbn(idIsbn: str):
    try:
        # Fazendo a consulta à API externa
        response = requests.get(
            f"https://brasilapi.com.br/api/isbn/v1/{idIsbn}",
            headers={"Accept": "application/json"},
        )
        
        if response.status_code == 200:
            # Convertendo a resposta para JSON
            livroData = response.json()
            
            # Verificando se o livro já está no banco de dados
            with Session(database) as session:
                query = select(Livros).where(Livros.isbn == idIsbn)
                result = session.exec(query).first()

                if result:
                    return {"status": status.HTTP_200_OK, "mensagem": "Livro já está no banco de dados."}

                # Caso não esteja, armazenar os dados no banco
                if result is None:
                    session.add(Livros(
                        isbn=livroData["isbn"],
                        titulo=livroData["title"],
                        sinopse=livroData.get("synopsis", ""),
                        editora=livroData.get("publisher", ""),
                        formato=livroData.get("format", ""),
                        ano=livroData.get("year", ""),
                        paginas=livroData.get("page_count", ""),
                        cover_url=livroData.get("cover_url", ""),
                    ))
                    session.commit()
                    return {"status": status.HTTP_201_CREATED, "mensagem": "Livro foi cadastrado com sucesso."}
        else:
            raise requests.exceptions.RequestException(
                f"Erro ao consultar a API externa: {response.status_code}"
            )
    except Exception as e:
        print(f"Erro na consulta do livro: {str(e)}")
        return {"status": "error", "mensagem": str(e)}
    
#================================== Put ==============================

def atualizarLivro(idIsbn: str):
    try:
        with Session(database) as session:
            query = select(Livros).where(Livros.isbn == idIsbn)
            result = session.exec(query).first()
            if result:
                result = idIsbn
                deletarIdLivro(idIsbn)
                if result:
                    print(f"O livro com ISBN '{idIsbn}' foi excluido do banco de dados com sucesso.")
                    cadastrarLivroIsbn(idIsbn)
                    if result:
                        return {"satus": status.HTTP_200_OK, "mensagem": f"O livro com ISBN '{idIsbn}' foi atualizado com sucesso."}
                    else:
                        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro ao cadastrar o livro no banco de dados."}
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "O livro com ISBN '{idIsbn}' não pode ser excluído do banco de dados."}
            if not result:
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Não foi encontrado um livro com esse ISBN no banco de dados"}
            else:
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno do servidor."}
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {"status": "Erro", "mensagem": str(e)}

    
#================================== Excluir - Delete ==============================

def deletarIdLivro(livroId: uuid.UUID):
    
    try:
        with Session(database) as session:
            query = select(Livros).where(Livros.idLivro == livroId)
            result = session.exec(query).first()

            if result:
                session.delete(result)
                session.commit()
                return {"status": status.HTTP_200_OK, "mensagem": "Livro foi excluído com sucesso."}
            
            if result is None:
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Livro não foi encontrado no banco de dados."}

            else:
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno no servidor."}
    except Exception as e:
        print(f"Erro na exclusão do livro: {str(e)}")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}
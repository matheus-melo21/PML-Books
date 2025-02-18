import requests
from sqlmodel import *
from utils.db.database import *
from fastapi import status

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
                        sinopse=livroData["synopsis"],
                        editora=livroData["publisher"],
                        formato=livroData["format"],
                        ano=livroData["year"],
                        paginas=livroData["page_count"],
                        cover_url=livroData["cover_url"],
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
    
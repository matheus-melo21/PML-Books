import requests
from sqlmodel import *
from utils.db.database import *
from utils.utils import *
from fastapi import status

# FIXME - Corrigir a consulta com espaços e/ou com caracteres especiais
# FIXME - atualizarLivro() - Comparar os jsons antes de atualizar, para evitar atualizações desnecessárias
# FIXME - consultarAutorIdAutor() - Mostrar os livros que o autor escreveu


#==================================== Get - Consultar ID ISBN ==============================

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


#==================================== Get - Consultar ID Livro ==============================
def consultarIdLivro(livroId: uuid.UUID):
    try:
        with Session(database) as session:
            # Faz a consulta do livro com o ID
            query = select(Livros).where(Livros.idLivro == livroId)
            # Armazena o primeiro resultado da lista
            result = session.exec(query).first()
            if result:
                return {"status": status.HTTP_200_OK, "mensagem": f"O livro encontrado com o ID '{livroId}' foi:", "livro": result }
            if not result:
                return {"satus": status.HTTP_404_NOT_FOUND, "mensagem": f"O livro com o id '{livroId}' não foi encontrado no banco de dados."}
            else:
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno no servidor."}
    except Exception as e:
        print(f"Não foi possível consultar o livro no banco de dados.", {str(e)} )
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}
    
#==================================== Get - Consultar Autor ==============================
def consultaridAutor(autorId):

    try:
        with Session(database) as session:
            # Faz a consulta do autor com o ID
            query = select(Autores).where(Autores.idAutor == autorId)
            # Armazena o primeiro resultado da lista
            result = session.exec(query).first()

            if result:
                return {"status": status.HTTP_200_OK, "mensagem": f"O autor encontrado com o ID '{autorId}' foi:", "autor": result }
            
            if not result:
                return {"satus": status.HTTP_404_NOT_FOUND, "mensagem": f"O autor com o id '{autorId}' não foi encontrado no banco de dados."}
            else:
                return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno no servidor."}
    except Exception as e:
        print(f"Não foi possível consultar o autor no banco de dados.", {str(e)} )
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}
    


#==================================== Get - Consultar Editora ==============================
def consultarIdEditora(editoraId: uuid.UUID):

    try:
        with Session(database) as session:
            # Faz a consulta dos livros publicados por uma editora no db
            query = select(Editoras).where(Editoras.idEditora == editoraId)
            # Armazena todos os resultados em uma lista
            result = session.exec(query).first()
            if result:
                # Retorna os livros publicados pela editora
                    return {"status": status.HTTP_200_OK, "Editora": result}
            else:
                # Erro ao encontrar os livros publicados
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Não foi encontrado nenhuma editora com esse ID."}
    except Exception as e:
        # Erro ao consultar o db, armazene o erro e guarde-o em 'e'
        print(f"Não foi possível consultar a editora no banco de dados.")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}
    

#==================================== Get - Consultar Título ==============================
def consultarLivroTitulo(titulo: str):
    try:
        with Session(database) as session:
            # Faz a consulta dos livros com o título no db
            query = select(Livros).where(Livros.titulo == titulo)
            # Armazena todos os resultados em uma lista
            result = session.exec(query).all()
            # Checa quantos livros foram encontrados no result
            if len(result) == 1:
                # Retorna o livro com o título
                return {"status": status.HTTP_200_OK, "mensagem": f"Foi encontrado 1 livro com esse título", "livro": result}
            if len(result) > 1:
                # Retorna os livros com o título
                return {"status": status.HTTP_200_OK, "mensagem": f"Foram encontrados {len(result)} livros com esse título:", "livros": result}
            else:
                # Erro ao encontrar o livro com o título
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Não foi encontrado nenhum livro com esse título."}
    except Exception as e:
        # Erro ao consultar o db, armazene o erro e guarde-o em 'e'
        print(f"Não foi possível consultar o título no banco de dados.")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}
    

#================================== Post ==============================

def cadastrarLivroIsbn(idIsbn: str):
    try:
        # Fazendo a consulta à Brasil API usando a função genérica
        livroData = consultarLivroBrasilApiISBN(idIsbn)

        if livroData is None:
            return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Livro não encontrado na API."}

        # Verificando se o livro já está no banco de dados
        with Session(database) as session:
            query = select(Livros).where(Livros.isbn == idIsbn)
            result = session.exec(query).first()

            if result:
                return {"status": status.HTTP_200_OK, "mensagem": "Livro já está no banco de dados."}
            
            # Acessando os dados retornados pela API
            nomeEditora = livroData.get("publisher", "").strip()

            if nomeEditora:
                query = select(Editoras).where(Editoras.nome == nomeEditora)
                editora = session.exec(query).first()

                if not editora:
                    editora = Editoras(nome=nomeEditora)
                    session.add(editora)
                    session.commit()  # Confirmando a criação da editora
            else:
                editora = None  # Caso o livro não tenha editora informada

            # Caso não esteja, armazenar os dados no banco
            if not result:
                # Criando o objeto do livro
                livro = Livros(
                    isbn=livroData["isbn"],
                    titulo=livroData["title"],
                    sinopse=livroData.get("synopsis", ""),
                    formato=livroData.get("format", ""),
                    ano=livroData.get("year", ""),
                    paginas=livroData.get("page_count", ""),
                    cover_url=livroData.get("cover_url", ""),
                    idEditora=editora.idEditora if editora else None,
                )
                session.add(livro)
                session.commit()             

                # Processando autores
                for nomeAutor in livroData.get("authors", []):
                    query = select(Autores).where(Autores.nome == nomeAutor)
                    autor = session.exec(query).first()

                    if not autor:
                        autor = Autores(nome=nomeAutor)
                        session.add(autor)
                        
                        # Criando a relação entre livro e autor
                        livroAutor = LivrosAutor(idLivro=livro.idLivro, idAutor=autor.idAutor)
                        session.add(livroAutor)

                        session.commit()
                return {"status": status.HTTP_201_CREATED, "mensagem": "Livro foi cadastrado com sucesso."}

    except Exception as e:
        print(f"Erro na consulta do livro: {str(e)}")
        return {"status": "error", "mensagem": str(e)}
    
#================================== Put ===========================================

def atualizarLivro(idIsbn: str):
    try:
        with Session(database) as session:
            # Verificando se o ISBN já está no banco de dados
            query = select(Livros).where(Livros.isbn == idIsbn)
            # Armazenando o primeiro resultado
            result = session.exec(query).first()
            if result:
                # Chame-o de idIsbn
                result = idIsbn
                # Chame a função para excluir o livro com esse ISBN
                deletarIdLivro(idIsbn)
                if result:
                    # Informe que ele foi excluído e cadastre o livro novamente
                    print(f"O livro com ISBN '{idIsbn}' foi excluido do banco de dados com sucesso.")
                    cadastrarLivroIsbn(idIsbn)
                    if result == status.HTTP_201_CREATED:
                        # Informe que o livro foi atualizado com sucesso
                        return {"status": status.HTTP_200_OK, "mensagem": f"O livro com ISBN '{idIsbn}' foi atualizado com sucesso."}
                    else:
                        # Erro ao cadastrar o livro
                        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro ao cadastrar o livro no banco de dados."}
                else:
                    # Erro ao excluir o livro
                    return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "O livro com ISBN '{idIsbn}' não pode ser excluído do banco de dados."}
            else:
                # Erro ao encontrar o livro no db
                return {"status": status.HTTP_404_NOT_FOUND, "mensagem": "Erro ao consultar o livro com esse ISBN no banco de dados"}
    # Se houver um erro, armazene-o em 'e' e informe-o
    except Exception as e:
        print(f"Erro ao atualizar o livro: {str(e)}")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": str(e)}

    
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
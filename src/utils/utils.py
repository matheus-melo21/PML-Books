from sqlmodel import Session, select
from fastapi import status
from sqlalchemy.sql import func

def paginacao(session: Session, model, page: int, per_page: int):
    """
    Função genérica para paginar qualquer Lista de modelos SQLModel.
    
    :param session: Sessão do banco de dados.
    :param model: Modelo SQLModel que será paginado.
    :param page: Página atual.
    :param per_page: Número de itens por página.
    :return: Dicionário com os dados paginados.
    """
    try:
        # Conta o total de registros na tabela
        total_records = session.exec(select(func.count()).select_from(model)).one()

        # Calcula o número total de páginas
        total_pages = (total_records // per_page) + (1 if total_records % per_page > 0 else 0)

        # Calcula o offset (posição inicial dos registros)
        offset = (page - 1) * per_page

        # Consulta paginada
        query = select(model).offset(offset).limit(per_page)
        result = session.exec(query).all()

        return {
            "status": status.HTTP_200_OK if result else status.HTTP_404_NOT_FOUND,
            "pagina": page,
            "por_pagina": per_page,
            "total_registros": total_records,
            "total_paginas": total_pages,
            "dados": result if result else [],
            "mensagem": "Nenhum registro encontrado." if not result else "Sucesso."
        }

    except Exception as e:
        print(f"Erro na paginação: {str(e)}")
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "mensagem": "Erro interno no servidor."}
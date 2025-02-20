from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from typing import List, Optional
import uuid

class LivrosAutor(SQLModel, table=True):
    idLivro: uuid.UUID = Field(default = None, foreign_key="livros.idLivro", primary_key=True)
    idAutor: uuid.UUID = Field(default = None, foreign_key="autores.idAutor", primary_key=True)

class Autores(SQLModel, table=True):
    idAutor: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nome: str = Field(index=True)

    livros: List["Livros"] = Relationship(back_populates="autores", link_model=LivrosAutor)

class Editoras(SQLModel, table=True):
    idEditora: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nome: Optional[str] | None = None 

    livros: List["Livros"] = Relationship(back_populates="editora")



class Livros(SQLModel, table=True):
    idLivro: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    isbn: str = Field(index=True)
    titulo: str = Field(index=True)
    sinopse: Optional[str] | None = None
    editora: Optional[str] | None = None
    formato: Optional[str] | None = None
    ano: Optional[int] | None = None
    paginas: Optional[int] | None = None
    cover_url: Optional[str] | None = None

    autores: List["Autores"] = Relationship(back_populates="livros", link_model=LivrosAutor)
    idEditora: Optional[uuid.UUID] = Field(default=None, foreign_key="editoras.idEditora")
    editora: Optional["Editoras"] = Relationship(back_populates="livros")



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

database = create_engine(sqlite_url, echo=True)



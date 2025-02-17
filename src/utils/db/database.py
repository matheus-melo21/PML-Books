from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
import uuid

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


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)



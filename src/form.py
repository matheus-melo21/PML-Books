from typing import Optional
import uuid
from sqlmodel import SQLModel

class formLivroCadastro(SQLModel):
    
    isbn: str
    titulo: str
    sinopse: Optional[str] = None
    formato: Optional[str] = None
    ano: Optional[int] = None
    paginas: Optional[int] = None
    cover_url: Optional[str] = None
    idEditora: Optional[uuid.UUID] = None  # FK opcional
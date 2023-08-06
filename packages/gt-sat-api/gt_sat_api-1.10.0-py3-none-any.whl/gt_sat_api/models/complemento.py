from dataclasses import dataclass
from datetime import date


@dataclass
class Complemento:
    """Define los complementos para el DTE"""

    nombre: str
    uri: str
    regimen: bool
    no_origen: str
    fecha_origen: date
    descripcion: str
    type: str

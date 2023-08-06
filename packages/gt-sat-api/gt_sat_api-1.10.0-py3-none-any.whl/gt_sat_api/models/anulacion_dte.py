from dataclasses import dataclass
from datetime import datetime

from .emisor import Emisor
from .receptor import Receptor


@dataclass
class AnulacionDTE:
    """Agrupa la estructura para anular un DTE."""

    uuid: str
    emisor: Emisor
    receptor: Receptor
    fecha_hora_emision: datetime
    fecha_hora_anulacion: datetime
    motivo_anulacion: str

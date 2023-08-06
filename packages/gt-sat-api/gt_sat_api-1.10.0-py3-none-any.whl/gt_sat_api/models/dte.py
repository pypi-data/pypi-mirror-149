from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from .complemento import Complemento
from .emisor import Emisor
from .frase import Frase
from .item import Item
from .receptor import Receptor
from .total_impuesto import TotalImpuesto


@dataclass
class DTE:
    """Agrupa la estructura para un DTE."""

    clase_documento: str
    codigo_moneda: str
    fecha_hora_emision: datetime
    tipo: str
    NumeroAbono: int
    FechaVencimiento: datetime
    MontoAbono: int
    CondicionesPago: str
    Vencimiento: datetime
    NoOCCliente: int
    CodigoCliente: int
    Agente: str
    Transporte: str
    emisor: Emisor
    NoPedido: int
    FechaPedido: datetime
    modelo: str
    receptor: Receptor
    frases: List[Frase]
    items: List[Item]
    complementos: Optional[List[Complemento]] = None
    peq_contr: bool = False

    @property
    def total_impuestos(self) -> List[TotalImpuesto]:
        """Generate sum of monto_impuesto of Impuestos gropued by NombreCorto

        Returns:
            List[TotalImpuesto]
        """
        impuestos = (impuesto for item in self.items for impuesto in item.impuestos)
        _total_impuestos_dict: Dict[str, float] = {}
        for impuesto in impuestos:
            _total_impuestos_dict[impuesto.nombre_corto] = (
                _total_impuestos_dict.get(impuesto.nombre_corto, 0) + impuesto.monto_impuesto
            )
        _total_impuestos = [
            TotalImpuesto(nombre, monto) for nombre, monto in _total_impuestos_dict.items()
        ]
        return _total_impuestos

    @property
    def gran_total(self) -> float:
        """Get sum of total of the items

        Returns:
            float
        """
        _gran_total = sum([item.total for item in self.items])
        return _gran_total

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .impuesto import Impuesto


@dataclass
class Item:
    """Agrupa la información de un renglón o ítem de un DTE.

    Se refiere a lo que la Ley del IVA define como “concepto” en la venta de bienes o como
    “clase de servicio” en la prestación de servicios. También se refiere a lo que el
    Reglamento de la Ley del IVA indica como “detalle” o “descripción” de la venta, del
    servicio prestado o del arrendamiento."""

    bien_o_servicio: str
    numero_linea: int
    cantidad: float
    descripcion: str
    precio_unitario: float
    MontoGravable: float
    MontoImpuesto: float
    impuestos_rate: List[Tuple[List, float]]
    descuento_porcentual: float = 0.0
    unidad_medida: Optional[str] = None

    def __post_init__(self):
        self.impuestos = [
            Impuesto(
                nombre_corto=nombre,
                codigo_unidad_gravable=t[0],
                precio_neto=self.total,
            )
            for nombre, t in self.impuestos_rate.items()
        ]

    @property
    def total_impuestos(self) -> float:
        """Sum of monto_impuesto of impuestos

        Returns:
            float
        """
        _total_impuestos = sum([impuesto.monto_impuesto for impuesto in self.impuestos])
        return _total_impuestos

    @property
    def total(self) -> float:
        """Get real total based on precio, descuento and impuestos

        Returns:
            float
        """
        _total = self.precio - self.descuento
        return _total

    @property
    def precio(self) -> float:
        """get precio based on precio_unitario and cantidad

        Returns:
            float
        """
        _precio = self.precio_unitario * self.cantidad
        return _precio

    @property
    def descuento(self) -> float:
        """Get descuento based on descuento_porcentual and precio

        Returns:
            float
        """
        _descuento = self.precio * self.descuento_porcentual / 100
        return _descuento

from dataclasses import dataclass


@dataclass
class TotalImpuesto:
    """Agrupa los datos de cada impuesto."""

    nombre_corto: str
    total_monto_impuesto: float

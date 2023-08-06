from dataclasses import dataclass


@dataclass
class Impuesto:
    """Agrupa los datos de un Impuesto."""

    nombre_corto: str
    codigo_unidad_gravable: int
    precio_neto: float

    tax_percentage = 12.0

    @property
    def monto_gravable(self) -> float:
        """Get monto_gravable based on tax_percentage and precio_neto

        Returns:
            float
        """
        _monto_gravable = self.precio_neto / (1 + self.tax_percentage / 100)
        return _monto_gravable

    @property
    def monto_impuesto(self) -> float:
        """Get monto_impuesto based on precio_neto and monto_gravable

        Returns:
            float
        """
        _monto_impuesto = self.monto_gravable * self.tax_percentage / 100
        return _monto_impuesto

from importlib import resources

import jinja2

from .. import templates
from ..models.anulacion_dte import AnulacionDTE


def dte_to_xml_annulled(adte: AnulacionDTE) -> str:
    """Parse DTE python object to XML"""
    factura_template = resources.read_text(templates, "AnulacionDTE.xml.jinja")
    jinja_template = jinja2.Template(factura_template, trim_blocks=True, lstrip_blocks=True)
    return jinja_template.render(adte=adte) + "\n"

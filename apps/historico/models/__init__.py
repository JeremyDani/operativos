"""Exports para modelos del paquete `apps.historico.models`.

Reúne las importaciones de modelos usados en distintas partes
de la aplicación para facilitar accesos desde otras apps y
para documentar que estas entidades pertenecen al esquema
histórico (`historico`).
"""
from apps.operativos.models.nomina_entes import NominaEntes
from apps.operativos.models.vm_nomina import VmNomina
from apps.historico.models.participacion import Participacion

__all__ = [
	"NominaEntes",
	"VmNomina",
	"Participacion",
]
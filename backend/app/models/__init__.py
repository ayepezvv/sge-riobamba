from .permission import Permission
from .role import Role, role_permission
from .user import User
from .mixins import AuditLog, AuditMixin
from .parametro import ParametroSistema
from .territorio import Red, Sector, Ruta, Barrio, Calle
from .ciudadano import Ciudadano, ReferenciaCiudadano
from .comercial import Predio, Acometida, Cuenta, Medidor, HistorialMedidorCuenta, HistorialTarifaCuenta
from .contratacion import TipoProceso, PlantillaDocumento, ProcesoContratacion, DocumentoGenerado, PacAnual, ItemPac, ProcesoItemPacLink, HistoricoReformaPac, GenealogiaMontoPac, StatusItemPac
from .administrativo import (
    Direccion, Unidad, Puesto, TituloProfesional,
)
from .rrhh import (
    AreaOrganizacional, EscalaSalarial, Cargo,
    Empleado, EmpleadoCargaFamiliar, HistorialLaboral,
    ParametroCalculo, ImpuestoRentaEscala, RubroNomina, Contrato
)
from .informatica import SegmentoRed, DireccionIpAsignada
from .bodega import CategoriaBien, ActivoFijo, EstadoFisico

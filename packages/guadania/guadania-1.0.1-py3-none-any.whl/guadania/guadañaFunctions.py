from email import message
from xml.dom import NotFoundErr
from .prisma.prismaFunctions import PrismaSession
from . import prisma

import os
import datetime
import json
import pandas as pd

from functools import wraps
from openpyxl import load_workbook



def to_excel(dst: str, table: pd.DataFrame, append: bool = False):
    """
    Exporta a una tabla de excel. Puede escribir al final de una ya creada también.

    :param dst: Ruta de destino. Debe contener el nombre del archivo en ella. P.e.: "./excel.xlsx"
    :param table: Dataframe a exportar a excel
    :param append: Append to an already existing table.
    """

    if append and os.path.exists(dst):
        wb = load_workbook(dst)
        sheet = wb.worksheets[0]

        table.to_excel(dst, engine='openpyxl', startrow=sheet.max_row, index=False, header=False)

    else:
        table.to_excel(dst, engine='openpyxl',  index=False)


def cloud_accounts(prismasession) -> pd.DataFrame:
    """
    Obtiene un DataFrame con todas las cuentas del tenant.

    :param prismasession: datos de la sesión con el tenant (url, token)
    :return: DataFrame con cada una de las cuentas del tenant
    """

    res = prisma.list_cloud_accounts(prismasession)
    df = pd.json_normalize(res)
    orgs = df[df['numberOfChildAccounts'] > 0]
    pd.set_option('display.max_columns', None)

    for org, cloud in zip(list(orgs.accountId), list(orgs.cloudType)):
        childs = cloud_org_accounts(prismasession, cloud, org)
        df = pd.concat([df, childs])

    return df


def cloud_org_accounts(prismasession, cloud_type: str, id: str) -> pd.DataFrame:
    """
    Obtiene un DataFrame con todas las cuentas hijas de una organización.

    :param prismasession: datos de la sesión con el tenant (url, token)
    :param cloud_type: tipo de nube
    :param id: ID de la cuenta organización
    :return: DataFrame con cada una de las cuentas hijas de una organización
    """

    _cloud_type = cloud_type.lower()
    cloud_list = ['aws', 'azure', 'gpc', 'oci']
    if (_cloud_type in cloud_list):
        res = prisma.list_cloud_org_accounts(prismasession, _cloud_type, id)
        return pd.json_normalize(res)
    else:
        raise Exception('Error introduciendo tipo de nube. Valores aceptables: aws, azure, gcp, oci.')


def account_groups(prismasession, detailed=True) -> pd.DataFrame:
    """
    Obtiene un DataFrame con todas las account groups del tenant.

    :param detailed: True si queremos info detallada.
    :param prismasession: datos de la sesión con el tenant (url, token).
    :return: DataFrame con cada una de las account group del tenant.
    """

    res = prisma.list_account_groups(prismasession, detailed)
    return pd.json_normalize(res)


def compliance_sumary(prismasession: PrismaSession, standards: list[str]) -> pd.DataFrame:
    """
    Obtiene un DataFrame con el resumen de compliance de un compliance standard de Prisma.

    Obtiene: failedResources, passedResources, totalResources, highSeverityFailedResources,
    mediumSeverityFailedResources y lowSeverityFailedResources.

    :param prismaSession: datos de la sesión con el tenant (url, token).
    :param complianceStandard: Standards de los que se busca el compliance (una lista).
    :return: DataFrame con el resumen compliance.
    """

    tenantStandards = compliance_standards(prismasession)
    summaries = []
    for standard in standards:
        selected_id = tenantStandards[tenantStandards['name'] == standard]['id'].values[0]
        res = prisma.get_standard_compliance_statistics(prismasession, selected_id)
        res["summary"]["standard"] = standard
        summaries.append(res["summary"])

    return pd.json_normalize(summaries)


def resource_compliance(prismasession, complianceStandard) -> pd.DataFrame:
    """
    Obtiene un DataFrame con el compliance de cada resourceType de un compliance standard de Prisma.

    :param prismaSession: datos de la sesión con el tenant (url, token)
    :param complianceStandard: compliance standard del que se busca los resultados
    :return: DataFrame con compliance detallado por resource de un compliance standard de Prisma
    """

    standards = compliance_standards(prismasession)
    selected_id = standards.loc[standards['name'] == complianceStandard].head(1).iloc[0]['id']

    rawResponse = prisma.get_standard_compliance_statistics(prismasession, selected_id)

    res = []
    for summary in rawResponse["requirementSummaries"]:
        for section in summary["sectionSummaries"]:
            res.append(section)

    return pd.json_normalize(res)


def historic(prismasession: PrismaSession, complianceStandard: str, cloudAccounts: list[str] = None, accountGroups: list[str] = None) -> pd.DataFrame:
    """
    Obtiene un DataFrame con el historial de compliance de un compliance standard de Prisma.

    :param prismaSession: datos de la sesión con el tenant (url, token)
    :param complianceStandard: compliance standard del que se busca el compliance
    :param cloudAccounts: lista opcional con los id de los cloud accounts en caso de que se quiera separar el historico por cuentas. Sólo aplica si no se define 'accountGroups'.
    :param accountGroups: lista opcional con los names de los accountGroups en caso de que se quiera separar el historico por cuentas. Tiene preferencia sobre 'cloudAccounts'.
    :return: DataFrame con el historial de compliance de un compliance standard de Prisma
    """

    if accountGroups:
        res = pd.DataFrame()
        groupIDs = get_group_accounts_ids_by_names(prismasession, accountGroups)
        cloudAccountsDetails = prisma.list_cloud_accounts_names(prismasession, accountGroupIds=groupIDs)

        cloudAccountsNames = [account['name'] for account in cloudAccountsDetails]

        return historic(prismasession, complianceStandard, cloudAccountsNames)

    standards = compliance_standards(prismasession)
    selected_id = standards.loc[standards['name'] == complianceStandard].head(1).iloc[0]['id']

    if cloudAccounts:
        res = pd.DataFrame()
        for account in cloudAccounts:
            tmp = pd.json_normalize(prisma.get_standard_compliance_statistics_trend(prismasession, selected_id, account))
            tmp['AccountName'] = account
            res = pd.concat([res, tmp])

    else:
        res = pd.json_normalize(prisma.get_standard_compliance_statistics_trend(prismasession, selected_id))
        
    res['date'] = res.apply(lambda x: timestamp_to_date(x), 1)

    return res


def get_group_accounts_ids_by_names(prismaSession: PrismaSession, groupAccountNames: list[str]) -> str:
    ids = []
    res = prisma.list_account_groups(prismaSession)
    for group in res:
        if group['name'] in groupAccountNames:
            ids.append(group['id'])
    
    return ids


def timestamp_to_date(x):
    _x = json.loads(x.to_json())
    date = datetime.datetime.fromtimestamp(_x['timestamp']/1000).strftime("%d/%m/%Y")
    return date


def compliance_standards(prismasession) -> pd.DataFrame:
    """
    Obtiene un DataFrame con todos los Standards (compliance standards) de Prisma.

    :param prismaSession: datos de la sesión con el tenant (url, token)
    :return: DataFrame con cada uno de los standards de Prisma
    """

    res = prisma.list_compliance_standards(prismasession)
    return pd.json_normalize(res)


def standard_requirements(prismasession, complianceStandard) -> pd.DataFrame:
    """
    Obtiene todos los requerimientos de un compliance standard de Prisma.

    :param prismaSession: datos de la sesión con el tenant (url, token)
    :param complianceStandard: nombre del compliance standard
    :return: DataFrame con cada uno de los standards de Prisma
    """

    standards = compliance_standards(prismasession)
    try:
        selected_id = standards.loc[standards['name'] == complianceStandard].head(1).iloc[0]['id']
    except:
        raise Exception(
            "Error obteniendo requiermientos. Probablemente, nombre de complianceStandard incorrecto.")

    res = prisma.list_compliance_requirements(prismasession, selected_id)
    return pd.json_normalize(res)


def standards_sections(prismasession, complianceStandard, requirement_name) -> pd.DataFrame:
    """
    Obtiene todas las secciones de un compliance standard de Prisma.

    :param prismaSession: datos de la sesión con el tenant (url, token)
    :param compliance standard: nombre del compliance standard
    :param requirement_name: nombre del requerimiento
    :return: DataFrame con cada uno de las secciones de un requerimiento de Prisma
    """

    reqs = standard_requirements(prismasession, complianceStandard)
    try:
        req_id = reqs.loc[reqs['name'] == requirement_name].head(1).iloc[0]['id']
    except:
        raise Exception("Error obteniendo requiermientos. Probablemente, nombre de compliance standard incorrecto.")

    res = prisma.list_compliance_sections(prismasession, req_id)

    return pd.json_normalize(res)


def resources_usage_over_time(prismaSession, accounts_ids: list[str], start_date: str = None,
                              end_date: str = None) -> pd.DataFrame:
    """
    Obtiene un json con el uso de recursos licenciables sobre el tiempo. Si no se concreta fecha de inicio o fecha de final,
    se asume que se busca sin acotación de fechas. Para acotar, hay que definir ambas fechas, inicio y final.

    :param prismaSession: datos de la sesión con el tenant (url, token).
    :param accounts_ids: Lista con IDs de las suscripciones sobre las que obtener el uso.
    :param start_date: Fecha de inicio, en formato "dd/mm/yyyy". Por defecto, es el origen.
    :param end_date: Fecha de fin, en formato "dd/mm/yyyy". Por defecto, es hoy.
    :return: DataFrame con el uso de recursos licenciables sobre el tiempo.
    """

    time_range = None
    if (start_date != None and end_date != None):
        time_range = {
            "type": "absolute",
            "value": {
                "startTime": int(datetime.datetime.strptime(start_date, '%d/%m/%Y').timestamp() * 1000),
                "endTime": int(datetime.datetime.strptime(end_date, '%d/%m/%Y').timestamp() * 1000)
            }
        }

    res = prisma.resource_usage_over_time(
        prismaSession, accounts_ids, time_range)
    return pd.json_normalize(res)


def list_policies(prismaSession, complianceStandard) -> pd.DataFrame:
    """
    Obtiene un DataFrame con un listado de politicas para un Compliance standard.

    La API de prisma no permite listar políticas pasando cierto standard. En cambio,
    al listar políticas, en sus detalles aparece el standard al que pertenecen. Por lo tanto,
    se listan las politicas y comprobamos si el standard aparece en sus detalles. Una policy 
    puede pertenecer a varios standard.

    :param prismaSession: datos de la sesión con el tenant (url, token)
    :param complianceStandard: nombre del compliance standard de las politicas a buscar
    :return: DataFrame con un listado de politicas.
    """

    res = prisma.list_policies(prismaSession)
    res = pd.json_normalize(res)
    res['compliance-standard'] = res.apply(lambda x: list_policies_get_standard(x, complianceStandard), 1)
    res = res.loc[res['compliance-standard'] == complianceStandard]
    return res

# Con esta función podemos comprobar si la policy pertenece a un determinado compliance standard
def list_policies_get_standard(x, complianceStandard):
    _x = json.loads(x.to_json())

    if ('complianceMetadata' in _x.keys() and _x['complianceMetadata'] != None):
        for c in _x['complianceMetadata']:
            if (c['standardName'] == complianceStandard):
                return complianceStandard
        return ''
    else:
        return ''


def alerts(prismasession: prisma.PrismaSession, basic: bool = True, timeType: str = 'relative', timeAmount: str = '2',
           timeUnit: prisma.TimeUnit = prisma.TimeUnit.YEAR, detailed: bool = False, sortBy: str = None, offset: int = 0,
           alertId: str = None, alertStatus: prisma.AlertStatus = prisma.AlertStatus.OPEN, cloudAccount: str = None,
           cloudAccountId: str = None, accountGroup: str = None, cloudType: str = None, cloudRegion: str = None,
           cloudService: str = None, policyId: str = None, policyName: str = None, policySeverity: prisma.PolicySeverity = None,
           policyLabel: str = None, policyType: prisma.PolicyType = None, policyComplianceStandard: str = None, 
           policyComplianceRequirement: str = None, policyComplianceSection: str = None, policyRemediable: bool = None, 
           alertRuleName: str = None, resourceId: str = None, resourceName: str = None, resourceType: str = None):
    """
    Obtiene un DataFrame de alertas de Prisma paginada.

    :param prismaSession: datos de la sesión con el tenant (url, token).
    :param basic: Si queremos sólo los datos de alertas más básicos: id, status, alertTime, resource.resourceType, resource.cloudType, resource.account y policy.policyId.
        Por defecto está a True.
    :param detailed: True si queremos detalles de las alertas, False en caso contrario
    :param timeType: Tipo de tiempo, default 'relative'.
    :param timeAmount: Cantidad de tiempo, unidad definida en el parámetro timeUnit, default 30.
    :param timeUnit: Unidad de tiempo, default 'year'.
    :param detailed: Alerta detallada o no, default 'True'.
    :param sortBy: Ordenar las alertas. El formato del parámetro es PROPERTY:asc para ascendiente, PROPERTY:desc para descendiente. P.e.: sortBy=id:desc, sortBy=firstseen:asc, sortBy=lastseen:desc).
        Propiedades válidas: firstseen, lastseen, resource.regionid, alerttime, id, resource.accountid, status y resource.id.
    :param offset: Número de alertas que saltar (ignorar) en los resultados.
    :param limit: Número máximo de alertas, no más de 10000. Default 10000.
    :param pageToken: Identificador de la página de alertas, para cuando las alertas no caben en una respuesta.
    :param alertId: Alert ID.
    :param alertStatus: Enum AlertStatus.
    :param cloudAccount: Cloud account.
    :param cloudAccountId: ID de la cloud account.
    :param accountGroup: Account group.
    :param cloudType: Cloud type, enum CloudType.
    :param cloudRegion: Cloud region.
    :param cloudService: Cloud service.
    :param policyId: ID de la policy.
    :param policyName: Nombre de la policy.
    :param policySeverity: PolicySeverity enum.
    :param policyLabel: Label de la policy.
    :param policyType: PolicyType enum.
    :param policyComplianceRequirement: Nombre del Compliance Requirement.
    :param policyComplianceStandard: Si queremos filtrar por standard. También trae datos de las políticas asociadas a esas alertas.
    :param policyComplianceSection: ID del Compliance Section.
    :param policyRemediable: Bool. True es remediable, False no.
    :param alertRuleName: Nombre de la Alert Rule.
    :param resourceId: ID del resource.
    :param resourceName: Nombre del resource.
    :param resourceType: Tipo del resource.
    :return: DataFrame con las alertas del tenant
    """

    # Prisma devuelve muchísimos metadatos, vamos a quedarnos con los interesantes
    columns_base = ['id', 'status', 'alertTime', 'resource.resourceType', 'resource.cloudType', 'resource.account', 'policy.policyId']

    alerts = []
    nextPageToken = None
    looping = True
    while(looping):
        res = prisma.list_alerts_v2(prismasession, timeType=timeType, timeAmount=timeAmount, timeUnit=timeUnit, detailed=detailed, sortBy=sortBy, 
                                    offset=offset, limit=10000, pageToken=nextPageToken, alertId=alertId, alertStatus=alertStatus, 
                                    cloudAccount=cloudAccount, cloudAccountId=cloudAccountId, accountGroup=accountGroup, cloudType=cloudType, 
                                    cloudRegion=cloudRegion, cloudService=cloudService, policyId=policyId, policyName=policyName, 
                                    policySeverity=policySeverity, policyLabel=policyLabel, policyType=policyType, policyComplianceStandard=policyComplianceStandard, 
                                    policyComplianceRequirement=policyComplianceRequirement, policyComplianceSection=policyComplianceSection, 
                                    policyRemediable=policyRemediable, alertRuleName=alertRuleName, resourceId=resourceId, resourceName=resourceName, 
                                    resourceType=resourceType)

        alerts += res['items']
        if('nextPageToken' not in res.keys()):
            looping = False
        else:
            nextPageToken = res['nextPageToken']

    df = pd.json_normalize(alerts)
    if(not df.empty and basic):
        df = df[columns_base]

    if(not df.empty and policyComplianceStandard is not None):
        policies = list_policies(prismaSession=prismasession, complianceStandard=policyComplianceStandard)[['policyId', 'name', 'description', 'severity']]
        df = pd.merge(df, policies,  how='left', left_on=['policy.policyId'], right_on=['policyId'])    
    return df


def login(apiUrl: str = None, access_key_id: str = None, access_key_pass: str = None):
    """
    Login en la api de prisma para empezar a hacer querys.

    :param apiUrl: Cluster donde se encuentra Prisma
    :param access_key_id: Access Key ID
    :param access_key_pass: Access Key Pass
    :return: Objeto con los datos de sesión (url, token)
    """

    ps = prisma.prisma_login(apiUrl, access_key_id, access_key_pass)
    return ps

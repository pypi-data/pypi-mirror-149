# GUADAÑA

Libreria que matará vuestro sufrimiento por la PARCA

# TODOs (actualizado 09/02/2022)

## TODO de funcionalidad
- Añadir la función de POST para las alertas y así poder filtrar por timeRange, puesto que en el GET no te lo permite.
- Añadir una progress bar bonita
- Hay dos funciones de compliance, summary y details, añadir una tercera (consultar con pepe)
- Añadir parámetro a la función para cambiar el timestamp de formato y así poder elegir qué columna debe cambiar.
## TODO para datos de PowerBi
Se han definido los datos que debería descargarse la librería para la plantilla de powerBi genérica, estos excel serían:
- Licencias: Con las columnas acountId, accountName, exportationDate, una columna por cada recurso de la nube y otra columna con la suma de las licencias en esa fecha.
- Compliance: Con las columnas Framework, Section, Policy, Severity, Fails, Pass...
- Alertas: Colunas Alert ID, Policy Name, Policy Type, Description, Policy Labels, Policy Severity, Resource Name, Cloud Type, Cloud Account Id, Cloud Account Name, Region, Recommendation, Alert Status, Alert Time, Event Occurred, Dismissed On, Dismissal Reason, Resolved On, Resolution Reason, Resource ID.
- Excel para completar las alertas: Este excel serviría para saber a que frameworks pertenecen las alertas, con las columnas: Framework, RequirementId, RequirementName, SectionId, SectionName, PolicyName. La idea es relacionar el policyName de este excel con el policyName del excel de alertas.
## TODO PowerBi
- Hay que hacer la plantilla basandonos en el dashboard de Dufry y de Inditex
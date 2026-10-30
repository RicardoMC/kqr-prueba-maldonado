## Decisiones

    Se implementó la generación automática de SSCC GS1 de 18 dígitos.
    Se utiliza el dígito de extensión 0 y un prefijo GS1 configurable por compañía.
    Se definió una secuencia independiente para cada compañía.
    Se asumió que la compañía se determina según el origen del paquete, utilizando la compañía del entorno como alternativa.

## Uso de IA

    Se utilizó ChatGPT como apoyo para analizar la estructura del módulo, revisar código y proponer pruebas.
    Se revisaron y corrigieron las sugerencias antes de incorporarlas.
    Se validaron los cambios mediante las pruebas de Odoo y los controles de pre-commit.

## Pendientes

    No se identificaron pendientes funcionales para el alcance solicitado.
    Con más tiempo, se ampliarían las pruebas de concurrencia y los escenarios de generación en entornos multiempresa.

## Tests

    Comando ejecutado: invoke test -m rmc_sscc_palet
    Resultado: 3 pruebas ejecutadas, 0 fallidas y 0 errores.

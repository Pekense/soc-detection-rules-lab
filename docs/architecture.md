# Arquitectura del SOC Detection Rules Lab

Este documento describe la arquitectura lógica del laboratorio, el flujo de trabajo aplicado y cómo las reglas de detección se gestionan como código.

---

## Visión general

El proyecto implementa un flujo básico de Detection as Code para gestionar reglas Sigma en un repositorio versionado.

La idea principal es que cada regla de detección pase por un proceso controlado antes de llegar a la rama principal.

```text
Analista SOC / Detection Engineer
        ↓
Nueva regla Sigma
        ↓
Rama feature
        ↓
Validación local
        ↓
Commit y push
        ↓
Pull Request
        ↓
Pipeline CI
        ↓
Revisión
        ↓
Merge a main
```

---

## Componentes principales

| Componente                             | Descripción                                                               |
| -------------------------------------- | ------------------------------------------------------------------------- |
| `rules/`                               | Directorio donde se almacenan las reglas Sigma organizadas por plataforma |
| `pipelines/validate_sigma.py`          | Script Python que valida campos obligatorios de cada regla                |
| `.github/workflows/validate-sigma.yml` | Pipeline CI que ejecuta la validación automática                          |
| `docs/`                                | Documentación técnica del proyecto                                        |
| `README.md`                            | Presentación general del laboratorio                                      |

---

## Flujo de validación

Cada vez que se crea o modifica una regla Sigma, el proceso esperado es:

```text
Crear/modificar regla
        ↓
Ejecutar validación local
        ↓
Subir rama a GitHub
        ↓
GitHub Actions ejecuta el pipeline
        ↓
Si pasa: la PR puede revisarse y mergearse
        ↓
Si falla: la regla debe corregirse
```

---

## Validación local

Antes de subir cambios, se recomienda ejecutar:

```bash
python pipelines/validate_sigma.py
```

El validador comprueba que cada regla incluya los campos mínimos:

```text
title
id
status
description
author
logsource
detection
level
```

Si falta alguno, el script devuelve error y termina con código distinto de cero.

---

## Pipeline CI

El workflow de GitHub Actions se ejecuta en:

* Push a `main`.
* Push a ramas `feature/**`.
* Pull Requests hacia `main`.

El pipeline realiza estos pasos:

```text
Checkout del repositorio
        ↓
Instalación de Python
        ↓
Instalación de dependencias
        ↓
Ejecución del validador
        ↓
Resultado verde o rojo
```

---

## Modelo de ramas

El proyecto sigue un flujo simple basado en ramas:

| Rama        | Uso                              |
| ----------- | -------------------------------- |
| `main`      | Rama principal estable           |
| `feature/*` | Nuevas reglas o funcionalidades  |
| `docs/*`    | Cambios de documentación         |
| `test/*`    | Pruebas controladas del pipeline |

No se recomienda trabajar directamente sobre `main`.

---

## Integración futura con SIEM

En una fase posterior, las reglas Sigma podrían convertirse a consultas específicas para diferentes SIEM:

| Plataforma         | Lenguaje           |
| ------------------ | ------------------ |
| Microsoft Sentinel | KQL                |
| Splunk             | SPL                |
| QRadar             | AQL                |
| Elastic            | Lucene / EQL / KQL |

El objetivo futuro sería añadir una fase de conversión o exportación automática.

```text
Regla Sigma
    ↓
Conversor
    ↓
Consulta SIEM
    ↓
Despliegue o documentación
```

---

## Integración futura con SOAR

El proyecto también puede evolucionar hacia automatización de respuesta:

```text
Detección Sigma
        ↓
Alerta SIEM
        ↓
Playbook SOAR
        ↓
Enriquecimiento
        ↓
Decisión
        ↓
Respuesta automatizada o ticket
```

Ejemplos de acciones futuras:

* Enriquecer IPs con inteligencia de amenazas.
* Consultar reputación de hashes.
* Abrir ticket automático.
* Notificar a un canal operativo.
* Ejecutar contención en endpoint mediante EDR/XDR.

---

## Valor arquitectónico

Este laboratorio demuestra una forma profesional de gestionar detecciones SOC:

```text
Detecciones como código
Control de versiones
Validación automática
Pull Requests
Trazabilidad
Base para SIEM/SOAR
```

El objetivo no es solo escribir reglas, sino construir un flujo repetible, auditable y ampliable.

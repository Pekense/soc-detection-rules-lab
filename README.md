# SOC Detection Rules Lab

Repositorio de laboratorio para gestionar reglas de detección SOC como código, usando reglas Sigma, control de versiones con Git y validación automática mediante CI/CD.

El objetivo del proyecto es simular un flujo profesional de trabajo donde las detecciones de seguridad se crean, revisan, versionan y validan antes de integrarse en la rama principal.

---

## Objetivos del proyecto

* Crear un repositorio estructurado de reglas de detección SOC.
* Gestionar reglas Sigma mediante Git y Pull Requests.
* Validar reglas automáticamente con un pipeline CI.
* Organizar detecciones por plataforma: Windows, Linux y Cloud.
* Aplicar buenas prácticas de Detection Engineering y DevSecOps.
* Construir una base ampliable para futuras integraciones con SIEM, SOAR y automatización.

---

## Tecnologías utilizadas

| Tecnología     | Uso                                       |
| -------------- | ----------------------------------------- |
| Sigma          | Formato estándar para reglas de detección |
| Python         | Validación automática de reglas           |
| PyYAML         | Lectura y análisis de ficheros YAML       |
| Git            | Control de versiones                      |
| GitHub         | Repositorio remoto y Pull Requests        |
| GitHub Actions | Pipeline CI para validación automática    |
| MITRE ATT&CK   | Mapeo de técnicas de ataque               |

---

## Estructura del repositorio

```text
soc-detection-rules-lab/
├── README.md
├── rules/
│   ├── windows/
│   │   └── suspicious_powershell.yml
│   ├── linux/
│   │   └── privilege_escalation.yml
│   └── cloud/
│       └── aws_failed_login.yml
├── pipelines/
│   └── validate_sigma.py
├── docs/
│   ├── architecture.md
│   └── detection-lifecycle.md
└── .github/
    └── workflows/
        └── validate-sigma.yml
```

---

## Reglas incluidas

| Plataforma | Regla                              | Objetivo                                              |
| ---------- | ---------------------------------- | ----------------------------------------------------- |
| Windows    | Suspicious PowerShell Execution    | Detectar ejecución sospechosa de PowerShell           |
| Linux      | Linux Privilege Escalation Attempt | Detectar posibles intentos de escalada de privilegios |
| AWS        | AWS Console Failed Login           | Detectar fallos de autenticación en consola AWS       |

---

## Validación local

Instalar dependencias:

```bash
pip install pyyaml
```

Ejecutar validador:

```bash
python pipelines/validate_sigma.py
```

Resultado esperado:

```text
Validando: rules/windows/suspicious_powershell.yml
OK: rules/windows/suspicious_powershell.yml
Validando: rules/linux/privilege_escalation.yml
OK: rules/linux/privilege_escalation.yml
Validando: rules/cloud/aws_failed_login.yml
OK: rules/cloud/aws_failed_login.yml
Todas las reglas Sigma son válidas.
```

---

## Pipeline CI/CD

El repositorio incluye un workflow de GitHub Actions que valida automáticamente las reglas Sigma en:

* Push a `main`.
* Push a ramas `feature/**`.
* Pull Requests hacia `main`.

Workflow:

```text
.github/workflows/validate-sigma.yml
```

El pipeline instala Python, descarga las dependencias necesarias y ejecuta el validador:

```bash
python pipelines/validate_sigma.py
```

Si una regla no contiene campos obligatorios, el pipeline falla y evita que el cambio sea integrado sin revisión.

---

## Campos obligatorios validados

Cada regla Sigma debe contener como mínimo:

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

---

## Flujo de trabajo recomendado

Crear una rama nueva:

```bash
git checkout -b feature/add-new-detection-rule
```

Añadir o modificar reglas.

Validar en local:

```bash
python pipelines/validate_sigma.py
```

Guardar cambios:

```bash
git add .
git commit -m "feat: add new sigma detection rule"
git push -u origin feature/add-new-detection-rule
```

Crear Pull Request hacia `main`.

---

## Valor para SOC

Este proyecto permite aplicar un enfoque de Detection as Code:

```text
Reglas de detección
↓
Control de versiones
↓
Validación automática
↓
Pull Request
↓
Integración controlada en main
```

Esto ayuda a reducir errores, mejorar la trazabilidad y mantener un catálogo de detecciones reutilizable y auditable.

---

## Próximas mejoras

* Añadir más reglas Sigma por plataforma.
* Añadir validación avanzada de sintaxis Sigma.
* Convertir reglas Sigma a consultas para SIEM.
* Añadir integración con Elastic, Sentinel o Splunk.
* Incorporar pruebas automatizadas.
* Añadir detecciones basadas en MITRE ATT&CK.
* Preparar integración futura con SOAR.
* Añadir generación automática de documentación.

---

## Autor

Proyecto creado por Rafa como laboratorio práctico de Detection Engineering, SOC Automation y DevSecOps.

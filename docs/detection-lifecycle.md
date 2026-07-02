# Ciclo de vida de una detección SOC

Este documento describe el ciclo de vida de una regla de detección dentro del laboratorio SOC Detection Rules Lab.

El objetivo es representar un flujo profesional donde una detección no se crea de forma aislada, sino que pasa por fases de análisis, diseño, validación, revisión y mejora continua.

---

## 1. Identificación del caso de uso

Toda detección debe comenzar con una necesidad clara.

Ejemplos:

* Detectar ejecución sospechosa de PowerShell.
* Detectar intentos de escalada de privilegios en Linux.
* Detectar fallos de autenticación en AWS.
* Detectar comportamiento anómalo en identidades cloud.
* Detectar actividad relacionada con técnicas MITRE ATT&CK.

Preguntas clave:

```text
¿Qué comportamiento quiero detectar?
¿Qué logs necesito?
¿Qué riesgo cubre?
¿Qué técnica MITRE ATT&CK está relacionada?
¿Qué falsos positivos puedo esperar?
```

---

## 2. Definición de la lógica de detección

Una vez identificado el caso de uso, se define la lógica.

Ejemplo:

```text
Si el proceso ejecutado termina en powershell.exe
Y la línea de comandos contiene -enc, -nop, IEX o DownloadString
Entonces generar una alerta de severidad alta
```

Esta lógica debe ser clara, entendible y revisable por otro analista.

---

## 3. Creación de la regla Sigma

La lógica se convierte en una regla Sigma dentro del directorio correspondiente:

```text
rules/windows/
rules/linux/
rules/cloud/
```

Ejemplo de estructura básica:

```yaml
title: Suspicious PowerShell Execution
id: 10000001-0000-0000-0000-000000000001
status: experimental
description: Detecta ejecución sospechosa de PowerShell.
author: Rafa
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image|endswith: '\powershell.exe'
    CommandLine|contains:
      - '-enc'
      - '-nop'
  condition: selection
level: high
```

---

## 4. Validación local

Antes de subir una regla al repositorio remoto, se ejecuta la validación local:

```bash
python pipelines/validate_sigma.py
```

El validador comprueba que cada regla contiene los campos mínimos obligatorios:

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

Si falta algún campo, la validación falla.

---

## 5. Control de versiones

Cada cambio debe realizarse en una rama específica.

Ejemplo:

```bash
git checkout -b feature/add-new-sigma-rule
```

Después se revisan los cambios:

```bash
git status
git diff
```

Y se crea un commit claro:

```bash
git add .
git commit -m "feat: add new sigma detection rule"
```

---

## 6. Pull Request

La regla no se integra directamente en `main`.

Primero se crea una Pull Request para revisar:

* Lógica de detección.
* Campos Sigma.
* Severidad.
* Posibles falsos positivos.
* Mapeo MITRE ATT&CK.
* Resultado del pipeline CI.

La Pull Request permite trazabilidad y revisión antes del merge.

---

## 7. Validación automática CI/CD

Al subir la rama, GitHub Actions ejecuta el pipeline automáticamente.

Flujo:

```text
Push a rama
    ↓
GitHub Actions
    ↓
Instala Python
    ↓
Instala dependencias
    ↓
Ejecuta validate_sigma.py
    ↓
Devuelve resultado verde o rojo
```

Si el pipeline falla, la regla debe corregirse antes de integrarse.

---

## 8. Integración en main

Cuando la Pull Request está revisada y el pipeline está en verde, se puede hacer merge hacia `main`.

La rama `main` representa el catálogo estable de detecciones.

---

## 9. Revisión y mejora continua

Una detección no termina cuando se integra.

Debe revisarse con el tiempo según:

* Nuevas técnicas de ataque.
* Cambios en los logs disponibles.
* Falsos positivos detectados.
* Cambios en la infraestructura.
* Nuevas fuentes de inteligencia de amenazas.
* Cambios en MITRE ATT&CK.

Posibles acciones:

```text
Ajustar condiciones
Añadir excepciones
Cambiar severidad
Añadir nuevas fuentes de log
Convertir la regla a consultas SIEM
Asociar playbooks SOAR
```

---

## 10. Flujo completo resumido

```text
Caso de uso
    ↓
Análisis de logs
    ↓
Lógica de detección
    ↓
Regla Sigma
    ↓
Validación local
    ↓
Commit
    ↓
Pull Request
    ↓
Pipeline CI
    ↓
Revisión
    ↓
Merge a main
    ↓
Monitorización y mejora continua
```

---

## Valor para SOC

Este ciclo permite aplicar Detection Engineering de forma profesional:

* Las detecciones son versionadas.
* Los cambios son revisables.
* La calidad se valida automáticamente.
* La documentación mejora la trazabilidad.
* El catálogo puede evolucionar hacia SIEM, SOAR y automatización.

El objetivo final es construir detecciones útiles, mantenibles y alineadas con riesgos reales.

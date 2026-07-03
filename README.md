# SOC Detection Rules Lab

Repositorio de laboratorio para gestionar reglas de detección SOC como código, usando reglas Sigma, control de versiones con Git y validación automática mediante CI/CD.

El objetivo del proyecto es simular un flujo profesional donde las detecciones de seguridad se crean, revisan, versionan y validan antes de integrarse en la rama principal.

---

## Objetivos del proyecto

- Crear un repositorio estructurado de reglas de detección SOC.
- Gestionar reglas Sigma mediante Git y Pull Requests.
- Validar reglas automáticamente con un pipeline CI.
- Organizar detecciones por plataforma: Windows, Linux y Cloud.
- Aplicar buenas prácticas de Detection Engineering y DevSecOps.
- Construir una base ampliable para futuras integraciones con SIEM, SOAR y automatización.

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Sigma | Formato estándar para reglas de detección |
| Python | Validación automática de reglas |
| PyYAML | Lectura y análisis de ficheros YAML |
| Git | Control de versiones |
| GitHub | Repositorio remoto y Pull Requests |
| GitHub Actions | Pipeline CI para validación automática |
| MITRE ATT&CK | Mapeo de técnicas de ataque |

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

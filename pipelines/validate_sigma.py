#!/usr/bin/env python3

"""
Validador de reglas Sigma.

Comprueba que todos los ficheros YAML dentro de rules/
contienen los campos mínimos, valores esperados y estructura básica.
"""

from pathlib import Path
import sys
import yaml


REQUIRED_FIELDS = [
    "title",
    "id",
    "status",
    "description",
    "author",
    "logsource",
    "detection",
    "level",
]

VALID_STATUS = {
    "stable",
    "test",
    "experimental",
    "deprecated",
    "unsupported",
}

VALID_LEVELS = {
    "informational",
    "low",
    "medium",
    "high",
    "critical",
}


def validate_required_fields(rule: dict, file_path: Path) -> bool:
    """Valida que existan los campos obligatorios."""
    missing_fields = [field for field in REQUIRED_FIELDS if field not in rule]

    if missing_fields:
        print(f"ERROR: {file_path} no tiene estos campos obligatorios: {missing_fields}")
        return False

    return True


def validate_non_empty_values(rule: dict, file_path: Path) -> bool:
    """Valida que los campos obligatorios no estén vacíos."""
    for field in REQUIRED_FIELDS:
        value = rule.get(field)

        if value in ("", None, [], {}):
            print(f"ERROR: {file_path} tiene el campo vacío: {field}")
            return False

    return True


def validate_status(rule: dict, file_path: Path) -> bool:
    """Valida el campo status."""
    status = rule.get("status")

    if status not in VALID_STATUS:
        print(
            f"ERROR: {file_path} tiene status inválido: {status}. "
            f"Valores válidos: {sorted(VALID_STATUS)}"
        )
        return False

    return True


def validate_level(rule: dict, file_path: Path) -> bool:
    """Valida el campo level."""
    level = rule.get("level")

    if level not in VALID_LEVELS:
        print(
            f"ERROR: {file_path} tiene level inválido: {level}. "
            f"Valores válidos: {sorted(VALID_LEVELS)}"
        )
        return False

    return True


def validate_logsource(rule: dict, file_path: Path) -> bool:
    """Valida que logsource tenga estructura de diccionario."""
    logsource = rule.get("logsource")

    if not isinstance(logsource, dict):
        print(f"ERROR: {file_path} tiene logsource inválido. Debe ser un diccionario.")
        return False

    return True


def validate_detection(rule: dict, file_path: Path) -> bool:
    """Valida que detection tenga estructura mínima."""
    detection = rule.get("detection")

    if not isinstance(detection, dict):
        print(f"ERROR: {file_path} tiene detection inválido. Debe ser un diccionario.")
        return False

    if "condition" not in detection:
        print(f"ERROR: {file_path} no tiene detection.condition.")
        return False

    return True


def validate_rule(file_path: Path) -> bool:
    """Valida una regla Sigma individual."""
    print(f"Validando: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            rule = yaml.safe_load(file)
    except yaml.YAMLError as error:
        print(f"ERROR YAML en {file_path}: {error}")
        return False
    except Exception as error:
        print(f"ERROR leyendo {file_path}: {error}")
        return False

    if not isinstance(rule, dict):
        print(f"ERROR: {file_path} no contiene un YAML válido tipo diccionario.")
        return False

    validations = [
        validate_required_fields(rule, file_path),
        validate_non_empty_values(rule, file_path),
        validate_status(rule, file_path),
        validate_level(rule, file_path),
        validate_logsource(rule, file_path),
        validate_detection(rule, file_path),
    ]

    if all(validations):
        print(f"OK: {file_path}")
        return True

    return False


def main() -> int:
    """Busca y valida todas las reglas Sigma."""
    rules_path = Path("rules")

    if not rules_path.exists():
        print("ERROR: no existe el directorio rules/")
        return 1

    rule_files = sorted(
        list(rules_path.rglob("*.yml")) + list(rules_path.rglob("*.yaml"))
    )

    if not rule_files:
        print("ERROR: no se han encontrado reglas Sigma.")
        return 1

    results = [validate_rule(file_path) for file_path in rule_files]

    if all(results):
        print("Todas las reglas Sigma son válidas.")
        return 0

    print("Una o más reglas Sigma no son válidas.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

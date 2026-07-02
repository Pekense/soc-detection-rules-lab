#!/usr/bin/env python3

"""
Validador básico de reglas Sigma.

Comprueba que todos los ficheros YAML dentro de rules/
contienen los campos mínimos necesarios para una regla Sigma.
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

    missing_fields = [field for field in REQUIRED_FIELDS if field not in rule]

    if missing_fields:
        print(f"ERROR: {file_path} no tiene estos campos obligatorios: {missing_fields}")
        return False

    print(f"OK: {file_path}")
    return True


def main() -> int:
    """Busca y valida todas las reglas Sigma."""
    rules_path = Path("rules")

    if not rules_path.exists():
        print("ERROR: no existe el directorio rules/")
        return 1

    rule_files = list(rules_path.rglob("*.yml")) + list(rules_path.rglob("*.yaml"))

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

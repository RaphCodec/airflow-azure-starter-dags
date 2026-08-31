"""
Helper utilities for DAG generation.

This module provides functions for validating and generating task IDs,
DAG IDs, and other identifiers that follow domain-based naming conventions.
"""

import re


class TaskIdError(Exception):
    """Exception raised for invalid task IDs."""

    pass


def normalize_identifier(text: str) -> str:
    """
    Normalize an identifier to lowercase, replacing spaces and hyphens with underscores.

    Args:
        text: The identifier text to normalize.

    Returns:
        Normalized identifier string.

    Raises:
        ValueError: If the input is empty or contains only invalid characters.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Identifier must be a non-empty string")

    # Convert to lowercase
    normalized = text.lower()

    # Replace spaces and hyphens with underscores
    normalized = re.sub(r"[\s\-]+", "_", normalized)

    # Remove or replace invalid characters (keep only lowercase letters, digits, underscores)
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)

    # Collapse repeated underscores
    normalized = re.sub(r"_+", "_", normalized)

    # Remove leading/trailing underscores
    normalized = normalized.strip("_")

    if not normalized:
        raise ValueError("Identifier contains no valid characters after normalization")

    return normalized


def validate_airflow_id(task_id: str) -> bool:
    """
    Validate that a string is a valid Airflow task/DAG ID.

    Airflow IDs must:
    - Be between 1 and 250 characters
    - Contain only lowercase letters, digits, hyphens, underscores, and dots
    - Start with a letter or underscore
    - Not contain consecutive dots or underscores (per best practices)

    Args:
        task_id: The ID to validate.

    Returns:
        True if the ID is valid, False otherwise.
    """
    if not task_id or len(task_id) > 250:
        return False

    # Check for valid characters
    if not re.match(r"^[a-z0-9_\-\.]+$", task_id):
        return False

    # Check that it starts with letter or underscore
    if not re.match(r"^[a-z_]", task_id):
        return False

    return True


def generate_task_id(domain: str, action: str, obj: str | None = None) -> str:
    """
    Generate a domain-based task ID.

    Task IDs follow the pattern: <domain>_<action>_<object>
    or <domain>_<action> if no object is specified.

    Args:
        domain: The domain (e.g., 'sales', 'finance').
        action: The action (e.g., 'extract', 'validate', 'load').
        obj: The object (e.g., 'orders', 'transactions'). Optional.

    Returns:
        A valid Airflow task ID.

    Raises:
        TaskIdError: If the generated ID is invalid or too long.
    """
    if not domain or not action:
        raise TaskIdError("Domain and action are required")

    # Normalize all parts
    domain = normalize_identifier(domain)
    action = normalize_identifier(action)

    if obj:
        obj = normalize_identifier(obj)
        task_id = f"{domain}_{action}_{obj}"
    else:
        task_id = f"{domain}_{action}"

    # Validate the result
    if not validate_airflow_id(task_id):
        raise TaskIdError(
            f"Generated task ID '{task_id}' is invalid. "
            f"Must be 1-250 chars, start with letter/underscore, "
            f"contain only lowercase letters, digits, hyphens, underscores, dots."
        )

    if len(task_id) > 250:
        raise TaskIdError(f"Generated task ID '{task_id}' exceeds 250 character limit")

    return task_id


def validate_unique_task_ids(task_ids: list[str]) -> None:
    """
    Validate that task IDs within a list are unique.

    Args:
        task_ids: List of task IDs to check.

    Raises:
        TaskIdError: If duplicate task IDs are found.
    """
    seen: set[str] = set()
    duplicates: set[str] = set()

    for task_id in task_ids:
        if task_id in seen:
            duplicates.add(task_id)
        seen.add(task_id)

    if duplicates:
        raise TaskIdError(f"Duplicate task IDs found: {', '.join(sorted(duplicates))}")


def generate_dag_id(domain: str, name: str, dag_type: str) -> str:
    """
    Generate a DAG ID following domain-based naming.

    DAG IDs follow the pattern: <domain>_<name>_<type>

    Args:
        domain: The domain (e.g., 'sales').
        name: The DAG name (e.g., 'orders').
        dag_type: The DAG type (e.g., 'ingestion', 'processing', 'orchestration').

    Returns:
        A valid Airflow DAG ID.

    Raises:
        TaskIdError: If the generated ID is invalid.
    """
    if not domain or not name or not dag_type:
        raise TaskIdError("Domain, name, and type are required")

    # Normalize all parts
    domain = normalize_identifier(domain)
    name = normalize_identifier(name)
    dag_type = normalize_identifier(dag_type)

    dag_id = f"{domain}_{name}_{dag_type}"

    if not validate_airflow_id(dag_id):
        raise TaskIdError(f"Generated DAG ID '{dag_id}' is invalid")

    if len(dag_id) > 250:
        raise TaskIdError(f"Generated DAG ID '{dag_id}' exceeds 250 character limit")

    return dag_id

from typing import Optional


class ResourceNotFoundError(Exception):
    """Raised when a domain entity cannot be resolved (maps to HTTP 404)."""

    def __init__(self, resource_type: str, identifier: str, suggestion: Optional[str] = None) -> None:
        self.resource_type = resource_type
        self.identifier = identifier
        self.suggestion = suggestion
        message = f"{resource_type} not found: {identifier}"
        if suggestion:
            message = f"{message}. {suggestion}"
        super().__init__(message)

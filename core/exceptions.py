class ResourceNotFoundError(Exception):
    """Raised when a domain entity cannot be resolved (maps to HTTP 404)."""

    def __init__(self, resource_type: str, identifier: str) -> None:
        self.resource_type = resource_type
        self.identifier = identifier
        super().__init__(f"{resource_type} not found: {identifier}")

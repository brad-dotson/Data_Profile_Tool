class DataProfileError(Exception):
    """Expected user-facing failure."""


class UserError(DataProfileError):
    """A problem the user can correct without debugging the application."""


class ConfigurationError(DataProfileError):
    """Invalid or incompatible project configuration."""


class SourceError(DataProfileError):
    """Unreadable, unsupported, or ambiguous source data."""

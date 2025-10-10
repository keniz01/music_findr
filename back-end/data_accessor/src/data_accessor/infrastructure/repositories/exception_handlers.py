import logging

from ...domain.exceptions.sql_statement_execution_exception import SqlStatementExecutionException


def raise_sql_execution_exception(
    message: str, error: Exception, include_traceback: bool = False
) -> None:
    """
    Raises a SqlStatementExecutionException with formatted error message and optional traceback.

    Args:
        message (str): Contextual message about the error.
        error (Exception): The caught exception.
        include_traceback (bool): If True, appends the full traceback to the message.
    """
    root_cause = error.__cause__ or error
    formatted_message = f"""
[SqlStatementExecutionException]
{message}
↳ Caused by {type(root_cause).__name__}: {root_cause}
""".strip()

    logging.error(message, exc_info=True)
    raise SqlStatementExecutionException(formatted_message) from error

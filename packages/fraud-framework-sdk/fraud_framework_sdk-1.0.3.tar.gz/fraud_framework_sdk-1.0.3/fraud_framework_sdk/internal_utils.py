import platform
import sys
from typing import Optional

from fraud_framework_sdk import __version__


def get_user_agent(prefix: Optional[str] = None, suffix: Optional[str] = None):
    """Construct the user-agent header with the package info,
    Python version and OS version.
    Returns:
        The user agent string.
        e.g. 'Python/3.8.6 FraudClient/2.0.0 Darwin/17.7.0'
    """
    client = f"fraud_framework_sdk/{__version__}"
    python_version = "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info)
    system_info = f"{platform.system()}/{platform.release()}"
    user_agent_string = " ".join([python_version, client, system_info])
    prefix = f"{prefix} " if prefix else ""
    suffix = f" {suffix}" if suffix else ""
    return prefix + user_agent_string + suffix


def _build_unexpected_body_error_message(body: str) -> str:
    body_for_logging = "".join([line.strip() for line in body.replace("\r", "\n").split("\n")])
    if len(body_for_logging) > 100:
        body_for_logging = body_for_logging[:100] + "..."
    message = f"Received a response in a non-JSON format: {body_for_logging}"
    return message


def _modify_params_for_logging(values: Optional[dict]) -> dict:
    if not values or not isinstance(values, dict):
        return {}
    return {k: ("(bytes)" if isinstance(v, bytes) else v) for k, v in values.items()}

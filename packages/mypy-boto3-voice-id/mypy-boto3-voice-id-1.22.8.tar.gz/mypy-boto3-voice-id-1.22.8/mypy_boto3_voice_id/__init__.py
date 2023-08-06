"""
Main interface for voice-id service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_voice_id import (
        Client,
        VoiceIDClient,
    )

    session = Session()
    client: VoiceIDClient = session.client("voice-id")
    ```
"""
from .client import VoiceIDClient

Client = VoiceIDClient


__all__ = ("Client", "VoiceIDClient")

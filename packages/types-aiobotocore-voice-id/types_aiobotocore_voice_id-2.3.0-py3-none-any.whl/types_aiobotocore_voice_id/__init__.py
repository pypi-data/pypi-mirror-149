"""
Main interface for voice-id service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_voice_id import (
        Client,
        VoiceIDClient,
    )

    session = get_session()
    async with session.create_client("voice-id") as client:
        client: VoiceIDClient
        ...

    ```
"""
from .client import VoiceIDClient

Client = VoiceIDClient


__all__ = ("Client", "VoiceIDClient")

"""
Main interface for compute-optimizer service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_compute_optimizer import (
        Client,
        ComputeOptimizerClient,
    )

    session = get_session()
    async with session.create_client("compute-optimizer") as client:
        client: ComputeOptimizerClient
        ...

    ```
"""
from .client import ComputeOptimizerClient

Client = ComputeOptimizerClient

__all__ = ("Client", "ComputeOptimizerClient")

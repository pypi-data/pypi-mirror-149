"""
Type annotations for schemas service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_schemas.client import SchemasClient
    from types_aiobotocore_schemas.waiter import (
        CodeBindingExistsWaiter,
    )

    session = get_session()
    async with session.create_client("schemas") as client:
        client: SchemasClient

        code_binding_exists_waiter: CodeBindingExistsWaiter = client.get_waiter("code_binding_exists")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CodeBindingExistsWaiter",)

class CodeBindingExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas.Waiter.CodeBindingExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/waiters/#codebindingexistswaiter)
    """

    async def wait(
        self,
        *,
        Language: str,
        RegistryName: str,
        SchemaName: str,
        SchemaVersion: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas.Waiter.CodeBindingExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/waiters/#codebindingexistswaiter)
        """

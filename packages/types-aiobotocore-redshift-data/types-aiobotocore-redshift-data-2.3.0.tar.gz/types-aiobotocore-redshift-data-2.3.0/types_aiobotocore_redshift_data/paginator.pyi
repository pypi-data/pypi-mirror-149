"""
Type annotations for redshift-data service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_redshift_data.client import RedshiftDataAPIServiceClient
    from types_aiobotocore_redshift_data.paginator import (
        DescribeTablePaginator,
        GetStatementResultPaginator,
        ListDatabasesPaginator,
        ListSchemasPaginator,
        ListStatementsPaginator,
        ListTablesPaginator,
    )

    session = get_session()
    with session.create_client("redshift-data") as client:
        client: RedshiftDataAPIServiceClient

        describe_table_paginator: DescribeTablePaginator = client.get_paginator("describe_table")
        get_statement_result_paginator: GetStatementResultPaginator = client.get_paginator("get_statement_result")
        list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
        list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
        list_statements_paginator: ListStatementsPaginator = client.get_paginator("list_statements")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import StatusStringType
from .type_defs import (
    DescribeTableResponseTypeDef,
    GetStatementResultResponseTypeDef,
    ListDatabasesResponseTypeDef,
    ListSchemasResponseTypeDef,
    ListStatementsResponseTypeDef,
    ListTablesResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeTablePaginator",
    "GetStatementResultPaginator",
    "ListDatabasesPaginator",
    "ListSchemasPaginator",
    "ListStatementsPaginator",
    "ListTablesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeTablePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.DescribeTable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#describetablepaginator)
    """

    def paginate(
        self,
        *,
        Database: str,
        ClusterIdentifier: str = ...,
        ConnectedDatabase: str = ...,
        DbUser: str = ...,
        Schema: str = ...,
        SecretArn: str = ...,
        Table: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeTableResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.DescribeTable.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#describetablepaginator)
        """

class GetStatementResultPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.GetStatementResult)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#getstatementresultpaginator)
    """

    def paginate(
        self, *, Id: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetStatementResultResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.GetStatementResult.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#getstatementresultpaginator)
        """

class ListDatabasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListDatabases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#listdatabasespaginator)
    """

    def paginate(
        self,
        *,
        Database: str,
        ClusterIdentifier: str = ...,
        DbUser: str = ...,
        SecretArn: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDatabasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListDatabases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#listdatabasespaginator)
        """

class ListSchemasPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListSchemas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#listschemaspaginator)
    """

    def paginate(
        self,
        *,
        Database: str,
        ClusterIdentifier: str = ...,
        ConnectedDatabase: str = ...,
        DbUser: str = ...,
        SchemaPattern: str = ...,
        SecretArn: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListSchemas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#listschemaspaginator)
        """

class ListStatementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListStatements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#liststatementspaginator)
    """

    def paginate(
        self,
        *,
        RoleLevel: bool = ...,
        StatementName: str = ...,
        Status: StatusStringType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListStatementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListStatements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#liststatementspaginator)
        """

class ListTablesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListTables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#listtablespaginator)
    """

    def paginate(
        self,
        *,
        Database: str,
        ClusterIdentifier: str = ...,
        ConnectedDatabase: str = ...,
        DbUser: str = ...,
        SchemaPattern: str = ...,
        SecretArn: str = ...,
        TablePattern: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListTables.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/paginators/#listtablespaginator)
        """

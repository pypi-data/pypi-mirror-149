import time
from typing import List, Optional, Union

from pyrasgo import primitives
from pyrasgo import schemas
from .error import APIError


class Update:
    def __init__(self):
        from . import Get
        from .connection import Connection
        from pyrasgo.config import get_session_api_key
        from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self.get = Get()
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()

    def dataset(
        self,
        dataset: primitives.Dataset,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        attributes: Optional[dict] = None,
    ) -> primitives.Dataset:
        """
        Update a dataset name, description, and/or attributes in Rasgo
        """
        # Raise error if trying to update a dataset in offline mode
        if not dataset._api_dataset:
            raise APIError("Can not update dataset. Needs to be saved first with `rasgo.save.dataset()`")

        dataset_update = schemas.DatasetUpdate(
            # Possible Changed Fields
            name=name,
            description=description,
            # Persist other fields in update contract so no fields set to None in update
            status=dataset._api_dataset.status,
            owner_id=dataset._api_dataset.owner_id,
            dw_table_id=dataset._api_dataset.dw_table_id,
            attributes=attributes,
        )
        response = self.api._put(
            f"/datasets/{dataset._api_dataset.id}",
            dataset_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2,
        ).json()
        dataset_schema = schemas.Dataset(**response)
        return primitives.Dataset(api_dataset=dataset_schema)

    def dataset_column(
        self,
        dataset_column_id: int,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        attributes: Optional[dict] = None,
        tags: Optional[List[str]] = None,
    ) -> schemas.DatasetColumn:
        """
        Update metadata about a dataset column

        Args:
            dataset_column_id: Dataset column id to updated. Use `dataset.columns[x].id` to retrieve
            display_name: Display name to update for this dataset column if set
            description: Description to update for this dataset column if set
            attributes: Attributes to add or update for this dataset column. Set as Key Value pairs dict
            tags: Tags to add to this dataset column

        Returns:
            Updated Dataset Column Obj
        """
        ds_col_update = schemas.DatasetColumnUpdate(
            display_name=display_name,
            description=description,
            attributes=attributes,
            tags=tags,
        )
        resp = self.api._put(
            f"/dataset-columns/{dataset_column_id}",
            ds_col_update.dict(exclude_unset=True, exclude_none=True),
            api_version=2,
        ).json()
        return schemas.DatasetColumn(**resp)

    def dataset_table(
        self,
        dataset: primitives.Dataset,
        verbose: bool = False,
    ) -> None:
        """
        Kicks off a query for re-materializing a dataset's set Dw Table.

        The dataset needs to be published first in order call this function

        Args:
            dataset: Published dataset to refresh table for
            verbose: If True will print information related to refreshing table
        """
        # We need to ensure that the API dataset is exists and is published
        if not dataset._api_dataset or dataset.status.lower() != "published":
            raise APIError('Can not refresh table. Dataset must first be published')

        if verbose:
            print(f"Refreshing table for dataset with id '{dataset.id}' at fqtn: '{dataset.fqtn}'")

        # Call endpoint to kick off Query to re-create table in background
        sf_query_id = self.api._put(
            f"/datasets/{dataset._api_dataset.id}/table-refresh",
            _json={'refreshInBackground': True},
            api_version=2,
        ).json()
        conn = self.data_warehouse.user_connection
        while conn.is_still_running(conn.get_query_status_throw_if_error(sf_query_id)):
            if verbose:
                print("Query still executing...")
            time.sleep(1)

        if verbose:
            print(f"Done Refreshing table for dataset with id '{dataset.id}' at fqtn: '{dataset.fqtn}'")

    def dataset_schema(self, dataset_id: int) -> None:
        """
        Queries the information_schema to get column metadata from Snowflake
        Then updates this dataset's column metadata in Rasgo to match
        """
        self.api._put(
            f"/datasets/{dataset_id}/sync-schema",
            api_version=2,
        ).json()

    def transform(
        self,
        transform_id: int,
        name: Optional[str] = None,
        source_code: Optional[str] = None,
        type: Optional[str] = None,
        arguments: Optional[List[dict]] = None,
        description: Optional[str] = None,
        tags: Optional[Union[List[str], str]] = None,
    ) -> schemas.Transform:
        """
        Updates a transform in Rasgo

        Args:
            transform_id: Id of transform to update
            name: Name of the Transform
            source_code: Source code of transform
            type: Type of transform it is. Used for categorization only
            arguments: A list of arguments to supply to the transform
                       so it can render them in the UI. Each argument
                       must be a dict with the keys: 'name', 'description', and 'type'
                       values all strings for their corresponding value
            description: Description of Transform
            tags: List of tags, or a tag (string), to set on this dataset
        """
        # Init tag array to be list of strings
        if tags is None:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        # Make request to update transform and return
        transform_update = schemas.TransformUpdate(
            name=name,
            type=type,
            description=description,
            sourceCode=source_code,
            arguments=arguments,
            tags=tags,
        )
        response = self.api._put(
            f"/transform/{transform_id}",
            transform_update.dict(exclude_unset=True, exclude_none=True),
            api_version=1,
        ).json()
        return schemas.Transform(**response)

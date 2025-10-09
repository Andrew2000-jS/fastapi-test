from pydantic import Field, model_serializer
from typing import Any
from enum import Enum
from datetime import datetime
from .schema import CommonBaseModel

class LogicalOperator(Enum):
    """
    Enumeration of logical operators for MongoDB queries.

    Attributes:
        AND (str): Represents the MongoDB `$and` operator.
        OR (str): Represents the MongoDB `$or` operator.
        NOR (str): Represents the MongoDB `$nor` operator.
    """
    AND = "$and"
    OR = "$or"
    NOR = "$nor"

class OrderBy(Enum):
    """
    Enumeration for sort order directions.

    Attributes:
        ASC (int): Ascending order, represented as 1 in MongoDB.
        DESC (int): Descending order, represented as -1 in MongoDB.
    """
    ASC = 1
    DESC = -1

class SortDTO(CommonBaseModel):
    """
    Represent sorting criteria for MongoDB queries.
    """
    field: str = Field(
        ...,
        description="The document field to sort by, e.g., 'created_at' or 'name'."
    )
    order: OrderBy = Field(
        ...,
        description="The sorting direction: ASC (1) for ascending or DESC (-1) for descending."
    )

    @model_serializer
    def to_mongo(self) -> dict[str, int]:
        """
        Convert the SortDTO into a MongoDB `$sort` stage.

        Returns:
            dict[str, int]: A dictionary in the format {field: order_value},
            e.g., {"created_at": 1} for ascending sort.
        """
        return {self.field: self.order.value}


class FiltersDTO(CommonBaseModel):
    """
    Represent filtering criteria for MongoDB queries.
    """
    query: list[dict[str, Any]] = Field(
        ...,
        description="A list of filter conditions (dicts). If multiple are provided, they will be combined with `$and`."
    )
    
    operator: LogicalOperator = Field(
        default=LogicalOperator.AND,
        description="Logical operator used to combine conditions (AND, OR, NOR)."
    )

    @model_serializer
    def to_mongo(self) -> dict[str, Any] | None:
        """
        Convert the FiltersDTO into a MongoDB `$match` stage.

        Returns:
            dict[str, Any] | None:
                - A `$match` stage if filters exist.
                - `None` if no filters are provided.
                - Combines multiple conditions with the specified logical operator.
        """
        if not self.query:
            return None

        if len(self.query) == 1:
            return {"$match": self.query[0]}

        return {"$match": {self.operator.value: self.query}}


class PaginationDTO(CommonBaseModel):
    """
    Represent pagination and optional date filtering for MongoDB queries.
    """
    limit: int = Field(
        5,
        description="Maximum number of documents to return. Defaults to 5."
    )
    cursor: str | None = Field(
        None,
        description="The cursor value (string) for pagination. Used for fetching the next page of results."
    )
    cursor_name: str | None = Field(
        None,
        description="The field name used as the cursor for pagination comparison."
    )
    start_date: datetime | None = Field(
        None,
        description="Optional filter for documents created after this date."
    )
    end_date: datetime | None = Field(
        None,
        description="Optional filter for documents created before this date."
    )

    def to_mongo(self) -> list[dict[str, Any]]:
        """
        Convert pagination and date filters into MongoDB aggregation pipeline stages.

        Returns:
            list[dict[str, Any]]:
                A list of MongoDB pipeline stages that may include:
                - `$match` for date ranges and cursor filtering.
                - `$limit` for limiting the number of documents.
        """
        stages = []
        match_conditions = {}
        if self.start_date:
            match_conditions["created_at"] = {"$gte": self.start_date}
        if self.end_date:
            match_conditions.setdefault("created_at", {})
            match_conditions["created_at"]["$lte"] = self.end_date

        if self.cursor and self.cursor_name:
            match_conditions[self.cursor_name] = {"$gt": self.cursor}

        if match_conditions:
            stages.append({"$match": match_conditions})

        stages.append({"$limit": self.limit})

        return stages


class Criteria(CommonBaseModel):
    """
    Aggregation criteria that combine pagination, sorting, and filters
    into a single MongoDB aggregation pipeline.
    """
    pagination: PaginationDTO = Field(
        ...,
        description="Pagination configuration including limits, cursor, and optional date filters."
    )
    sort_by: SortDTO = Field(
        ...,
        description="Sorting configuration specifying field and direction."
    )
    filters: list[FiltersDTO] | None = Field(
        default_factory=list,
        description="A list of filtering conditions to apply."
    )

    def to_pipeline(self) -> list[dict[str, Any]]:
        """
        Build a MongoDB aggregation pipeline from the criteria.

        Returns:
            list[dict[str, Any]]:
                The complete aggregation pipeline with `$match`, `$limit`, and `$sort`
                stages applied according to the criteria configuration.
        """
        pipeline: list[dict[str, Any]] = []

        if self.filters:
            for f in self.filters:
                stage = f.model_dump()
                if stage:
                    pipeline.append(stage)

        pipeline.extend(self.pagination.to_mongo())

        if self.sort_by:
            pipeline.append({"$sort": self.sort_by.model_dump()})

        return pipeline

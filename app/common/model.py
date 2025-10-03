from beanie import Document, before_event, Save, Update, Insert
from pydantic import Field
from typing import Any, AsyncIterator
from .criteria import Criteria
from datetime import datetime

class CommonDocument(Document):
    """
        Base document class that adds automatic timestamping for creation and updates.

        Provides `created_at` and `updated_at` fields that are automatically managed
        whenever a document is saved, inserted, or updated.
    """
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)
    
    @before_event(Save, Update, Insert)
    async def set_update_date(self):
        """
            Automatically update the `updated_at` timestamp before saving, updating, or inserting.

            This ensures that the `updated_at` field always reflects the latest modification time.
        """
        self.updated_at = datetime.now()
        
    @classmethod
    async def paginate(
        cls,
        criteria: Criteria,
        cursor_name: str
    ) -> dict[str, Any]:
        """
            Apply the criteria pattern using MongoDB aggregation.
            
            Args:
                criteria (Criteria): The filtering, sorting, and pagination configuration.

            Returns:
                dict[str, Any]: Contains paginated results, total count, and next cursor.
        """
        pipeline = criteria.to_pipeline()
        cursor = cls.aggregate(pipeline)

        total = await cls.count()

        docs = [doc async for doc in cursor]
        next_cursor = str(docs[-1][cursor_name]) if docs else None

        return {
            "result": docs,
            "total": total,
            "next_cursor": next_cursor
        }

    
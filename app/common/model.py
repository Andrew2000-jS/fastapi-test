from beanie import Document, before_event, Save, Update, Insert
from pydantic import Field
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

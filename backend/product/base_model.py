import mongoengine
from datetime import datetime, timezone

class TimeStampedDocument(mongoengine.Document):
    created_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super(TimeStampedDocument, self).save(*args, **kwargs)
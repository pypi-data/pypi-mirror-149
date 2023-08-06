from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GWorkspaceWatch(BaseModel):
    kind: str
    id: UUID
    resourceId: str
    resourceUri: str
    token: str
    expiration: str


class CreateWatch(BaseModel):
    uuid: UUID
    url: str
    token: str
    ttl: Optional[int] = 3600

    def dict(self, *args, **kwargs):
        data = super(CreateWatch, self).dict()
        data["uuid"] = str(self.uuid)
        return data


class DeleteWatch(BaseModel):
    uuid: UUID
    resource_id: str

    def dict(self, *args, **kwargs):
        data = super(DeleteWatch, self).dict()
        data["uuid"] = str(self.uuid)
        return data
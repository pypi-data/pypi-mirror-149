from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GWorkspaceUserWildflowerSchema(BaseModel):
    School_Founder: Optional[bool]
    Teacher_Leader: Optional[bool]
    Emerging_Teacher_Leader: Optional[bool]
    Classroom_Staff: Optional[bool]
    Fellow: Optional[bool]
    Partner: Optional[bool]
    Contractor: Optional[bool]


class GWorkspaceUserCustomSchema(BaseModel):
    Wildflower_Profile: Optional[GWorkspaceUserWildflowerSchema]


class GWorkspaceUserLanguages(BaseModel):
    languageCode: str
    preference: str


class GWorkspaceUserEmails(BaseModel):
    address: str
    primary: Optional[bool]


class GWorkspaceUserName(BaseModel):
    givenName: str
    familyName: str
    fullName: str


class GWorkspaceUser(BaseModel):
    kind: str
    id: str
    etag: str
    primaryEmail: str
    isAdmin: bool
    isDelegatedAdmin: bool
    lastLoginTime: datetime
    creationTime: datetime
    agreedToTerms: bool
    suspended: bool
    archived: bool
    changePasswordAtNextLogin: bool
    ipWhitelisted: bool
    customerId: str
    orgUnitPath: str
    isMailboxSetup: bool
    isEnrolledIn2Sv: bool
    isEnforcedIn2Sv: bool
    includeInGlobalAddressList: bool
    name: GWorkspaceUserName
    customSchemas: Optional[GWorkspaceUserCustomSchema]
    emails: list[GWorkspaceUserEmails]
    languages: list[GWorkspaceUserLanguages]

    def is_school_founder(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.School_Founder

    def is_teacher_leader(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.Teacher_Leader

    def is_emerging_teacher_leader(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.Emerging_Teacher_Leader

    def is_classroom_staff(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.Classroom_Staff

    def is_fellow(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.Fellow

    def is_partner(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.Partner

    def is_contractor(self) -> Optional[bool]:
        if self.customSchemas is None:
            return None

        return self.customSchemas.Wildflower_Profile.Contractor

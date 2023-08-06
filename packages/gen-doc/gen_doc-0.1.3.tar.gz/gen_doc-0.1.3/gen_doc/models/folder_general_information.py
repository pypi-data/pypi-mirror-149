"""
General info of the repository
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class GeneralInfo(BaseModel):
    """
    Model with general information about the repository
    """

    title: Optional[str] = Field(None, description="Title project")
    description: Optional[str] = Field(None, description="Description project")
    author: Optional[str] = Field(None, description="Name author")
    author_contacts: Optional[List[str]] = Field(None, description="Contacts author")
    release: Optional[str] = Field(None, description="Version release")
    repository_main_url: Optional[str] = Field(None, description="Url to repository")

# In the name of GOD


from pydantic import ConfigDict, BaseModel, Field, EmailStr, StringConstraints
from pydantic.functional_validators import BeforeValidator
from pydantic.types import SecretStr, constr

from typing import Optional, List, Required
from typing_extensions import Annotated
from bson import ObjectId



# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserLogin(BaseModel):
    username : Optional[str] = None
    email: Optional[EmailStr] = Field(unique=True)
    password : SecretStr


class UserRegister(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    username : Annotated[str, StringConstraints(to_lower=True)]
    email: Optional[EmailStr] = Field(unique=True)
    password : SecretStr


class UserUpdate(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email: Optional[EmailStr] = None
    image : Optional[str] = None


class AdminUserUpdate(UserUpdate):
    is_email_verified : Optional[bool] = False
    is_active : Optional[bool] = True
    is_superuser : Optional[bool] = False
    is_deleted : Optional[bool] = False


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username : str
    email: Optional[EmailStr] = None
    password : SecretStr
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    is_active : Optional[bool] = True
    is_superuser : Optional[bool] = False
    is_deleted : Optional[bool] = False
    image : Optional[str] = None
    is_email_verfied : Optional[str] = False


class UserCollection(BaseModel):
    """
    A container holding a list of `UserModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    users: List[User]
@router.post(
    "/update_profile",
    response_description="Update profile",
    # response_model=User,
    response_model_by_alias=False,
)
async def update_profile(user_data:LoginDep, update_data: UserUpdate = Body(...)): # depend on login
    """
    check input credential to be in User collection and pass it to athorization.
    """
    account_db = collections['users_collection']
    result = await account_db.update_one(filter={"username": user_data.get("data").get("username")}, update={"$set": update_data.dict(exclude_none=True)})

    return JSONResponse({"message": str(result)}, status_code=status.HTTP_200_OK)

@router.get(

    "/user_profile",
    response_description="User profile for internal services access",
)
async def user_profile(user_data:LoginDep): # depend on login

    account_db = collections['users_collection']
    user_profile_data = await account_db.find_one(filter={"$or":[{"username":{"$eq": user_data["data"]["username"], "$ne": None}},
                                                        {"email": {"$eq":user_data["data"].get("email", "no email"), "$ne": None}}]})
    if not user_profile_data:
        return JSONResponse({"message": "User Not found"}, status_code=status.HTTP_404_NOT_FOUND)
    user_profile_data.pop("_id")
    return JSONResponse({"user_profile": user_profile_data}, status_code=status.HTTP_200_OK)
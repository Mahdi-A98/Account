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

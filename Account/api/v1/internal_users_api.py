@router.post(
    "/update_user_data",
    response_description="Update profile for internal services access",
    dependencies=[Depends(AllowedServices(["authentication"]))],
)
async def update_user_data(user_data:dict=Body(...), update_data: AdminUserUpdate = Body(...)): # depend on login
    account_db = collections['users_collection']
    result = await account_db.update_one(filter={"$or":[{"username": user_data.get("username")},
                                                        {"email": user_data.get("email")}]},
                                        update={"$set": update_data.dict(exclude_none=True)})
    if not result.matched_count:
        return JSONResponse({"message": str(result)}, status_code=status.HTTP_404_NOT_FOUND)

    if not result.modified_count:
        return JSONResponse({"message": "Nothig changed"}, status_code=215)
    return JSONResponse({"message": str(result)}, status_code=status.HTTP_202_ACCEPTED)


@router.post(
    "/user_profile_X",
    response_description="User profile for internal services access",
    dependencies=[Depends(AllowedServices(["authentication"]))],
)
async def user_profile_x(user_data:dict=Body(...)): # depend on login
    account_db = collections['users_collection']
    result = await account_db.find_one({"$or":[{"username": user_data.get("username")},
                                                {"email": user_data.get("email")}]})
    result.pop("_id")
    if not result:
        return JSONResponse({"message": "User not found "}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({"message": "User has found", "data": result}, status_code=status.HTTP_200_OK)
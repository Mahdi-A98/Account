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

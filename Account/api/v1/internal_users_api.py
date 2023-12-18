


@router.post(
    "/login",
    response_description="User Login",
    response_model=User,
    response_model_by_alias=False,
    dependencies=[Depends(AllowedServices(["authentication"]))]
)
async def login(login_data:UserLogin=Body(...)):
    """
    check input credential to be in User collection and pass it to athorization.
    """
    users_collection = collections["users_collection"]
    data = login_data.model_dump(by_alias=True, exclude=["id", "password"])
    data['password'] = login_data.password.get_secret_value()
    existed_user =  await users_collection.find_one({"$or":[{"username":{"$eq": data.get("username"), "$ne": None}},
                                                            {"email": {"$eq":data.get("email"), "$ne": None}}]},)
    if existed_user:
        if existed_user.get("password") == data.get("password"):
            return existed_user
        return JSONResponse({"message": "password doesn't match!!"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse({"message": "Invalid username or email"}, status_code=status.HTTP_401_UNAUTHORIZED)


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
from fastapi import APIRouter, Depends
from typing import List
from app.deps import check_token
from app.endpoints import (
    get_users,
    get_user,
    create_user,
    delete_user,
    get_groups,
    get_group,
    create_group,
    delete_group,
)
from app.schemas import DetailedGroupSchema, DetailedUserSchema, GroupSchema, UserSchema


app_router = APIRouter()
app_router.add_api_route(
    "/users",
    get_users,
    methods=["GET"],
    response_model=List[UserSchema],
)
app_router.add_api_route(
    "/users/{user_id}",
    get_user,
    methods=["GET"],
    response_model=DetailedUserSchema,
)
app_router.add_api_route(
    "/users",
    create_user,
    methods=["POST"],
    dependencies=[Depends(check_token)],
    response_model=DetailedUserSchema,
)
app_router.add_api_route(
    "/users/{user_id}",
    delete_user,
    methods=["DELETE"],
    dependencies=[Depends(check_token)],
)

app_router.add_api_route(
    "/groups",
    get_groups,
    methods=["GET"],
    response_model=List[GroupSchema],
)
app_router.add_api_route(
    "/groups/{group_id}",
    get_group,
    methods=["GET"],
    response_model=DetailedGroupSchema,
)
app_router.add_api_route(
    "/groups",
    create_group,
    methods=["POST"],
    dependencies=[Depends(check_token)],
    response_model=DetailedGroupSchema,
)
app_router.add_api_route(
    "/groups/{group_id}",
    delete_group,
    methods=["DELETE"],
    dependencies=[Depends(check_token)],
)

from typing import List
from fastapi import HTTPException
from app.models import Group, User
from neomodel import db
from app.schemas import (
    CreateGroupSchema,
    CreateUserSchema,
    DetailedGroupSchema,
    DetailedUserSchema,
    GroupSchema,
    UserSchema,
)


async def get_users(limit: int = 50, offset: int = 0):
    query = """
    MATCH (user:User)
    OPTIONAL MATCH (user)-[rel:FOLLOWS]->(target:User)
    RETURN user, collect({target: target}) AS relationships
    SKIP $offset LIMIT $limit
    """
    results, _ = db.cypher_query(
        query,
        {"offset": offset, "limit": limit},
    )

    users = []

    for res in results:
        node, rels = res
        user = UserSchema(**node._properties)

        for rel in rels:
            if not rel["target"]:
                continue
            user.friends.append(rel["target"]["user_id"])

        users.append(user)

    return users


async def get_user(user_id: int):
    item = User.nodes.get_or_none(user_id=user_id)

    if not item:
        raise HTTPException(status_code=404)

    follows = item.follows.all()
    subscribes = item.subscribes.all()

    return DetailedUserSchema(
        user_id=item.user_id,
        name=item.name,
        sex=item.sex,
        home_town=item.home_town,
        follows=[
            UserSchema(
                user_id=u.user_id,
                name=u.name,
                sex=u.sex,
                home_town=u.home_town,
            )
            for u in follows
        ],
        subscribes=[
            GroupSchema(
                group_id=g.group_id,
                name=g.name,
            )
            for g in subscribes
        ],
    )


async def create_user(payload: CreateUserSchema):
    follows: List[User] = []
    subscribes: List[Group] = []

    if payload.follows:
        follows = User.nodes.filter(user_id__in=payload.follows)
    if payload.subscribes:
        subscribes = Group.nodes.filter(group_id__in=payload.subscribes)

    user = User(
        user_id=payload.user_id,
        name=payload.name,
        sex=payload.sex,
        home_town=payload.home_town,
    ).save()

    if follows:
        for f in follows:
            user.follows.connect(f)

    if subscribes:
        for s in subscribes:
            user.subscribes.connect(s)

    return DetailedUserSchema(
        user_id=user.user_id,
        name=user.name,
        sex=user.sex,
        home_town=user.home_town,
        follows=[
            UserSchema(
                user_id=u.user_id,
                name=u.name,
                sex=u.sex,
                home_town=u.home_town,
            )
            for u in follows
        ],
        subscribes=[
            GroupSchema(
                group_id=g.group_id,
                name=g.name,
            )
            for g in subscribes
        ],
    )


async def delete_user(user_id: int) -> bool:
    item = User.nodes.get_or_none(user_id=user_id)

    if not item:
        raise HTTPException(status_code=404)

    return User.delete(item)


async def get_groups(limit: int = 50, offset: int = 0):
    query = """
    MATCH (group:Group)
    OPTIONAL MATCH (subscriber:User)-[rel:SUBSCRIBES]->(group)
    RETURN group, collect({subscriber: subscriber, relationship: type(rel)}) AS subscribers
    SKIP $offset LIMIT $limit
    """
    results, _ = db.cypher_query(
        query,
        {"offset": offset, "limit": limit},
    )

    groups = []

    for res in results:
        node, rels = res
        group = GroupSchema(**node._properties)

        for rel in rels:
            if not rel["subscriber"]:
                continue
            group.members.append(int(rel["subscriber"]["user_id"]))

        groups.append(group)

    return groups


async def get_group(group_id: int):
    item: Group | None = Group.nodes.get_or_none(group_id=group_id)

    if not item:
        raise HTTPException(status_code=404)

    subs = item.subscribers.all()

    return DetailedGroupSchema(
        group_id=item.group_id,
        name=item.name,
        subscribers=[
            UserSchema(
                user_id=u.user_id,
                name=u.name,
                sex=u.sex,
                home_town=u.home_town,
            )
            for u in subs
        ],
    )


async def create_group(payload: CreateGroupSchema):
    subscribers: List[User] = []

    if payload.subscribers:
        subscribers = User.nodes.filter(user_id__in=payload.subscribers)

    group = Group(
        group_id=payload.group_id,
        name=payload.name,
    ).save()

    if subscribers:
        for s in subscribers:
            group.subscribers.connect(s)

    return DetailedGroupSchema(
        group_id=group.group_id,
        name=group.name,
        subscribers=[
            UserSchema(
                user_id=u.user_id,
                name=u.name,
                sex=u.sex,
                home_town=u.home_town,
            )
            for u in subscribers
        ],
    )


async def delete_group(group_id: int) -> bool:
    item = Group.nodes.get_or_none(group_id=group_id)

    if not item:
        raise HTTPException(status_code=404)

    return Group.delete(item)
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    IntegerProperty,
)


class User(StructuredNode):
    user_id = IntegerProperty(unique_index=True)
    name = StringProperty()
    sex = IntegerProperty()
    home_town = StringProperty()

    follows = RelationshipTo("User", "FOLLOWS")
    subscribes = RelationshipTo("Group", "SUBSCRIBES")


class Group(StructuredNode):
    group_id = IntegerProperty(unique_index=True)
    name = StringProperty()

    subscribers = RelationshipFrom("User", "SUBSCRIBES")

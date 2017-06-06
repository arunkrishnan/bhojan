import graphene

import bhojanmenu.schema


class Query(bhojanmenu.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)

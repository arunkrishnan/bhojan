import graphene

import bhojanmenu.schema
import bhojanusers.schema


class Query(bhojanmenu.schema.Query,
            bhojanusers.schema.Query,
            graphene.ObjectType):
    pass

class Mutation(bhojanmenu.schema.Mutation,
                bhojanusers.schema.Mutation,
                graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene

import bhojanmenu.schema


class Query(bhojanmenu.schema.Query, graphene.ObjectType):
    pass

class Mutation(bhojanmenu.schema.Mutation, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query, mutation=Mutation)

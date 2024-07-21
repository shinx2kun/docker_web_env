import graphene
import procmanual.schema
# import users.schema
import graphql_jwt


# class Query(procmanual.schema.Query, users.schema.Query, graphene.ObjectType):
class Query(procmanual.schema.Query, graphene.ObjectType):
    pass

# class Mutation(procmanual.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
class Mutation(procmanual.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

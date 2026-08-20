import graphene
import accounts.schema 
import app1.schema
import graphql_jwt

# Query Merge
class Query(accounts.schema.Query, 
            app1.schema.Query, 
            graphene.ObjectType):
    pass

# Mutation Merge
class Mutation(accounts.schema.Mutation,
               app1.schema.Mutation,  
               graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# Make a package w/Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
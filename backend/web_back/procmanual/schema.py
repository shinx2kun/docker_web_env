import graphene
from graphene_django.types import DjangoObjectType
from .models import Procmanual, Site, Rank
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required
from django.utils import timezone


class ProcmanualNode(DjangoObjectType):
    class Meta:
        model = Procmanual
        # 検索時のフィルター設定
        filter_fields = {
            "title": ['icontains'],
            'site__site_name': ['icontains'],
            'rank__rank': ['icontains'],
            # 'check_cmd': ['icontains'],
            'created_date': ['icontains'],
            'published_date': ['icontains'],
        }
        interfaces = (relay.Node,)

class SiteNode(DjangoObjectType):
    class Meta:
        model = Site
        filter_fields = {
            'procmanual': ['exact'],
            'site_name': ['exact'],
        }
        interfaces = (relay.Node,)

class RankNode(DjangoObjectType):
    class Meta:
        model = Rank
        filter_fields = {
            'procmanual': ['exact'],
            'rank': ['exact'],
        }
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    procmanual = graphene.Field(ProcmanualNode, id=graphene.NonNull(graphene.ID))
    all_procmanuals = DjangoFilterConnectionField(ProcmanualNode)

    site = graphene.Field(SiteNode, id=graphene.NonNull(graphene.ID))
    all_site = DjangoFilterConnectionField(SiteNode)

    rank = graphene.Field(RankNode, id=graphene.NonNull(graphene.ID))
    all_rank = DjangoFilterConnectionField(RankNode)

    def resolve_procmanual(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Procmanual.objects.get(id=from_global_id(id)[1])
    def resolve_all_procmanuals(self, info, **kwargs):
        return Procmanual.objects.all()

    def resolve_site(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Site.objects.get(id=from_global_id(id)[1])
    def resolve_all_site(self, info, **kwargs):
        return Site.objects.all()
            
    def resolve_rank(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Rank.objects.get(id=from_global_id(id)[1])
    def resolve_all_rank(self, info, **kwargs):
        return Rank.objects.all()


class ProcmanualCreateMutation(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        site = graphene.ID(required=True)
        rank = graphene.ID(required=True)
        # check_cmd = graphene.List(graphene.String)
    procmanual = graphene.Field(ProcmanualNode)

    # @login_required
    def mutate_and_get_payload(root, info, **input):
        site_id = from_global_id(input.get('site'))[1]
        rank_id = from_global_id(input.get('rank'))[1]
        procmanual = Procmanual(
            title = input.get('title'),
            site = Site.objects.get(id=site_id),
            rank = Rank.objects.get(id=rank_id),
            # check_cmd = input.get('check_cmd'),
            created_date = input.get('created_date', timezone.now())
        )
        procmanual.save()
        return ProcmanualCreateMutation(procmanual=procmanual)

class ProcmanualUpdateMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True) 
        title = graphene.String(required=True) 
        site = graphene.ID(required=True)
        rank = graphene.ID(required=True)
        created_date = graphene.DateTime(required=True)
        # check_cmd = graphene.List(graphene.String, required=True)
    procmanual = graphene.Field(ProcmanualNode)
    
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        site_id = from_global_id(input.get('site'))[1]
        rank_id = from_global_id(input.get('rank'))[1]
        procmanual = Procmanual(
            id = from_global_id(input.get('id'))[1],
        )        
        procmanual.title = input.get('title')
        procmanual.site = Site.objects.get(id=site_id)
        procmanual.rank = Rank.objects.get(id=rank_id)
        procmanual.created_date = input.get('created_date')
        # procmanual.check_cmd = input.get('check_cmd')
        procmanual.published_date = input.get('published_date', timezone.now())

        procmanual.save()
        return ProcmanualUpdateMutation(procmanual=procmanual)


class ProcmanualDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    procmanual = graphene.Field(ProcmanualNode)

    # @login_required
    def mutate_and_get_payload(root, info, **input):
        procmanual = Procmanual(
            id=from_global_id(input.get("id"))[1]
        )
        procmanual.delete()
        return ProcmanualDeleteMutation(procmanual=None)



class Mutation(graphene.ObjectType):
    create_procmanual = ProcmanualCreateMutation.Field()
    update_procmanual = ProcmanualUpdateMutation.Field()
    delete_procmanual = ProcmanualDeleteMutation.Field()


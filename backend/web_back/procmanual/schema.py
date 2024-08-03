import graphene
from graphene_django.types import DjangoObjectType
import django_filters
from django.db import models
from .models import Procmanual, Site, Rank
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required
from django.utils import timezone
import json


class JSONFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(**{f"{self.field_name}__icontains": value})

class ProcmanualFilter(django_filters.FilterSet):
    check_cmd = JSONFilter(field_name='check_cmd', lookup_expr='icontains')
    check_list = JSONFilter(field_name='check_list', lookup_expr='icontains')
    execute_cmd = JSONFilter(field_name='execute_cmd', lookup_expr='icontains')
    class Meta:
        model = Procmanual
        fields = {
            'title': ['icontains'],
            'site__site': ['icontains'],
            'rank__rank': ['icontains'],
            'created_date': ['icontains'],
            'published_date': ['icontains'],
        }
        filter_overrides = {
            models.JSONField: {
                'filter_class': JSONFilter,
            },
        }

class ProcmanualNode(DjangoObjectType):
    class Meta:
        model = Procmanual
        filterset_class = ProcmanualFilter
        interfaces = (relay.Node,)

class SiteNode(DjangoObjectType):
    class Meta:
        model = Site
        filter_fields = {
            'procmanual': ['exact'],
            'site': ['exact'],
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
    all_sites = DjangoFilterConnectionField(SiteNode)
    rank = graphene.Field(RankNode, id=graphene.NonNull(graphene.ID))
    all_ranks = DjangoFilterConnectionField(RankNode)
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
    def resolve_all_sites(self, info, **kwargs):
        return Site.objects.all()      
    def resolve_rank(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Rank.objects.get(id=from_global_id(id)[1])
    def resolve_all_ranks(self, info, **kwargs):
        return Rank.objects.all()


class ProcmanualCreateMutation(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        site = graphene.ID(required=True)
        rank = graphene.ID(required=True)
        check_cmd = graphene.JSONString()
        check_list = graphene.JSONString()
        execute_cmd = graphene.JSONString()
    procmanual = graphene.Field(ProcmanualNode)
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        site_id = from_global_id(input.get('site'))[1]
        rank_id = from_global_id(input.get('rank'))[1]
        procmanual = Procmanual(
            title = input.get('title'),
            site = Site.objects.get(id=site_id),
            rank = Rank.objects.get(id=rank_id),
            check_cmd=input.get('check_cmd', {}),
            check_list=input.get('check_list', {}),
            execute_cmd=input.get('execute_cmd', {}),
            created_date = input.get('created_date', timezone.now()),
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
        check_cmd = graphene.JSONString(required=True)
        check_list = graphene.JSONString(required=True)
        execute_cmd = graphene.JSONString(required=True)
        
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
        procmanual.check_cmd = input.get('check_cmd')
        procmanual.check_list = input.get('check_list')
        procmanual.execute_cmd = input.get('execute_cmd')
        procmanual.created_date = input.get('created_date')
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

class SiteCreateMutation(relay.ClientIDMutation):
    class Input:
        site = graphene.String(required=True)
    site = graphene.Field(SiteNode)
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        site = Site(
            site = input.get('site'),
        )
        site.save()
        return SiteCreateMutation(site=site)

class SiteUpdateMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True) 
        site = graphene.String(required=True) 
        # check_cmd = graphene.List(graphene.String, required=True)
    site = graphene.Field(SiteNode)   
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        site = Site(
            id = from_global_id(input.get('id'))[1],
        )        
        site.site = input.get('site')
        site.save()
        return SiteUpdateMutation(site=site)

class SiteDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    site = graphene.Field(SiteNode)
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        site = Site(
            id=from_global_id(input.get("id"))[1]
        )
        site.delete()
        return SiteDeleteMutation(site=None)    


class RankCreateMutation(relay.ClientIDMutation):
    class Input:
        rank = graphene.String(required=True)
    rank = graphene.Field(RankNode)
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        rank = Rank(
            rank = input.get('rank'),
        )
        rank.save()
        return RankCreateMutation(rank=rank)

class RankUpdateMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True) 
        rank = graphene.String(required=True) 
        # check_cmd = graphene.List(graphene.String, required=True)
    rank = graphene.Field(RankNode)   
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        rank = Rank(
            id = from_global_id(input.get('id'))[1],
        )        
        rank.rank = input.get('rank')
        rank.save()
        return RankUpdateMutation(rank=rank)

class RankDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    rank = graphene.Field(RankNode)
    # @login_required
    def mutate_and_get_payload(root, info, **input):
        rank = Rank(
            id=from_global_id(input.get("id"))[1]
        )
        rank.delete()
        return RankDeleteMutation(rank=None) 


class Mutation(graphene.ObjectType):
    create_procmanual = ProcmanualCreateMutation.Field()
    update_procmanual = ProcmanualUpdateMutation.Field()
    delete_procmanual = ProcmanualDeleteMutation.Field()
    create_site = SiteCreateMutation.Field()
    update_site = SiteUpdateMutation.Field()
    delete_site = SiteDeleteMutation.Field()
    create_rank = RankCreateMutation.Field()
    update_rank = RankUpdateMutation.Field()
    delete_rank = RankDeleteMutation.Field()

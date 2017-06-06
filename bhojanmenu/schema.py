from graphene import relay, ObjectType, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from models import Food, Menu


class FoodNode(DjangoObjectType):
    class Meta:
        model = Food
        filter_fields = ['category', 'cuisine', 'menu']
        interfaces = (relay.Node, )


class MenuNode(DjangoObjectType):
    class Meta:
        model = Menu
        filter_fields = {'availability_start_time': ['exact', 'istartswith'],
        				 'availability_end_time':['gt','lt', 'exact'],
        				 'quantity':['gt', 'lt', 'exact'],
        				 'price': ['gt', 'lt','exact']
        				}
        interfaces = (relay.Node, )


class Query(AbstractType):
	food = relay.Node.Field(FoodNode)
	all_food = DjangoFilterConnectionField(FoodNode)
	menu = relay.Node.Field(MenuNode)
	all_menu = DjangoFilterConnectionField(MenuNode)

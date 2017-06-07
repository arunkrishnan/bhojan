from graphene import relay, ObjectType, AbstractType, ClientIDMutation
from graphene import Field, String, Int, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

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
                         'availability_end_time':['gt', 'lt', 'exact'],
                         'quantity':['gt', 'lt', 'exact'],
                         'price': ['gt', 'lt', 'exact']
                        }
        interfaces = (relay.Node, )


class NewFood(ClientIDMutation):
    food = Field(FoodNode)
    class Input:
        name = String()
        description = String()
        ingrediants = String()
        cuisine = String()
        category = String()
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        food = Food(
            name = input.get('name') ,
            description = input.get('description'),
            ingrediants = input.get('ingrediants'),
            cuisine = input.get('cuisine'),
            category = input.get('category')
        )
        food.save()
        return NewFood(food=food)


class NewMenu(ClientIDMutation):
    menu = Field(MenuNode)
    class Input:
        food = String()
        availability_start_time = String()
        availability_end_time = String()
        quantity = Int()
        price = Float()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        menu = Menu(
            availability_start_time = input.get('availability_start_time'),
            availability_end_time = input.get('availability_end_time'),
            quantity = input.get('quantity'),
            food = Food.objects.get(name=input.get('food'))
        )
        menu.save()
        return NewMenu(menu=menu)


class UpdateFood(ClientIDMutation):
    food = Field(FoodNode)
    class Input:
        id = String()
        name = String()
        description = String()
        ingrediants = String()
        cuisine = String()
        category = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        food = Food.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('name'):
            food.name = input.get('name')
        if input.get('description'):
            food.description = input.get('description')
        if input.get('ingrediants'):
            food.ingrediants = input.get('ingrediants')
        if input.get('cuisine'):
            food.cuisine = input.get('cuisine')
        if input.get('category'):
            food.category = input.get('category')
        food.save()
        return UpdateFood(food=food)


class UpdateMenu(ClientIDMutation):
    menu = Field(MenuNode)
    class Input:
        id = String()
        availability_start_time = String()
        availability_end_time = String()
        quantity = Int()
        price = Float()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        menu = Menu.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('availability_start_time'):
            menu.availability_start_time = input.get('availability_start_time')
        if input.get('availability_end_time'):
            menu.availability_end_time = input.get('availability_end_time')
        if input.get('quantity'):
            menu.quantity = input.get('quantity')
        if input.get('price'):
            menu.price = input.get('price')
        menu.save()
        return UpdateMenu(menu=menu)


class DeleteFood(ClientIDMutation):
    success = String()
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        food = Food.objects.get(pk=from_global_id(input.get('id'))[1])
        food.delete()
        return DeleteFood(success=True)


class DeleteMenu(ClientIDMutation):
    success = String()
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        menu = Menu.objects.get(pk=from_global_id(input.get('id'))[1])
        menu.delete()
        return DeleteMenu(success=True)


class Query(AbstractType):
    food = relay.Node.Field(FoodNode)
    all_food = DjangoFilterConnectionField(FoodNode)
    menu = relay.Node.Field(MenuNode)
    all_menu = DjangoFilterConnectionField(MenuNode)


class Mutation(AbstractType):
    new_food = NewFood.Field()
    new_menu = NewMenu.Field()
    update_food = UpdateFood.Field()
    update_menu = UpdateMenu.Field()
    delete_food = DeleteFood.Field()
    delete_menu = DeleteMenu.Field()

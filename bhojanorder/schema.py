from graphene import relay, ObjectType, AbstractType, ClientIDMutation
from graphene import Field, String, Int, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from bhojanmenu.models import Food
from bhojanusers.models import Customer, DeliveryExecutive, CustomerAddress
from models import Order, OrderItems


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filter_fields = {'customer': ['exact'],
                         'amount': ['exact', 'lt', 'gt'],
                         'order_time': ['exact', 'lt', 'gt'],
                         'delivery_executive': ['exact'],
                         'status': ['exact']
                        }
        interfaces = (relay.Node, )


class OrderItemsNode(DjangoObjectType):
    class Meta:
        model = OrderItems
        filter_fields = ['order', 'food']
        interfaces = (relay.Node, )


class NewOrder(ClientIDMutation):
    success = String()
    class Input:
        customer = String()
        amount = Float()
        order_time = String()
        delivery_executive = String()
        delivery_address = String()
        status = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        order = Order(
            customer = Customer.objects.get(pk=from_global_id(input.get('customer'))[1]),
            amount = input.get('amount'),
            order_time = input.get('order_time'),
            delivery_executive = DeliveryExecutive.objects.get(pk=from_global_id(input.get('delivery_executive'))[1]),
            delivery_address = CustomerAddress.objects.get(pk=from_global_id(input.get('delivery_address'))[1]),
            status = input.get('status')
        )
        order.save()
        return NewOrder(success=True)


class NewOrderItems(ClientIDMutation):
    success = String()
    class Input:
        order = String()
        food = String()
        quantity = Int()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        order_items = OrderItems(
            order = Order.objects.get(pk=from_global_id(input.get('order'))[1]),
            food = Food.objects.get(pk=from_global_id(input.get('food'))[1]),
            quantity = input.get('quantity')
        )
        order_items.save()
        return NewOrderItems(success=True)


class UpdateOrder(ClientIDMutation):
    success = String()
    class Input:
        id = String()
        amount = Float()
        delivery_executive = String()
        delivery_address = String()
        status = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        order = Order.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('amount'):
            order.amount = input.get('amount')
        exec_id = input.get('delivery_executive')
        if exec_id:
            delivery_exec_obj = DeliveryExecutive.objects.get(pk=from_global_id(exec_id)[1])
            order.delivery_executive = delivery_exec_obj
        addr = input.get('delivery_address')
        if addr:
            delivery_addr_obj = CustomerAddress.objects.get(pk=from_global_id(addr)[1])
            order.delivery_address = delivery_addr_obj
        if input.get('status'):
            order.status = input.get('status')
        order.save()
        return UpdateOrder(success=True)


class UpdateOrderItems(ClientIDMutation):
    success = String()
    class Input:
        id = String()
        quantity = Int()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        order_items = OrderItems.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('quantity'):
            order_items.quantity = input.get('quantity')
        order_items.save()
        return UpdateOrderItems(success=True)


class DeleteOrder(ClientIDMutation):
    success = String()
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        order = Order.objects.get(pk=from_global_id(input.get('id'))[1])
        order.delete()
        return DeleteOrder(success=True)


class DeleteOrderItems(ClientIDMutation):
    success = String()
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        order_item = OrderItems.objects.get(pk=from_global_id(input.get('id'))[1])
        order_item.delete()
        return DeleteOrderItems(success=True)


class Query(AbstractType):
    order = relay.Node.Field(OrderNode)
    all_order = DjangoFilterConnectionField(OrderNode)
    order_items = relay.Node.Field(OrderItemsNode)
    all_order_items = DjangoFilterConnectionField(OrderItemsNode)


class Mutation(AbstractType):
    new_order = NewOrder.Field()
    new_order_items = NewOrderItems.Field()
    update_order = UpdateOrder.Field()
    update_order_items = UpdateOrderItems.Field()
    delete_order = DeleteOrder.Field()
    delete_order_items = DeleteOrderItems.Field()

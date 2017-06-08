from graphene import relay, ObjectType, AbstractType, ClientIDMutation
from graphene import Field, String, Int, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from django.contrib.auth.models import User
from models import Customer, CustomerAddress, DeliveryExecutive


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = {'full_name': ['exact', 'icontains']}
        interfaces = (relay.Node, )


class CustomerAddressNode(DjangoObjectType):
    class Meta:
        model = CustomerAddress
        filter_fields = {'address': ['icontains'] }
        interfaces = (relay.Node, )


class DeliveryExecutiveNode(DjangoObjectType):
    class Meta:
        model = DeliveryExecutive
        filter_fields = {'employee_id': ['exact'],
                         'full_name': ['exact', 'icontains']
                        }
        interfaces = (relay.Node, )


class NewCustomer(ClientIDMutation):
    success = String()
    class Input:
        username = String()
        first_name = String()
        last_name = String()
        email_address = String()
        passsword = String()
        phone_extension = String()
        phoneno = String()
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = User.objects.create_user(input.get('username'),
                                        input.get('email_address'),
                                        input.get('passsword')
                                       )
        first_name = input.get('first_name')
        last_name = input.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        customer = Customer(
            user = user,
            full_name = first_name + ' ' + last_name,
            phone_extension = input.get('phone_extension'),
            phoneno = input.get('phoneno')
        )
        customer.save()
        return NewCustomer(success=True)


class NewCustomerAddress(ClientIDMutation):
    success = String()
    class Input:
        customer_id = String()
        header = String()
        address = String()
        lat_long = Int()
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        address = CustomerAddress(
            customer = Customer.objects.get(pk=from_global_id(input.get('customer_id'))[1]),
            header = input.get('header'),
            address = input.get('address'),
            lat_long = input.get('lat_long')
        )
        address.save()
        return NewCustomerAddress(success=True)


class NewDeliveryExecutive(ClientIDMutation):
    success = String()
    class Input:
        username = String()
        first_name = String()
        last_name = String()
        email_address = String()
        passsword = String()
        employee_id = String()
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = User.objects.create_user(input.get('username'),
                                        input.get('email_address'),
                                        input.get('passsword')
                                       )
        first_name = input.get('first_name')
        last_name = input.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        executive = DeliveryExecutive(
            user = user,
            full_name = first_name + ' ' + last_name,
            employee_id = input.get('employee_id')
        )
        executive.save()
        return NewCustomer(success=True)


class Query(AbstractType):
    user = relay.Node.Field(UserNode)
    all_user = DjangoFilterConnectionField(UserNode)
    customer = relay.Node.Field(CustomerNode)
    all_customer = DjangoFilterConnectionField(CustomerNode)
    customer_address = relay.Node.Field(CustomerAddressNode)
    all_customer_address = DjangoFilterConnectionField(CustomerAddressNode)
    delivery_executive = relay.Node.Field(DeliveryExecutiveNode)
    all_delivery_executive = DjangoFilterConnectionField(DeliveryExecutiveNode)


class Mutation(AbstractType):
    new_customer = NewCustomer.Field()
    new_customer_address = NewCustomerAddress.Field()
    new_delivery_executive = NewDeliveryExecutive.Field()


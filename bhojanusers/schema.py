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
    customer = Field(CustomerNode)
    class Input:
        username = String()
        first_name = String()
        last_name = String()
        email_address = String()
        password = String()
        phone_extension = String()
        phoneno = String()
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = User.objects.create_user(input.get('username'),
                                    input.get('email_address'),
                                    input.get('password')
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
        return NewCustomer(customer=customer)


class NewCustomerAddress(ClientIDMutation):
    address = Field(CustomerAddressNode)
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
        return NewCustomerAddress(address=address)


class NewDeliveryExecutive(ClientIDMutation):
    executive = Field(DeliveryExecutiveNode)
    class Input:
        username = String()
        first_name = String()
        last_name = String()
        email_address = String()
        password = String()
        employee_id = String()
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = User.objects.create_user(input.get('username'),
                                        input.get('email_address'),
                                        input.get('password')
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
        return NewDeliveryExecutive(executive=executive)


class UpdateUser(ClientIDMutation):
    user = Field(UserNode)
    class Input:
        id = String()
        first_name = String()
        last_name = String()
        password = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('first_name'):
            user.first_name = input.get('first_name')
        if input.get('last_name'):
            user.last_name = input.get('last_name')
        if input.get('password'):
            user.set_password(input.get('password'))
        user.save()
        return UpdateUser(user=user)


class UpdateCustomer(ClientIDMutation):
    customer = Field(CustomerNode)
    class Input:
        id = String()
        phone_extension = String()
        phoneno = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        customer = Customer.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('phone_extension'):
            customer.phone_extension = input.get('phone_extension')
        if input.get('last_name'):
            customer.phoneno = input.get('phoneno')
        customer.save()
        return UpdateCustomer(customer=customer)


class UpdateCustomerAddress(ClientIDMutation):
    address = Field(CustomerAddressNode)
    class Input:
        id = String()
        header = String()
        address = String()
        lat_long = Int()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        customer_address = CustomerAddress.objects.get(pk=from_global_id(input.get('id'))[1])
        if input.get('header'):
            customer_address.header = input.get('header')
        if input.get('address'):
            customer_address.address = input.get('address')
        if input.get('lat_long'):
            customer_address.lat_long = input.get('lat_long')
        customer_address.save()
        return UpdateCustomerAddress(address=address)


class DeleteUser(ClientIDMutation):
    user = Field(UserNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = User.objects.get(pk=from_global_id(input.get('id'))[1])
        user.delete()
        return DeleteUser(user=user)


class DeleteCustomer(ClientIDMutation):
    customer = Field(CustomerNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        customer = Customer.objects.get(pk=from_global_id(input.get('id'))[1])
        customer.delete()
        return DeleteCustomer(customer=customer)


class DeleteCustomerAddress(ClientIDMutation):
    address = Field(CustomerAddressNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        address = CustomerAddress.objects.get(pk=from_global_id(input.get('id'))[1])
        address.delete()
        return DeleteCustomerAddress(address=address)


class DeleteDeliveryExecutive(ClientIDMutation):
    executive = Field(DeliveryExecutiveNode)
    class Input:
        id = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        executive = DeliveryExecutive.objects.get(pk=from_global_id(input.get('id'))[1])
        executive.delete()
        return DeleteDeliveryExecutive(executive=executive)


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
    update_user = UpdateUser.Field()
    update_customer = UpdateCustomer.Field()
    update_customer_address = UpdateCustomerAddress.Field()
    delete_user = DeleteUser.Field()
    delete_customer = DeleteCustomer.Field()
    delete_customer_address = DeleteCustomerAddress.Field()
    delete_delivery_executive = DeleteDeliveryExecutive.Field()

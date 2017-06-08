# bhojan - Assignment

## Modules

* bhojanuser
* bhojanmenu

* bhojanorder


### GQL query functions

* user

* all_user

* customer

* all_customer

* customer_address

* all_customer_address

* delivery_executive

* all_delivery_executive


* food

* all_food

* menu

* all_menu


* order

* all_order

* order_items

* all_order_items


### Mutations

* new_customer

* new_customer_address

* new_delivery_executive

* update_user

* update_customer_address

* update_delivery_executive

* delte_customer

* delete_customer_address

* delete_delivery_executive


* new_food

* new_menu

* update_food

* update_menu

* delete_menu

* delete_order


* new_order

* new-order_items

* update_order

* update_order_items

* delete_order

* delete_order_items


### Example:

```javascript
query {
  allCustomer {
    edges {
      node {
        id,
        fullName
      }
    }
  }
}

mutation {
  newCustomer(input:{username:"user3",
    firstName:"third",
    lastName: "user",
    emailAddress: "third@user3.com",
    phoneExtension: "+91",
    phoneno: "123458547"}) {
      customer {
        id,
        emailAddress
      }
    }
}

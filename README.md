# webstore
Simple backend app on Django, DRF, with JWT
## api/sign_in
## POST request
### Body:
{

    "username": string,
    
    "password": string,
    
    "email": string
    
}
Take data, check username to be unique and save new user in db
### return:
or 
status 200
{
    "massage": "success"
}

or 
status 400
{
    "error": "username is used"
}

## api/login_view
## POST request
### Body:
{

    "username": string,
    
    "password": string,
    
}
Take data, check if user exist, login user
### return
or 
status 200
{
    "access_token": string
    "user": {
        "id": int,
        "username": string,
        "email": string
    }
}
in Cookies return {"csrftoken": string, "refreshtoken": string}

or status 403

{
    "detail": "user not found"
}
## api/refresh_token
## POST request
in headers should include:

"X-CSRFTOKEN": string (frontend take it from cookies)

take refresh token from cookies check, if user can refresh token, refresh jwt for user

###return
or
status 200 

{
    "access_token": string
}

or 
status 403

{
    "detail": "Authentication credentials were not provided."
}

## api/get_all_products

##GET request
in headers should contain:

"Authorization": "Token str_user_token"

## return 
status 200

list of product objects

##api/get_order
## GET request 
in headers should contain:

"Authorization": "Token str_user_token"

if user is superuser:

with param -> category=completed

return list of completed orders

with param -> category=uncompleted

return list of un-completed orders

with param -> category=user&user_id=int

return users orders

without param will return list of all orders

if user is regular user:

return list of his/her orders

## api/post_order
## POST request

in headers should contain:

"X-CSRFTOKEN": string,
"Authorization": "Token str_user_token"

###Body:

{
    "address": string,
    
    "phone": string,
    
    "items": [
        {
        "product_id": int, 
        "amount": int
        }, 
        {
        "product_id": int,
        "amount": int
         }
     ]
}

return Order object, if all products exist and have required amount

else 
status 400

error massage



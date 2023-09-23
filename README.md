
# Dive Logger API

This is a REST API for Dive Logger. Developed for educational and personal purposes.




## Tech Stack

**Rest Api:** Python, FastApi

**Database:** MongoDB, Motor(Async driver for Python)



## Features

- Saving/Updating/Retrieving user profiles(in progress)
- Authorization(done)


Other features would be described here later...


## Authorization

I have chosen quite simple algorithm of Authorization.


Here are some explanations:

- As UI I have a telegram bot, so I don't want my users to type their logins and passwords for authentication in Dive Logger API.
- Very few clients would use Dive Logger API(telegram bot and maybe some individuals)
- In case I would have a website or an app - I would enhance authorization and add authentication

A token is given to required clients(telegram bot or maybe some individual) manually. It is:

- Non-expiring
- Revocable(right now manually, because I don't plan to have to many tokens)

#### Token should be passed in headers as 'token'. 
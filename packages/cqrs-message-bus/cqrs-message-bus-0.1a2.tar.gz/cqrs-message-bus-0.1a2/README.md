# Python Message Bus

A small framework to enable the CQRS pattern in a Python project.

## Why this?

To ease the application of the CQRS pattern at code level within the same project.

## What provides?

- A `Command` base class
- An `Event` base class
- An in-memory `MessageBus` to subscribe to commands and events.
- A `UnitOfWork` to put all things together


## Use case

This script should run as is.

```python
from dataclasses import dataclass
from email.message import EmailMessage

from mb import MessageBus, Command, Event
from mb.unit_of_work import UnitOfWork


# -------------------------------------
# User Domain
# -------------------------------------

# Define the database models


@dataclass
class User:
    username: str
    email: str


users_db: list[User] = []


# Define commands and events


@dataclass
class CreateUser(Command):
    username: str
    email: str


@dataclass
class UserCreated(Event):
    username: str
    email: str

    def __hash__(self):
        """Although not required, this supports event deduplication"""
        return self.username


# Define your own command and event handlers


def create_user(cmd: CreateUser, uow: UnitOfWork) -> User:
    with uow:
        # Create
        user = User(username=cmd.username, email=cmd.email)
        users_db.append(user)
        # Emit event
        user_created = UserCreated(username=cmd.username, email=cmd.email)
        uow.emit_event(user_created)
        # Commands can return a value
        return user


def send_welcome_email(e: UserCreated, _: UnitOfWork):
    """
    This might belong to the User domain
    """
    print(f"Sending welcome email: 'Welcome {e.username}!'")


# -------------------------------------
# Integration-ABC Domain
# -------------------------------------


def sync_integration(e: UserCreated, _: UnitOfWork):
    """
    This might belong to another domain
    """
    print(f"Synchronizing user: '{e.username}'")


# -------------------------------------
# XYZ Domain
# -------------------------------------


def do_other_stuff(e: UserCreated, _: UnitOfWork):
    """
    and so on...
    """


# -------------------------------------
# Bootstrap the bus
# -------------------------------------

bus = MessageBus()
bus.subscribe_command(CreateUser, create_user)
bus.subscribe_event(UserCreated, send_welcome_email)
bus.subscribe_event(UserCreated, sync_integration)
bus.subscribe_event(UserCreated, do_other_stuff)


# -------------------------------------
# Instance a UoW
# -------------------------------------

# You should create a new UoW instance for every request or contextual run.

uow = UnitOfWork(bus)
user = uow.handle_command(CreateUser("me", "me@message.bus"))
print("User is", user)
```


## Django integration

This is a work in progress.

Currently, there is a `DjangoUnitOfWork` class to integrate the UoW with the
Django ORM machinery.

Further support will be:
- A Django app with handlers autodiscovery (similar to Celery tasks.py file)
- A Django middleware to automatically inject the UoW into the request.META


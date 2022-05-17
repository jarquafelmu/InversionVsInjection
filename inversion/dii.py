"""Inversion vs Injection video

https://youtu.be/2ejbLVkCndI
"""

import random
import string
from abc import ABC, abstractmethod


class Authorizer(ABC):
    """Makes the actual authorizer agent generic so more could be added
    """
    @abstractmethod
    def authorize(self):
        """stub for authorize
        """
        ...

    @abstractmethod
    def is_authorized(self) -> bool:
        """stub for is_authorized"""
        ...


class Order:
    """Represents a customer's order"""

    def __init__(self) -> None:
        self.id = ''.join(random.choices(string.ascii_lowercase, k=6))
        self.status = "open"

    def set_status(self, status: str) -> None:
        """sets the status of this order

        Args:
            status (str): the status
        """
        self.status = status


class AuthorizerSMS(Authorizer):
    """Authorizes purchase by sending a SMS message to the customer
    and verifying the code they send back is the one that was sent.
    """

    def __init__(self) -> None:
        self.authorized = False
        self.code = None

    def generate_sms_code(self):
        """Generates a SMS code
        """
        self.code = ''.join(random.choices(string.digits, k=6))

    def authorize(self):
        """Verifies the SMS code given by the customer is correct."""
        code = input("Enter SMS code: ")
        self.authorized = code == self.code

    def is_authorized(self) -> bool:
        """if this was authorized by the user

        Returns:
            bool: the status of authorized
        """
        return self.authorized


class AuthorizerRobot(Authorizer):
    """Authorizes purchase by sending a SMS message to the customer
    and verifying the code they send back is the one that was sent.
    """

    def __init__(self) -> None:
        self.authorized = False

    def authorize(self):
        """Verifies the SMS code given by the customer is correct."""
        robot = ""
        while robot != "y" and robot != "n":
            robot = input("are you a robot (y/n)? ").lower()
        self.authorized = robot == "n"

    def is_authorized(self) -> bool:
        """if this was authorized by the user

        Returns:
            bool: the status of authorized
        """
        return self.authorized


class PaymentProcessor:
    """Represents a payment processor"""

    def __init__(self, authorizer: Authorizer) -> None:
        self.authorizer = authorizer

    def pay(self, order: Order):
        """processes the payment

        Args:
            order (Order): The customer's order

        Raises:
            Exception: Authorization check
        """
        self.authorizer.authorize()
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized.")
        print(f"Processing payment for order with id {order.id}")
        order.set_status("paid")

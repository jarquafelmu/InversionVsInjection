"""unit tests for dii"""

import unittest
from unittest.mock import patch
from dii import AuthorizerSMS, Order, PaymentProcessor


class OrderTestCase(unittest.TestCase):
    """Tests the Order class
    """

    def test_init(self):
        """status is initially "open"
        """
        order = Order()
        self.assertEqual(order.status, "open")

    def test_set_status(self):
        """set_status actually sets the status
        """
        order = Order()
        order.set_status("paid")
        self.assertEqual(order.status, "paid")


class AuthorizerSMSTestCase(unittest.TestCase):
    """Tests the AuthorizerSMS class
    """

    def test_init_authorized(self):
        """is_authorized is initially False"""
        auth = AuthorizerSMS()
        self.assertFalse(auth.is_authorized())

    def test_code_decimal(self):
        """code must be a decimal"""
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        self.assertTrue(auth.code.isdecimal())

    def test_authorize_success(self):
        """A correct code authorizes"""
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        # patch replaces what happens when you call the first value
        # in this case it replaces input
        with patch("builtins.input", return_value=auth.code):
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    @patch("builtins.input", return_value="1234567")
    def test_authorize_fail(self, mocked_input):
        """An incorrect code fails to authorize"""
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        auth.authorize()
        self.assertFalse(auth.is_authorized())


class PaymentProcessorTestCase(unittest.TestCase):
    """Tests the PaymentProcessor class
    """

    def test_init(self):
        """The authorizer given to payment processor must
        be the same one that was generated outside of it
        """
        auth = AuthorizerSMS()
        pay = PaymentProcessor(auth)
        self.assertEqual(pay.authorizer, auth)

    def test_payment_success(self):
        """a paid order is set to "paid"
        """
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        with patch("builtins.input", return_value=auth.code):
            pay = PaymentProcessor(auth)
            order = Order()
            pay.pay(order)
            self.assertEqual(order.status, "paid")

    def test_payment_fail(self):
        """payment wasn't authorized
        """
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        with patch("builtins.input", return_value="1234567"):
            pay = PaymentProcessor(auth)
            order = Order()
            self.assertRaises(Exception, pay.pay, order)


if __name__ == "__main__":
    unittest.main()

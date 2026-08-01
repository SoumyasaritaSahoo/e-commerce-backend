"""Common payment gateway interface (docs/09-tech-stack.md, docs/10-project-structure.md).

Concrete gateways (razorpay.py, stripe.py) implement this so the rest of
the payments app never branches on which gateway is active.
"""

from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def create_payment(self, order, amount, currency):
        """Start a payment for an order; return a gateway-specific reference."""
        raise NotImplementedError

    @abstractmethod
    def verify_webhook(self, request):
        """Verify an incoming webhook's signature; return the parsed event."""
        raise NotImplementedError

    @abstractmethod
    def refund(self, payment, amount):
        """Issue a refund against a previously captured payment."""
        raise NotImplementedError

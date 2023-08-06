#
# This class was auto-generated.
#
from abc import ABCMeta, abstractmethod


class IMerchantClient:
    """
    Merchant client interface. Thread-safe.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def hosted_checkout(self):
        """
        Resource /v2/{merchantId}/hostedcheckouts

        :return: :class:`onlinepayments.sdk.merchant.hostedcheckout.i_hosted_checkout_client.IHostedCheckoutClient`
        """
        pass

    @abstractmethod
    def hosted_tokenization(self):
        """
        Resource /v2/{merchantId}/hostedtokenizations

        :return: :class:`onlinepayments.sdk.merchant.hostedtokenization.i_hosted_tokenization_client.IHostedTokenizationClient`
        """
        pass

    @abstractmethod
    def mandates(self):
        """
        Resource /v2/{merchantId}/mandates

        :return: :class:`onlinepayments.sdk.merchant.mandates.i_mandates_client.IMandatesClient`
        """
        pass

    @abstractmethod
    def payments(self):
        """
        Resource /v2/{merchantId}/payments

        :return: :class:`onlinepayments.sdk.merchant.payments.i_payments_client.IPaymentsClient`
        """
        pass

    @abstractmethod
    def payouts(self):
        """
        Resource /v2/{merchantId}/payouts

        :return: :class:`onlinepayments.sdk.merchant.payouts.i_payouts_client.IPayoutsClient`
        """
        pass

    @abstractmethod
    def product_groups(self):
        """
        Resource /v2/{merchantId}/productgroups

        :return: :class:`onlinepayments.sdk.merchant.productgroups.i_product_groups_client.IProductGroupsClient`
        """
        pass

    @abstractmethod
    def products(self):
        """
        Resource /v2/{merchantId}/products

        :return: :class:`onlinepayments.sdk.merchant.products.i_products_client.IProductsClient`
        """
        pass

    @abstractmethod
    def services(self):
        """
        Resource /v2/{merchantId}/services

        :return: :class:`onlinepayments.sdk.merchant.services.i_services_client.IServicesClient`
        """
        pass

    @abstractmethod
    def sessions(self):
        """
        Resource /v2/{merchantId}/sessions

        :return: :class:`onlinepayments.sdk.merchant.sessions.i_sessions_client.ISessionsClient`
        """
        pass

    @abstractmethod
    def tokens(self):
        """
        Resource /v2/{merchantId}/tokens

        :return: :class:`onlinepayments.sdk.merchant.tokens.i_tokens_client.ITokensClient`
        """
        pass

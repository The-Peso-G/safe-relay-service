from eth_account import Account

from gnosis.safe.tests.safe_test_case import SafeTestCaseMixin
from gnosis.safe.tests.utils import generate_salt_nonce, generate_valid_s

from safe_relay_service.gas_station.gas_station import GasStationProvider

from ..models import SafeCreation, SafeCreation2
from ..services.safe_creation_service import SafeCreationServiceProvider
from ..services.transaction_service import TransactionServiceProvider


class RelayTestCaseMixin(SafeTestCaseMixin):
    @classmethod
    def prepare_tests(cls):
        super().prepare_tests()
        cls.gas_station = GasStationProvider()
        SafeCreationServiceProvider.del_singleton()
        TransactionServiceProvider.del_singleton()
        cls.safe_creation_service = SafeCreationServiceProvider()
        cls.transaction_service = TransactionServiceProvider()

    def create_test_safe_in_db(self, owners=None, number_owners=3, threshold=None,
                               payment_token=None) -> SafeCreation:
        s = generate_valid_s()
        owners = owners or [Account.create().address for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners)

        safe_creation = self.safe_creation_service.create_safe_tx(s, owners, threshold, payment_token)
        return safe_creation

    def create2_test_safe_in_db(self, owners=None, number_owners=3, threshold=None,
                                payment_token=None, salt_nonce=None) -> SafeCreation2:

        salt_nonce = salt_nonce or generate_salt_nonce()
        owners = owners or [Account.create().address for _ in range(number_owners)]
        threshold = threshold if threshold else len(owners)

        return self.safe_creation_service.create2_safe_tx(salt_nonce, owners, threshold, payment_token)

from loguru import logger
from config import PHI_PROTOCOL_ABI, PHI_PROTOCOL_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class PhiProtocol(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Phi Protocol NFT")

        contract = self.get_contract(PHI_PROTOCOL_CONTRACT, PHI_PROTOCOL_ABI)

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.mint(self.address).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

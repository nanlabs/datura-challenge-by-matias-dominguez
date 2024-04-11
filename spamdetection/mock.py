import time
import asyncio
import random
import bittensor as bt

from typing import List

from spamdetection.protocol import SpamDetectionSynapse, SpamAssessmentResult


class MockSubtensor(bt.MockSubtensor):
    def __init__(self, netuid, n=16, wallet=None, network="mock"):
        super().__init__(network=network)

        if not self.subnet_exists(netuid):
            self.create_subnet(netuid)

        # Register ourself (the validator) as a neuron at uid=0
        if wallet is not None:
            self.force_register_neuron(
                netuid=netuid,
                hotkey=wallet.hotkey.ss58_address,
                coldkey=wallet.coldkey.ss58_address,
                balance=100000,
                stake=100000,
            )

        # Register n mock neurons who will be miners
        for i in range(1, n + 1):
            self.force_register_neuron(
                netuid=netuid,
                hotkey=f"miner-hotkey-{i}",
                coldkey="mock-coldkey",
                balance=100000,
                stake=100000,
            )


class MockMetagraph(bt.metagraph):
    def __init__(self, netuid=1, network="mock", subtensor=None):
        super().__init__(netuid=netuid, network=network, sync=False)

        if subtensor is not None:
            self.subtensor = subtensor
        self.sync(subtensor=subtensor)

        for axon in self.axons:
            axon.ip = "127.0.0.0"
            axon.port = 8091

        bt.logging.info(f"Metagraph: {self}")
        bt.logging.info(f"Axons: {self.axons}")


class MockDendrite(bt.dendrite):
    """
    Replaces a real bittensor network request with a mock request that just returns some static response for all axons that are passed and adds some random delay.
    """

    def __init__(self, wallet):
        super().__init__(wallet)

    async def forward(
        self,
        axons: List[bt.axon],
        synapse: SpamDetectionSynapse = SpamDetectionSynapse(),
        timeout: float = 12,
        deserialize: bool = True,
        run_async: bool = True,
        streaming: bool = False,
    ):
        if streaming:
            raise NotImplementedError("Streaming not implemented yet.")

        async def query_all_axons(streaming: bool):
            """Queries all axons for responses."""

            async def single_axon_response(i, axon):
                """Simulates querying a single axon for a spam assessment response."""

                start_time = time.time()
                s = synapse.copy()
                # Simulate processing
                process_time = random.random()
                if process_time < timeout:
                    # Mock spam assessment
                    s.evaluation_response = SpamAssessmentResult(
                        request_id=s.evaluation_request.request_id,
                        is_spam=random.choice([True, False]),
                        confidence=random.uniform(0.5, 1.0),
                    )
                    s.dendrite.process_time = str(time.time() - start_time)
                    s.dendrite.status_code = 200
                    s.dendrite.status_message = "OK"
                else:
                    # Simulate a timeout scenario
                    s.dendrite.status_code = 408
                    s.dendrite.status_message = "Timeout"

                # Return the updated synapse object after deserializing if requested
                if deserialize:
                    return s.evaluation_response
                else:
                    return s

            return await asyncio.gather(
                *(
                    single_axon_response(i, target_axon)
                    for i, target_axon in enumerate(axons)
                )
            )

        return await query_all_axons(streaming)

    def __str__(self) -> str:
        """
        Returns a string representation of the MockDendrite object.

        Returns:
            str: The string representation of the MockDendrite object in the format "MockDendrite(<user_wallet_address>)".
        """
        return f"MockDendrite({self.wallet.ss58_address})"

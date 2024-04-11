# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2024 Matias Dominguez

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import time
import typing
import bittensor as bt

from spamdetection.protocol import SpamDetectionSynapse, SpamAssessmentResult
from spamdetection.base.miner import BaseMinerNeuron
from spamdetection.utils.is_spam import is_spam


class Miner(BaseMinerNeuron):
    """
    Custom miner neuron class for spam detection. Inherits from BaseMinerNeuron, which provides
    setup for wallet, subtensor, metagraph, and more. Override methods as needed for specific behaviors.
    """

    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)
        # Custom initialization for the spam detection miner

    async def forward(self, synapse: SpamDetectionSynapse) -> SpamDetectionSynapse:
        """
        Analyzes the message within the synapse for spam and responds with an assessment.

        Args:
            synapse (SpamDetectionSynapse): Contains the message for spam detection.

        Returns:
            SpamDetectionSynapse: Updated with the spam assessment result.
        """
        synapse.evaluation_response = is_spam(synapse.evaluation_request)
        return synapse

    async def blacklist(self, synapse: SpamDetectionSynapse) -> typing.Tuple[bool, str]:
        """
        Determines if an incoming request should be blacklisted.

        Args:
            synapse (SpamDetectionSynapse): Synapse object from the request headers.

        Returns:
            Tuple[bool, str]: Whether the request is blacklisted, and reason if so.
        """
        # Implement blacklist logic based on request details
        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            # Ignore requests from un-registered entities.
            bt.logging.trace(
                f"Blacklisting un-registered hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        if self.config.blacklist.force_validator_permit:
            # If the config is set to force validator permit, then we should only allow requests from validators.
            if not self.metagraph.validator_permit[uid]:
                bt.logging.warning(
                    f"Blacklisting a request from non-validator hotkey {synapse.dendrite.hotkey}"
                )
                return True, "Non-validator hotkey"

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"

    async def priority(self, synapse: SpamDetectionSynapse) -> float:
        """
        Assigns priority to requests based on criteria like stake.

        Args:
            synapse (SpamDetectionSynapse): Contains request metadata.

        Returns:
            float: Priority score.
        """
        # Implement priority logic (e.g., based on stake)
        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )  # Get the caller index.
        priority = float(
            self.metagraph.S[caller_uid]
        )  # Return the stake as the priority.
        bt.logging.trace(
            f"Prioritizing {synapse.dendrite.hotkey} with value: ", priority
        )
        return priority


# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)

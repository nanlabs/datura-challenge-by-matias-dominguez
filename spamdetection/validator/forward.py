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

import bittensor as bt

from spamdetection.protocol import SpamDetectionSynapse, EvaluationRequest
from spamdetection.validator.reward import get_rewards
from spamdetection.utils.uids import get_random_uids


async def forward(self):
    """
    The forward function is called by the validator at every time step.

    It is responsible for querying the network with spam detection queries and scoring the responses based on accuracy.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

    """
    # Example method to select miner uids to query, replace or modify as needed.
    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

    # Example spam message to send for detection.
    # In a real scenario, you would cycle through or randomly generate spam/non-spam messages.
    # For the validator this is not a spam message because it does not contain the word "spam".
    example_message = "Simple message!"

    # randomly decide whether to add a spam keyword to the message.
    # For the purpose of this example, the validator will assume the message is spam if it contains the word "spam".
    if bt.random.uniform(0, 1) > 0.5:
        example_message = "This is a spam message: Earn money fast!"

    # The dendrite client queries the network with spam detection requests.
    responses = await self.dendrite(
        # Send the query to selected miner axons in the network.
        axons=[self.metagraph.axons[uid] for uid in miner_uids],
        # Construct a SpamDetectionSynapse query.
        synapse=SpamDetectionSynapse(
            evaluation_request=EvaluationRequest(
                request_id=self.step, message=example_message
            )
        ),
        # Ensure responses are deserialized according to SpamDetectionSynapse specification.
        deserialize=True,
    )

    # Log the results for monitoring purposes.
    bt.logging.info(f"Received responses: {responses}")

    # Process responses to determine accuracy and issue rewards.
    # This is an example function, you'll need to define scoring based on correctness of spam detection.
    rewards = get_rewards(self, message=example_message, responses=responses)

    bt.logging.info(f"Scored responses: {rewards}")
    # Update the scores based on the rewards.
    # This function should be implemented to reflect how you adjust miner scores/rewards based on their performance.
    self.update_scores(rewards, miner_uids)

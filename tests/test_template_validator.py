import asyncio
import sys
import torch
import unittest
import bittensor as bt

from spamdetection.protocol import (
    SpamDetectionSynapse,
    EvaluationRequest,
    SpamAssessmentResult,
)
from spamdetection.validator import ValidatorNeuron
from spamdetection.utils.uids import get_random_uids
from spamdetection.validator.reward import get_rewards


class SpamDetectionValidatorNeuronTestCase(unittest.TestCase):
    """
    Unit tests for the spam detection validator neuron, focusing on the evaluation and reward system for miners.
    """

    def setUp(self):
        # Simplified setup assuming a configuration method similar to what was previously described.
        sys.argv = sys.argv[:1]  # Resets argv to avoid issues with unittest arguments.
        config = ValidatorNeuron.config()
        config.wallet._mock = True
        config.metagraph._mock = True
        config.subtensor._mock = True
        self.validator = ValidatorNeuron(config)
        self.miner_uids = get_random_uids(self.validator, k=10)

    def test_run_single_step(self):
        # Example placeholder test.
        pass

    def test_sync_error_if_not_registered(self):
        # Example placeholder test.
        pass

    def test_forward(self):
        """
        Test that the forward function correctly evaluates spam detection requests and returns accurate responses.
        """
        # Example of simulating a spam detection request.
        spam_message = "This is a spam message example."
        synapse = SpamDetectionSynapse(
            evaluation_request=EvaluationRequest(request_id=1, message=spam_message)
        )

        # Simulate the forward call
        result_synapse = asyncio.run(self.validator.dendrite.forward(synapse))

        # Assert the response is as expected (Note: This assumes the existence of a mocked forward method)
        self.assertIsInstance(result_synapse.evaluation_response, SpamAssessmentResult)
        self.assertTrue(
            result_synapse.evaluation_response.is_spam
        )  # Assuming the message is identified as spam.

    def test_spamdetection_responses(self):
        """
        Test that spamdetection responses are correctly handled. This is more of a conceptual test,
        as the real implementation would not use spamdetection inputs or expect doubled outputs.
        """
        # This test would need significant adaptation to fit into a spam detection scenario.
        pass

    def test_reward(self):
        """
        Test that the reward function returns the correct values based on miners' responses to spam detection queries.
        """
        # Simulate obtaining responses from the network
        # Note: This section needs adaptation to create a mocked network response scenario.

        # Example of obtaining rewards
        responses = [
            SpamAssessmentResult(request_id=1, is_spam=True, confidence=0.9)
        ] * len(self.miner_uids)
        rewards = get_rewards(self.validator, responses)

        # Assuming all responses are correct and receive a reward of 1.0
        expected_rewards = torch.FloatTensor([1.0] * len(responses)).to(
            self.validator.device
        )
        torch.testing.assert_allclose(rewards, expected_rewards)

    def test_reward_with_nan(self):
        """
        Test that NaN rewards are correctly sanitized and a warning is logged.
        """
        responses = [
            SpamAssessmentResult(request_id=1, is_spam=True, confidence=0.9)
        ] * len(self.miner_uids)
        rewards = get_rewards(self.validator, responses)

        # Intentionally introduce NaN to simulate error handling
        rewards[0] = float("nan")

        # Mocking logging to capture warnings
        with self.assertLogs("bittensor", level="WARNING") as cm:
            sanitized_rewards = self.validator.sanitize_rewards(rewards)
            self.assertNotIn(
                float("nan"), sanitized_rewards, "NaN reward was not sanitized"
            )
            self.assertTrue(
                any("WARNING" in message for message in cm.output),
                "Expected warning log for NaN reward",
            )

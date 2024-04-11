import pytest
import asyncio
import bittensor as bt
from spamdetection.mock import MockDendrite, MockMetagraph, MockSubtensor
from spamdetection.protocol import (
    SpamDetectionSynapse,
    EvaluationRequest,
    SpamAssessmentResult,
)


@pytest.mark.parametrize("netuid", [1, 2, 3])
@pytest.mark.parametrize("n", [2, 4, 8, 16, 32, 64])
@pytest.mark.parametrize("wallet", [bt.MockWallet(), None])
def test_mock_subtensor(netuid, n, wallet):
    subtensor = MockSubtensor(netuid=netuid, n=n, wallet=wallet)
    neurons = subtensor.neurons(netuid=netuid)
    # Check netuid
    assert subtensor.subnet_exists(netuid)
    # Check network
    assert subtensor.network == "mock"
    assert subtensor.chain_endpoint == "mock_endpoint"
    # Check number of neurons
    assert len(neurons) == (n + 1 if wallet is not None else n)
    # Check wallet
    if wallet is not None:
        assert subtensor.is_hotkey_registered(
            netuid=netuid, hotkey_ss58=wallet.hotkey.ss58_address
        )

    for neuron in neurons:
        assert type(neuron) == bt.NeuronInfo
        assert subtensor.is_hotkey_registered(netuid=netuid, hotkey_ss58=neuron.hotkey)


@pytest.mark.parametrize("n", [16, 32, 64])
def test_mock_metagraph(n):
    mock_subtensor = MockSubtensor(netuid=1, n=n)
    mock_metagraph = MockMetagraph(subtensor=mock_subtensor)
    # Check axons
    axons = mock_metagraph.axons
    assert len(axons) == n
    # Check ip and port
    for axon in axons:
        assert type(axon) == bt.AxonInfo
        assert axon.ip == mock_metagraph.default_ip
        assert axon.port == mock_metagraph.default_port


@pytest.mark.skip(reason="TODO: Define how to test the mock reward pipeline.")
def test_mock_reward_pipeline():
    # TODO: Implement this test to verify the mock reward pipeline functionality.
    pass


@pytest.mark.skip(reason="TODO: Define how to test the mock neuron behavior.")
def test_mock_neuron():
    # TODO: Implement this test to simulate neuron behavior and validate it.
    pass


@pytest.mark.parametrize("timeout", [0.1, 0.2])
@pytest.mark.parametrize("min_time", [0, 0.05, 0.1])
@pytest.mark.parametrize("max_time", [0.1, 0.15, 0.2])
@pytest.mark.parametrize("n", [4, 16, 64])
def test_mock_dendrite_timings(timeout, min_time, max_time, n):
    mock_wallet = None
    mock_dendrite = MockDendrite(mock_wallet)
    mock_dendrite.min_time = min_time
    mock_dendrite.max_time = max_time
    mock_subtensor = MockSubtensor(netuid=1, n=n)
    mock_metagraph = MockMetagraph(subtensor=mock_subtensor)
    axons = mock_metagraph.axons

    async def run():
        return await mock_dendrite(
            axons,
            synapse=SpamDetectionSynapse(
                evaluation_request=EvaluationRequest(
                    request_id=1, message="What is the capital of France?"
                )
            ),
            timeout=timeout,
        )

    responses = asyncio.run(run())
    for synapse in responses:
        assert (
            hasattr(synapse, "dendrite") and type(synapse.dendrite) == bt.TerminalInfo
        )

        dendrite = synapse.dendrite
        # Check for expected attributes in the dendrite response.
        for field in ("process_time", "status_code", "status_message"):
            assert hasattr(dendrite, field) and getattr(dendrite, field) is not None

        # Verify dendrite response times fall within expected ranges.
        assert min_time <= float(dendrite.process_time) <= max_time + timeout
        # Check responses timing and status codes.
        if float(dendrite.process_time) > timeout:
            assert dendrite.status_code == 408
            assert dendrite.status_message == "Timeout"
        else:
            assert dendrite.status_code == 200
            assert dendrite.status_message == "OK"

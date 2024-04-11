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

import typing
import bittensor as bt

class EvaluationRequest:
    """
    Represents a request to evaluate a message for spam detection.

    Attributes:
    - request_id (int): A unique identifier for the request.
    - message (str): The message text to be evaluated for potential spam.
    """
    def __init__(self, request_id: int, message: str):
        self.request_id = request_id
        self.message = message

class SpamAssessmentResult:
    """
    Encapsulates the result of spam assessment for a message.

    Attributes:
    - request_id (int): The unique identifier of the request, matching the EvaluationRequest.
    - is_spam (bool): Indicates whether the message was determined to be spam.
    - confidence (float): A confidence score for the spam assessment, ranging from 0 to 1.
    """
    def __init__(self, request_id: int, is_spam: bool, confidence: float):
        self.request_id = request_id
        self.is_spam = is_spam
        self.confidence = confidence

class SpamDetectionSynapse(bt.Synapse):
    """
    A protocol representation for spam detection, utilizing bt.Synapse as its base.
    Facilitates communication for spam message evaluation between the validator and the miner.

    Attributes:
    - evaluation_request (EvaluationRequest): A structured request containing the message to be evaluated.
    - evaluation_response (typing.Optional[SpamAssessmentResult]): The miner's response, including whether the message is spam and the confidence level.
    """

    # The message for spam evaluation, filled by the validator.
    evaluation_request: 'EvaluationRequest'

    # The assessment result from the miner, indicating if the message is spam.
    evaluation_response: typing.Optional['SpamAssessmentResult'] = None

    def deserialize(self) -> 'SpamAssessmentResult':
        """
        Deserializes the evaluation response from the miner, allowing it to be processed or displayed.

        Returns:
        - SpamAssessmentResult: The deserialized response, encapsulating the spam detection verdict and confidence level.
        """
        return self.evaluation_response

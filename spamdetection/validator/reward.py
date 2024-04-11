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

import torch
from typing import List
from spamdetection.protocol import EvaluationRequest, SpamAssessmentResult

def reward(expected_spam: bool, response: SpamAssessmentResult) -> float:
    """
    Calculate the reward for a single miner's response based on the accuracy of their spam detection.
    
    Args:
    - expected_spam (bool): Whether the message sent in the query was spam.
    - response (SpamAssessmentResult): The miner's response to the spam detection request.
    
    Returns:
    - float: The reward value for the miner, based on the correctness of their response.
    """
    # This simplistic model rewards correct detections with 1 and incorrect with 0.
    # Adjust this logic as needed to account for confidence levels or other factors.
    if response.is_spam == expected_spam:
        return 1.0
    else:
        return 0

def get_rewards(
    self,
    message: str,
    responses: List[SpamAssessmentResult],
) -> torch.FloatTensor:
    """
    Calculate rewards for a batch of miner responses to a spam detection query.

    Args:
    - message (str): The message that was sent to miners for spam detection.
    - responses (List[SpamAssessmentResult]): The list of responses from miners.
    
    Returns:
    - torch.FloatTensor: A tensor containing the reward values for each response.
    """
    # Example logic to decide if the original message was intended to be spam or not.
    # Replace or refine this with your actual logic or predefined labels.
    expected_spam = "spam" in message.lower()
    
    # Calculate rewards for each response based on its accuracy.
    rewards = [reward(expected_spam, response) for response in responses]
    
    return torch.FloatTensor(rewards).to(self.device)

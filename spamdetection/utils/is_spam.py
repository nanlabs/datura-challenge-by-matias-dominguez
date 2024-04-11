from spamdetection.protocol import EvaluationRequest, SpamAssessmentResult


def is_spam(evaluation_request: EvaluationRequest) -> SpamAssessmentResult:
    """
    Determines whether a message is spam based on a simplistic keyword matching approach.

    This function serves as a simplified example to illustrate the concept of message
    validation in a proof of concept (POC) for a system where a miner analyzes messages
    to detect spam. It is not intended for real-world spam detection, which would require
    more sophisticated methods.

    Parameters:
    - evaluation_request (EvaluationRequest): An instance of EvaluationRequest containing
      the 'request_id' and 'message' to be analyzed.

    Returns:
    - SpamAssessmentResult: An instance of SpamAssessmentResult containing the original
      'request_id', a boolean 'is_spam' indicating if the message is considered spam, and
      a 'confidence' field representing the confidence level of the spam assessment.

    Example:
    >>> evaluation_request = EvaluationRequest(request_id=1, message="Earn money easily from your home!")
    >>> result = is_spam(evaluation_request)
    >>> print(result.is_spam, result.confidence)
    True 0.95
    """

    # List of simple spam keywords for illustration purposes
    spam_keywords = ["earn money", "easily", "subscribe"]
    confidence = 0.95  # Arbitrary confidence level for this simplistic model

    # Checking if any spam keywords are present in the message
    if any(keyword in evaluation_request.message.lower() for keyword in spam_keywords):
        return SpamAssessmentResult(
            request_id=evaluation_request.request_id,
            is_spam=True,
            confidence=confidence,
        )
    else:
        return SpamAssessmentResult(
            request_id=evaluation_request.request_id, is_spam=False, confidence=0.05
        )  # Low confidence for non-spam messages


"""
In a real-world scenario, spam detection would likely involve more advanced machine learning models
trained on large datasets of labeled messages. These models could utilize techniques such as natural
language processing (NLP) to understand the context and semantics of the messages, rather than relying
on simple keyword matching. Implementing such a model would require collecting a diverse set of training
data, selecting an appropriate model architecture (e.g., neural networks), and continuously updating the
model to adapt to new types of spam.

As a simple next iteration, the function above could import a pre-trained machine learning model and use
it to make predictions on the message text. This would allow for more accurate spam detection based on
the model's learned patterns and generalization capabilities.
"""

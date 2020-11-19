from app.requests import InvalidRequest, InvalidRequestMessage, ValidRequest


def test_invalid_request_message_init():
    parameter = "1"
    message = "Message"
    request = InvalidRequestMessage(parameter=parameter, message=message)
    assert request.parameter == parameter
    assert request.message == message


def test_invalid_request():
    parameter = "1"
    message = "Message"
    message = InvalidRequestMessage(parameter=parameter, message=message)
    request = InvalidRequest()
    assert bool(request) is False

    assert request.has_errors() is False
    request.add_error(**message.dict())
    assert request.has_errors() is True


def test_valid_request():
    request = ValidRequest()
    assert bool(request) is True

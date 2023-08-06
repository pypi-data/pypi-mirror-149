import logging

MAX_PAYLOAD_LENGTH = 25
MAX_TEXT_LENGTH = 100000
ALLOWLIST_TYPE_ID = [str, int]


def to_json(response):
    res_decoded, decoding_err = try_json(response)

    if decoding_err:
        # decoding error, report, but assume unrecoverable
        logging.exception(decoding_err)
        return None

    if not (isinstance(res_decoded, list) or isinstance(res_decoded, dict)):
        logging.error(f"Invalid response type: {type(res_decoded)} (expected: dict)")
        return None

    return res_decoded


def try_json(response):
    """ Decodes response as json, returns decoded and optional error """
    try:
        return response.json(), None
    except ValueError as e:
        return None, e


def check_payload_format(payload: list):
    assert payload, "You should provide a payload"
    assert type(payload) == list, "Payload should be of type list"
    assert (
        len(payload) <= MAX_PAYLOAD_LENGTH
    ), f"Payload should not be longer than {MAX_PAYLOAD_LENGTH} items"
    for item in payload:
        check_item_format(item)


def check_item_format(item: dict):
    assert item.get("id"), "Item does not contain an id key"
    assert (
        type(item.get("id")) in ALLOWLIST_TYPE_ID
    ), "id key should either be a str or a int"

    assert item.get("text"), "Item does not contain a text key"
    assert type(item.get("text")) == str, "text value should be of type str"
    assert (
        len(item.get("text")) <= MAX_TEXT_LENGTH
    ), f"Text should not be longer than {MAX_TEXT_LENGTH} characters"

"""
:Copyright: 2007-2022 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from weitersager.http import _parse_json_message


@pytest.mark.parametrize(
    'channel, text',
    [
        ('#example', 'ohai, kthxbye!'),
        ('#idlers', 'Nothing to see here, move along.'),
    ],
)
def test_parse_json_message(channel, text):
    data = {
        'channel': channel,
        'text': text,
    }

    message = _parse_json_message(data)

    assert message.channel == channel
    assert message.text == text

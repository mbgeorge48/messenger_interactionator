from utils.get_participants import get_participants


def test_get_participants():
    output = get_participants(
        json_string=[
            {"name": "Mr Bean"},
            {"name": "Mr Whimma"},
            {"name": "Gregory Biscuit"},
            {"name": "Wallce"},
            {"name": "Mr Blobby"},
        ]
    )
    assert len(output) == 5
    assert "Mr Bean" in output
    assert "Mr Whimma" in output
    assert "Gregory Biscuit" in output
    assert "Wallce" in output
    assert "Mr Blobby" in output

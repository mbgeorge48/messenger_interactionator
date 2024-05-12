from utils.get_data_to_parse import date_filter, convert_date
from datetime import datetime

test_messages = [
    {
        "sender_name": "Gregory Biscuit",
        "content": "8",
        "timestamp_converted": "2000-08-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "7",
        "timestamp_converted": "2000-07-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "6",
        "timestamp_converted": "2000-06-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "5",
        "timestamp_converted": "2000-05-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "4",
        "timestamp_converted": "2000-04-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "3",
        "timestamp_converted": "2000-03-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "2",
        "timestamp_converted": "2000-02-01 12:00:00",
    },
    {
        "sender_name": "Gregory Biscuit",
        "content": "1",
        "timestamp_converted": "2000-01-01 12:00:00",
    },
]


def test_date_filter__full_range():
    output = date_filter(
        messages=test_messages,
        date_range={"start": "1999-01-01 00:00:00", "end": "2002-01-01 23:59:59"},
    )
    assert len(output) == len(test_messages)


def test_date_filter__smaller_range():
    output = date_filter(
        messages=test_messages,
        date_range={"start": "2000-03-01 00:00:00", "end": "2000-06-01 23:59:59"},
    )
    assert len(output) == 4


def test_date_filter__out_of_range():
    output = date_filter(
        messages=test_messages,
        date_range={"start": "2002-03-01 00:00:00", "end": "2002-06-01 23:59:59"},
    )
    assert len(output) == 0


def test_convert_date__string():
    output = convert_date("2000-01")
    assert output == "2000-01-01 00:00:00"


def test_convert_date__date_object():
    output = convert_date(datetime.strptime("2000-01-01 12:00:00", "%Y-%m-%d %H:%M:%S"))
    assert output == "2000-01-01 12:00:00"


def test_convert_date__string__end_of_the_month():
    output = convert_date("2000-01", True)
    assert output == "2000-01-31 23:59:59"

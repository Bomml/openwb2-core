import datetime
from unittest.mock import MagicMock, Mock
import pytest

from helpermodules import pub, timecheck


@pytest.fixture(autouse=True)
def mock_today(monkeypatch) -> None:
    datetime_mock = MagicMock(wraps=datetime.datetime)
    # Montag 16.05.2022, 8:40:52  "05/16/2022, 08:40:52" Unix: 1652683252
    datetime_mock.today.return_value = datetime.datetime(2022, 5, 16, 8, 40, 52)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)
    mock_today_timestamp = Mock(return_value=1652683252)
    monkeypatch.setattr(timecheck, "create_timestamp_unix", mock_today_timestamp)


@pytest.fixture(autouse=True)
def mock_pub(monkeypatch) -> Mock:
    pub_mock = Mock()
    pub_mock.pub.return_value = None
    monkeypatch.setattr(pub.Pub, 'instance', pub_mock)
    return pub_mock

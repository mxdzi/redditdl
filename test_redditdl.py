import datetime
import json
from unittest.mock import MagicMock, patch, mock_open

import redditdl


@patch('redditdl.Path.mkdir')
@patch('redditdl.requests.Session.get')
@patch('redditdl.date', wraps=datetime.date)
@patch('builtins.open', mock_open())
def test(mock_date, mock_session, mock_path, capsys):
    mock_response_new = MagicMock()
    mock_response_new.status_code = 200
    mock_response_new.json = MagicMock(return_value=json.loads(test_response_new))
    mock_session.side_effect = [mock_response_new,
                                MagicMock(status_code=200, content=b""),
                                MagicMock(status_code=200, content=b""),
                                MagicMock(status_code=200, content=b"")]

    mock_date.today.return_value = datetime.date(2019, 12, 4)

    subreddit = "test"
    redditdl.download(subreddit)

    captured = capsys.readouterr()
    output = ("test 4\n"
              "test https://i.redd.it/2.jpg 2019-12-03 13:00:00\n")
    assert mock_path.call_count == 1
    assert captured.out == output


test_response_new = """
{
    "kind": "Listing",
    "data": {
        "after": null,
        "dist": 25,
        "modhash": "",
        "geo_filter": "",
        "children": [
             {
                "kind": "t3",
                "data": {
                    "post_hint": "image",
                    "created": 1575460800.0,
                    "permalink": "/r/test/comments/aaa/title-1/",
                    "url": "https://i.redd.it/1.jpg"
                }
            },
            {
                "kind": "t3",
                "data": {
                    "created": 1575374400.0,
                    "permalink": "/r/test/comments/bbb/title-2/",
                    "url": "https://i.redd.it/2.jpg"
                }
            },
            {
                "kind": "t3",
                "data": {
                    "post_hint": "image",
                    "created": 1575374400.0,
                    "permalink": "/r/test/comments/ccc/title-3/",
                    "url": "https://i.redd.it/3.jpg"
                }
            },
            {
                "kind": "t3",
                "data": {
                    "post_hint": "image",
                    "created": 1575201600.0,
                    "permalink": "/r/test/comments/ddd/title-4/",
                    "url": "https://i.redd.it/4.jpg"
                }
            }
         ],
        "before": null
    }
}
"""

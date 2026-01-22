import json
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lambda_function.convert_csv import lambda_handler

@patch("lambda_function.convert_csv.boto3")
def test_valid_csv(mock_boto3):
    """Lambda should return success for a simple CSV."""

    # Mock S3 client
    mock_s3 = MagicMock()
    mock_boto3.client.return_value = mock_s3

    # Simulate successful S3 upload
    mock_s3.put_object.return_value = {}

    event = {
        "body": "name,age\njohn,30\nsarah,25"
    }

    result = lambda_handler(event, None)

    print("Lambda returned:", result)

    assert result["statusCode"] == 200

    body = json.loads(result["body"])
    assert "message" in body


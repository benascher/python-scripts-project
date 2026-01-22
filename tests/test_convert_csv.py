import sys
import os
import json
from unittest.mock import patch, MagicMock

# allow import of lambda_function package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lambda_function.convert_csv import lambda_handler

@patch("lambda_function.convert_csv.s3")
def test_valid_csv(mock_s3):
    """Lambda should return success for a simple CSV."""

    # Simulate successful S3 upload
    mock_s3.put_object.return_value = {}

    event = {
        "body": "name,age\njohn,30\nsarah,25"
    }

    result = lambda_handler(event, None)

    print("Lambda returned:", result)

    assert result["statusCode"] == 200

    body = json.loads(result["body"])
    assert "excel_path" in body
    assert body["message"] == "Excel file created successfully"


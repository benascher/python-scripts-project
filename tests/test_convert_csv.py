import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from unittest.mock import patch, MagicMock
from lambda_function.convert_csv import lambda_handler


def test_missing_body():
    """Lambda should return error if no CSV is sent."""
    event = {"body": ""}
    result = lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == 400
    assert "error" in body


def test_valid_csv():
    """Lambda should return success for a simple CSV."""
    event = {
        "body": "name,age\njohn,30\nsarah,25"
    }
    result = lambda_handler(event, None)
    body = json.loads(result["body"])
    print("Lambda returned:", result)


    assert result["statusCode"] == 200
    assert "Excel file created" in body["message"]
    assert "excel_path" in body
    assert body["file_name"].endswith(".xlsx")



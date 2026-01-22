import json
import boto3
import pandas as pd
import io
import datetime


s3 = boto3.client('s3')

BUCKET = "python-scripts12"          
OUTPUT_PREFIX = "output/"             # where Excel files go4 

def lambda_handler(event, context):
    try:
        # ---------------------------
        # 1. Read CSV text from body
        # ---------------------------
        csv_text = event.get("body", "")

        if not csv_text:
            return response(400, {"error": "No CSV data received"})

        # Convert CSV text → dataframe
        rows = [line.split(",") for line in csv_text.split("\n") if line]
        df = pd.DataFrame(rows)

        # ---------------------------
        # 2. Convert to Excel in memory
        # ---------------------------
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)

        # ---------------------------
        # 3. Auto-generate output name
        # ---------------------------
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        output_name = f"converted-{timestamp}.xlsx"
        output_key = OUTPUT_PREFIX + output_name

        # ---------------------------
        # 4. Upload Excel to S3
        # ---------------------------
        s3.put_object(
            Bucket=BUCKET,
            Key=output_key,
            Body=excel_buffer.getvalue(),
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ---------------------------
        # 5. Return successful result
        # ---------------------------
        return response(200, {
            "message": "Excel file created successfully",
            "excel_path": f"s3://{BUCKET}/{output_key}",
            "file_name": output_name
        })

    except Exception as e:
        return response(500, {"error": str(e)})


# ---------------------------
# Helper: Include CORS headers
# ---------------------------
def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps(body)
    }


import os
import boto3
from flask import Flask
from dotenv import load_dotenv

# constants
TABLE = "beograd"

# get environment variables
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


# create flask app
app = Flask(__name__)

client = boto3.client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)
resource = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


# if the table is not there, create it
if client:
    tables = client.list_tables()["TableNames"]

    if not tables:
        print("creating new table: ", TABLE)
        client.create_table(
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
            TableName=TABLE,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
        )
    else:
        table = resource.Table(TABLE)
        print(f"\n {TABLE} table details:")
        print(table.name)
        print(table.creation_date_time)
        print(table.table_name)
        print(table.replicas)
        print(table.table_size_bytes)
        print("\n")
else:
    print("could not connect to aws")


@app.route("/")
def travel():
    s = "travel the world little bug"
    print(s)
    return f"<p>{s}</p>"


# """
# flask --app main run --debug

# """

import boto3
from flask import Flask
from models.photos import Photo

# constants
TABLE = "beograd"


# create flask app
app = Flask(__name__)

# connect to aws dynamodb
client = boto3.client(
    "dynamodb",
)

dynamodb = boto3.resource(
    "dynamodb",
)


tables = client.list_tables()["TableNames"]

if not tables:
    print("creating new table: ", TABLE)
    dynamodb.create_table(
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
        TableName=TABLE,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        BillingMode="PAY_PER_REQUEST",
    )
else:
    table = dynamodb.Table(TABLE)
    print(f"\n {TABLE} table details:")
    print(table.name)
    print(table.creation_date_time)
    print(table.table_size_bytes)
    print("\n\n")
    photo: Photo = Photo(id="1", description="my first picture", likes=88)
    # if table.table_status == 'ACTIVE':
    #     table.put_item(
    #         TableName="beograd",
    #         Item={
    #             "id": 88
    #         },
    #     )
    #     print("added an item")
    print("\n\n")



@app.route("/")
def travel():
    s = "travel the world little bug"
    return f"<p>{s}</p>"


# """
# flask --app app run --debug
# """

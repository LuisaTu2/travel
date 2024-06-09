import boto3
from models.photos import Photo, TableStatus


PHOTOS = "beograd"
BILLING_MODE = "PAY_PER_REQUEST"
COUNTER_ID = "counter"


client = boto3.client(
    "dynamodb",
)
dynamodb = boto3.resource(
    "dynamodb",
)

photos = dynamodb.Table(PHOTOS)


def get_counter():
    if photos.table_status == TableStatus.ACTIVE:
        try:
            counter = photos.get_item(
                TableName=PHOTOS,
                Key={"id": COUNTER_ID},
                AttributesToGet=["value"],
            )
            if counter:
                return counter["Item"]["value"]
        except:
            raise Exception("[GET-COUNTER] could not get index counter")


def update_counter(value: int):
    if photos.table_status == TableStatus.ACTIVE:
        return photos.put_item(
            TableName=PHOTOS, Item={"id": COUNTER_ID, "value": value}
        )


def connect_db():

    tables = client.list_tables()["TableNames"]

    if not tables:
        # TODO: add timestamp
        dynamodb.create_table(
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            TableName=PHOTOS,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            BillingMode=BILLING_MODE,
        )
    else:
        counter = get_counter()
        if not counter:
            update_counter(0)


def add_photo(title, description):
    counter = get_counter()
    counter += 1
    photo = photos.get_item(TableName=PHOTOS, Key={"id": str(counter)})
    if "Item" in photo:
        raise Exception(f"[ADD-PHOTO] photo ix {counter} already exists")
    description = description + " " + str(counter)
    photo: Photo = Photo(id=str(counter), title=title, description=description, likes=0)
    photos.put_item(TableName=PHOTOS, Item=dict(photo))
    photos.put_item(TableName=PHOTOS, Item={"id": COUNTER_ID, "value": counter})

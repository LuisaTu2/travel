import click
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from flask import Flask

from constants import (
    PARTITION_KEY,
    PARTITION_KEY_VALUE,
    PHOTOS,
    PHOTOS_DATA_PATH,
    SORT_KEY,
    TRAVELS,
)
from models import Action, Photo, UpdatePhotoRequest


def register_cli(app: Flask, db, s3):

    # -------------------------------#
    #            DYNAMODB            #
    # -------------------------------#

    # flask create-travels-table
    @app.cli.command("create-travels-table")
    def create_travels_table():
        db.create_travels_table()
        click.echo("[cli-add-travels-table] created travels table")

    # flask delete-table
    @app.cli.command("delete-table")
    @click.argument("table")
    def delete_table(table):
        db.delete_table(table)
        click.echo(f"[cli-delete-table] deleted {table} table")

    # flask delete-item
    @app.cli.command("delete-item")
    @click.argument("table_name")
    @click.argument("pk")
    @click.argument("sk")
    def delete_item(table_name, pk, sk):
        photo = Photo(pk=pk, sk=sk)
        db.delete_item(table_name, item=photo)
        click.echo(
            f"[cli-delete_item] deleted item pk:{photo.pk}, sk: {photo.sk} from table {table_name}"
        )

    # -------------------------------#
    #                S3              #
    # -------------------------------#

    # flask create-bucket
    @app.cli.command("create-bucket")
    @click.argument("bucket_name")
    def create_photos_bucket(bucket_name):
        s3.create_bucket(bucket_name)
        click.echo(f"[cli-create-photos-bucket] created {bucket_name} bucket")

    # flask add-bucket-policy
    @app.cli.command("add-bucket-policy")
    @click.argument("bucket_name")
    def add_bucket_policy(bucket_name):
        s3.add_bucket_policy(bucket_name)
        click.echo(f"[cli-empty-bucket] added policy to {bucket_name} bucket")

    # flask list-files "travels-photos-00"
    @app.cli.command("list-files")
    @click.argument("bucket_name")
    def list_files(bucket_name):
        files = s3.list_files(bucket_name)
        print(files)
        click.echo(f"[cli-list-files] files in {bucket_name} bucket")

    # flask empty-bucket
    @app.cli.command("empty-bucket")
    @click.argument("bucket_name")
    def empty_bucket(bucket_name):
        s3.empty_bucket(bucket_name)
        click.echo(f"[cli-empty-bucket] emptied {bucket_name} bucket")

    # flask delete-bucket
    @app.cli.command("delete-bucket")
    @click.argument("bucket_name")
    def delete_bucket(bucket_name):
        s3.delete_bucket(bucket_name)
        click.echo(f"[cli-delete-bucket] deleted {bucket_name} bucket")

    # flask delete-file
    @app.cli.command("delete-file")
    @click.argument("bucket_name")
    @click.argument("file_name")
    def delete_file(bucket_name, file_name):
        s3.delete_file(bucket_name, file_name)
        click.echo(
            f"[cli-delete-file] deleted file {file_name} from {bucket_name} bucket"
        )

    # -------------------------------#
    #               APP              #
    # -------------------------------#

    # flask upload-photos "images" "travels-photos-00" "travels"
    @app.cli.command("upload-photos")
    @click.argument("folder_path")
    @click.argument("bucket_name")
    @click.argument("table_name")
    def upload_photos(folder_path, bucket_name, table_name):
        import json
        from os import listdir
        from os.path import isfile, join

        try:
            file_names = [
                file
                for file in listdir(f"{folder_path}")
                if isfile(join(f"{folder_path}", file)) and not file.endswith(".json")
            ]
            with open(PHOTOS_DATA_PATH) as f:
                photos_data = json.load(f)

            for file_name in file_names:
                name = file_name.split(".")[0]
                # first try uploading to s3
                s3.upload_file(folder_path + "/" + file_name, bucket_name, name)

                # then store photo item in dynamodb
                sk = name
                title = photos_data[name]["title"]
                description = photos_data[name]["description"]
                url = s3.get_file_url(bucket_name, name)
                photo = Photo(
                    pk=PARTITION_KEY_VALUE,
                    sk=sk,
                    title=title,
                    description=description,
                    link=url,
                )
                db.put_item(table_name, photo)

                print(
                    f"[cli-upload-photos] successfully uploaded photo {PARTITION_KEY_VALUE}:{sk}"
                )

        except ClientError as e:
            print(e)
        else:
            click.echo(
                f"[cli-upload-photos] uploaded files to s3 {bucket_name} bucket and ddb {table_name} table\n"
            )

    # flask update-photo "photo" "beograd:4000" --action='INCREMENT_REACTION' --reaction='like'
    # flask update-photo "photo" "beograd:4000" --action='ADD_COMMENT' --comment='ddddd from cli'
    # flask update-photo "photo" "beograd:4000" --action='DELETE_COMMENT' --position=0
    @app.cli.command("update-photo")
    @click.argument("pk")
    @click.argument("sk")
    @click.option(
        "--action",
        type=click.Choice(
            [Action.ADD_COMMENT, Action.DELETE_COMMENT, Action.INCREMENT_REACTION]
        ),
        required=True,
    )
    @click.option("--reaction")
    @click.option("--comment")
    @click.option("--position")
    def update_photo(pk, sk, action, reaction, comment, position):
        data = UpdatePhotoRequest(
            key={"pk": pk, "sk": sk},
            action=Action(action),
            reaction=reaction,
            comment=comment,
            position=position,
        )
        req = db.build_update_item_request(data)
        db.update_item(TRAVELS, req)
        click.echo(f"[cli-update-photo] updated photo {req} \n")

    # flask delete-photo "photo" "beograd:3000"
    @app.cli.command("delete-photo")
    @click.argument("pk")
    @click.argument("sk")
    def delete_photo(pk, sk):
        try:
            # item = db.get_item(TRAVELS, pk, sk)
            photo = Photo(pk=pk, sk=sk)
            # delete from ddb
            db.delete_item(TRAVELS, item=photo)
            # delete from bucket
            s3.delete_file(PHOTOS, f"{sk}")

        except ClientError as e:
            print(e)
        else:
            click.echo(f"[cli-upload-photos] deleted photo {pk}:{sk} \n")

    # flask delete-photos "photo" "beograd:1"
    @app.cli.command("delete-photos")
    @click.argument("pk_pattern")
    @click.argument("sk_pattern")
    def delete_photos(pk_pattern, sk_pattern):
        try:
            table = db.get_table(TRAVELS)
            photos = table.query(
                ProjectionExpression="pk, sk",
                KeyConditionExpression=Key(PARTITION_KEY).eq(pk_pattern)
                & Key(SORT_KEY).begins_with(sk_pattern),
            )["Items"]
            for photo in photos:
                db.delete_item(TRAVELS, item=Photo(pk=photo["pk"], sk=photo["sk"]))
                s3.delete_file(PHOTOS, photo["sk"])
        except ClientError as e:
            print(e)
        else:
            click.echo(f"[cli-delete-photos] deleted photos \n")

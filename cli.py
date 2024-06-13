import click
from flask import Flask

from constants import PARTITION_KEY_NAME, TRAVELS
from models import Action, Photo, UpdatePhotoRequest


def register_cli(app: Flask, db, s3):
    # DYNAMODB

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

    # flask add-photo "photos" "beograd:9000" --title "la rosa" --description "this is a flower"
    @app.cli.command("add-photo")
    @click.argument("pk")
    @click.argument("sk")
    @click.option("--title")
    @click.option("--description")
    def add_photo(pk, sk, title, description):
        photo = Photo(pk=pk, sk=sk, title=title, description=description)
        db.put_item(TRAVELS, item=photo)
        click.echo(f"[cli-add-photo] created new photo pk:{photo.pk}, sk: {photo.sk}")

    # flask delete-photo "photos" "beograd:9000"
    @app.cli.command("delete-photo")
    @click.argument("pk")
    @click.argument("sk")
    def delete_photo(pk, sk):
        photo = Photo(pk=pk, sk=sk)
        db.delete_item(TRAVELS, item=photo)
        click.echo(f"[cli-delete_photo] deleted photo pk:{photo.pk}, sk: {photo.sk}")

    # flask update-photo "photos" "beograd:8000" --action='INCREMENT_REACTION' --reaction='like'
    # flask update-photo "photos" "beograd:9000" --action='ADD_COMMENT' --comment='ddddd from cli'
    # flask update-photo "photos" "beograd:9000" --action='DELETE_COMMENT' --position=0
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

    # S3
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

    # flask upload-file "images/blow.jpg" "travels-photos-00" "beograd:1000:blow.jpg"
    @app.cli.command("upload-file")
    @click.argument("file_name")
    @click.argument("bucket_name")
    @click.argument("object_name")
    def upload_file(file_name, bucket_name, object_name):
        s3.upload_file(file_name, bucket_name, object_name)
        click.echo(f"[cli-upload-file] upladed file to {bucket_name} bucket")

    # flask upload-files "images" "travels-photos-00"
    @app.cli.command("upload-files")
    @click.argument("folder_name")
    @click.argument("bucket_name")
    def upload_files(folder_name, bucket_name):
        s3.upload_files(folder_name, bucket_name)
        click.echo(f"[cli-upload-files] upladed files to {bucket_name} bucket")

    # flask list-files "travels-photos-00"
    @app.cli.command("list-files")
    @click.argument("bucket_name")
    def list_files(bucket_name):
        files = s3.list_files(bucket_name)
        print(files)
        click.echo(f"[cli-list-files] files in {bucket_name} bucket")

    # PHOTOS
    # flask upload-photos "images" "travels-photos-00" "travels"
    @app.cli.command("upload-photos")
    @click.argument("folder_path")
    @click.argument("bucket_name")
    @click.argument("table_name")
    def upload_photos(folder_path, bucket_name, table_name):
        import json
        from os import listdir
        from os.path import isfile, join

        from botocore.exceptions import ClientError

        try:
            file_names = [
                file
                for file in listdir(f"{folder_path}")
                if isfile(join(f"{folder_path}", file)) and not file.endswith(".json")
            ]
            with open("images/descriptions.json") as j:
                descriptions = json.load(j)

            for file_name in file_names:
                # first try uploading to s3
                s3.upload_file(folder_path + "/" + file_name, bucket_name, file_name)

                # then store photo item in dynamodb
                name = file_name.split(".")[0]
                sk = name.split(":")[0] + ":" + name.split(":")[1]
                title = name.split(":")[2]
                description = descriptions[name]
                url = s3.get_file_url(bucket_name, file_name)
                photo = Photo(
                    pk=PARTITION_KEY_NAME,
                    sk=sk,
                    title=title,
                    description=description,
                    link=url,
                )
                db.put_item(table_name, photo)

                print(
                    f"[cli-upload-photos] successfully uploaded photo {PARTITION_KEY_NAME}:{sk}"
                )

        except ClientError as e:
            print(e)
        else:
            click.echo(
                f"[cli-upload-photos] uploaded files to s3 {bucket_name} bucket and ddb {table_name} table\n"
            )

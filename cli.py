import click
from flask import Flask

from constants import TRAVELS
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

    # flask delete-bucket
    @app.cli.command("delete-bucket")
    @click.argument("bucket_name")
    def delete_bucket(bucket_name):
        s3.delete_bucket(bucket_name)
        click.echo(f"[cli-delete-bucket] deleted {bucket_name} bucket")

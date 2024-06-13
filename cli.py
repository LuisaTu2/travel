from flask import Flask
import click
from constants import TRAVELS
from models import Action, Photo, UpdatePhotoRequest


def register_cli(app: Flask, db):
    # flask create-travels-table
    @app.cli.command("create-travels-table")
    def create_travels_table():
        db.create_travels_table()
        click.echo(f"[cli-add-travels-table] created travels table")

    # flask delete-travels-table
    @app.cli.command("delete-travels-table")
    def delete_travels_table():
        db.delete_table(TRAVELS)
        click.echo(f"[cli-delete-travels-table] deleted travels table")

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

from pathlib import Path
from typing import Optional
import typer
import toml
from relycomply_client.cli import RelyComplyCLI
from relycomply_client.exceptions import (
    RelyComplyCliException,
    RelyComplyClientException,
)

from relycomply_client.relycomply_gql_client import RelyComplyGQLClient
from tabulate import tabulate


class RelySync:
    def __init__(self, location, recursive, interactive, cli: RelyComplyCLI = None):
        self.location = location or Path(".")
        self.recursive = recursive
        self.interactive = interactive

        self.cli: RelyComplyCLI = cli or RelyComplyCLI()
        self.gql: RelyComplyGQLClient = self.cli.gql
        self.sync_order: list[str] = self.gql.templates["TypeRelationships"][
            "SyncOrder"
        ]
        self.implementations: list[str] = self.gql.templates["TypeRelationships"][
            "Implementations"
        ]

    def run_cli(self):
        self.locate_files()
        self.display_locations()

        if not self.with_metadata:
            return

        self.schedule_actions()

        self.display_schedule()

        if self.interactive and not typer.prompt(
            "Are you sure you would like to continue (yes/no)?", type=bool
        ):
            return

        self.execute_schedule()

    def locate_files(self):

        # These are the supported types

        glob_pattern = "**/*.toml" if self.recursive else "*.toml"

        toml_files = list(self.location.glob(glob_pattern))

        self.no_metadata = set()
        self.incorrect_metadata = []
        self.with_metadata = []
        for path in toml_files:
            with open(path) as f:
                lines = f.readlines()

                # Clear empty lines
                lines = [line.strip() for line in lines if line.strip()]

                # Strip preceeding normal comments
                lines = [
                    line
                    for line in lines
                    if not (line[0] == "#" and not line.startswith("#%"))
                ]

                # Has no fore-matter
                if not lines or not lines[0].startswith("#%"):
                    self.no_metadata.add(path)

                fore_lines = []
                for line in lines:
                    if line.startswith("#%"):
                        fore_lines.append(line[2:].strip())
                    else:
                        break

                metadata_str = "\n".join(fore_lines)

                try:
                    metadata = toml.loads(metadata_str)
                    if not metadata:
                        self.no_metadata.add(path)
                    elif "type" not in metadata:
                        self.incorrect_metadata.append((path, "No type information"))
                    elif "type" in metadata and metadata["type"] not in self.sync_order:
                        self.incorrect_metadata.append(
                            (
                                path,
                                f"Type '{metadata['type']}' is not support for syncing",
                            )
                        )
                    else:
                        self.with_metadata.append((path, metadata))

                except Exception as e:
                    self.incorrect_metadata.append(
                        (path, f"Metadata TOML error: {str(e)}")
                    )

    def display_locations(self):
        if self.no_metadata:
            typer.secho("Found the following files with no metadata")
            for path in self.no_metadata:
                typer.secho("  - " + str(path))
            typer.echo()

        if self.incorrect_metadata:
            typer.secho(
                "Found the following files with incorrect metadata", fg=typer.colors.RED
            )
            for path, error in self.incorrect_metadata:
                typer.secho(f"  - {path} [{error}]", fg=typer.colors.RED)
            typer.echo()

        if self.with_metadata:
            typer.secho(
                "Found the following files with type information", fg=typer.colors.GREEN
            )
            for path, metadata in sorted(self.with_metadata):
                typer.secho(
                    f"  - {path} [type = {metadata['type']}]", fg=typer.colors.GREEN
                )
            typer.echo()

    def get_rank(self, path, metadata):
        return self.sync_order.index(metadata["type"]), path

    def schedule_actions(self):
        self.with_metadata.sort(key=lambda t: self.get_rank(*t))

        implements_map = {
            implementor: implemented
            for implemented, implementors in self.implementations.items()
            for implementor in implementors
        }

        for path, metadata in self.with_metadata:
            metadata["implements"] = implements_map.get(
                metadata["type"], metadata["type"]
            )

        self.schedule = [
            dict(path=path, metadata=metadata, variables=toml.load(path))
            for path, metadata in self.with_metadata
        ]

        for item in self.schedule:
            try:
                existing = self.cli.execute(
                    item["metadata"]["implements"],
                    "retrieve",
                    dict(name=item["variables"]["name"]),
                )
                item["action"] = "update"
                item["existing"] = existing

            except RelyComplyCliException:
                item["action"] = "create"
                item["existing"] = None

    def display_schedule(self):
        to_create = [item for item in self.schedule if item["action"] == "create"]
        to_update = [item for item in self.schedule if item["action"] == "update"]

        def display_schedule_table(items, message):
            if items:
                typer.secho(message)
                typer.echo()
                typer.echo(
                    tabulate(
                        [
                            [
                                item["metadata"]["type"],
                                item["variables"]["name"],
                                item["path"],
                            ]
                            for item in items
                        ],
                        headers=["Type", "name", "path"],
                    )
                )
                typer.echo()

        display_schedule_table(to_create, "The following items will be created:")
        display_schedule_table(to_update, "The following items may be updated:")

    def execute_schedule(self):

        for item in self.schedule:
            try:
                if item["action"] == "create":
                    typer.echo(
                        f'rely {item["metadata"]["type"]} {item["action"]} {item["path"]}'
                    )
                    self.cli.execute(
                        item["metadata"]["type"], item["action"], item["variables"]
                    )
                elif item["action"] == "update":
                    typer.echo(
                        f'rely {item["metadata"]["type"]} {item["action"]} --id={item["variables"]["name"]} {item["path"]}'
                    )

                    self.cli.execute(
                        item["metadata"]["type"],
                        item["action"],
                        {"id": item["variables"]["name"], **item["variables"]},
                    )
            except RelyComplyClientException as e:
                typer.secho(str(e), fg=typer.colors.RED)
                break


def sync(
    location: Optional[Path] = typer.Argument(None),
    recursive: bool = typer.Option(False),
    interactive: bool = typer.Option(True),
):
    rely_sync = RelySync(location, recursive, interactive)
    rely_sync.run_cli()


def main():
    typer.run(sync)


if __name__ == "__main__":
    main()

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


def get_import_command(osmfile: str) -> Tuple[List[str], Dict]:
    """
    Returns a command string and env vars for `osm2pgsql`
    """

    # This based on `connection.client.settings_to_cmd_args_env`
    # but slightly different parameters for OSM2PGSQL
    settings_dict = settings.DATABASES["default"]
    args = ["osm2pgsql", "--output=flex", "--style=./run.lua"]

    host = settings_dict.get("HOST")
    port = settings_dict.get("PORT")
    dbname = settings_dict.get("NAME")
    user = settings_dict.get("USER")
    passwd = settings_dict.get("PASSWORD")

    if user:
        args += ["-U", user]
    if host:
        args += ["-H", host]
    if port:
        args += ["-P", str(port)]
    if dbname:
        args += ["-d", dbname]
    else:
        args += ["-d", "postgres"]

    env = {}
    if passwd:
        env["PGPASSWORD"] = str(passwd)

    args.append(osmfile)
    env["SKIP_META"] = "true"  # Otherwise lua tries to connect using `PGOSM_CONN` string instead of the settings here
    return args, env


class Command(BaseCommand):
    help = "Import data to the staging, 'osm' schema. Note that this requires a writable osm schema to be present."

    def add_arguments(self, parser):
        parser.add_argument("osmfile", type=str, help="Path to the OSM protobuf file to import")

    def handle(self, *args, **options):
        working_dir = Path(__file__).parent.parent / "flex-config"
        os.chdir(working_dir)
        args, env = get_import_command(options["osmfile"])
        # The list version of subprocess.run does not work with osm2pgsql
        # hence the join
        self.stdout.write(self.style.SUCCESS("Creating the `osm` schema"))
        with connection.cursor() as c:
            try:
                c.execute("CREATE SCHEMA IF NOT EXISTS osm;")
            except Exception as E:  # noqa: F841
                # TODO: Explain to user what to do
                # This may occur when a user does not have permission
                # Run as a user with permission to create a schema
                # with "GRANT CREATE ON database {database} TO {user};"
                raise

        self.stdout.write(self.style.SUCCESS(f"Running Import of {options['osmfile']}"))
        self.stdout.write(self.style.SUCCESS("This may take a few minutes..."))
        run = subprocess.run((" ").join(args), env={**env}, shell=True, capture_output=True)
        try:
            run.check_returncode()
        except subprocess.CalledProcessError:
            self.stdout.write(self.style.ERROR(f"Running Import of {options['osmfile']} failed"))
            self.stdout.write(self.style.ERROR(run.stderr.decode()))
        else:
            self.stdout.write(self.style.SUCCESS(f"Running Import of {options['osmfile']} complete"))
            self.stdout.write(
                self.style.SUCCESS("To insert/update the Django tables, please run `import_from_pgosmflex`")
            )
            self.stdout.write(self.style.SUCCESS("You can drop the osm schema after that command"))

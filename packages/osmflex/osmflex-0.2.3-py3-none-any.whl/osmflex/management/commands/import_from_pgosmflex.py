from typing import Generator, Iterable, Set

from django.core.management.base import BaseCommand
from django.db import connection, models, transaction

from osmflex.models import Osm, Tags, Unitable
from osmflex.utils import truncate_sql, upsert_sql


class Command(BaseCommand):
    help = "Import roads from an OSM pbf file"

    def add_arguments(self, parser):
        parser.add_argument("--truncate", action="store_true", help="Truncate current table data")
        parser.add_argument("--unitable", action="store_true", help="Include the 'unitable' table")

    def handle(self, *args, **options):
        def update_all_from_flex(truncate: bool = False, unitable: bool = False) -> Generator[str, None, None]:
            """
            Generate import SQL for all tables. This executes an "upsert" from the parallel tables in
            the "osm" schema.
            """

            def get_all_subclasses(cls) -> Iterable[models.Model]:
                subs = set()  # type: Set[models.Model]
                for sc in cls.__subclasses__():
                    if not sc._meta.abstract:
                        subs.add(sc)
                    subs.update(get_all_subclasses(sc))
                return subs

            for sc in get_all_subclasses(Osm):
                if truncate:
                    self.stdout.write(self.style.WARNING(f"Truncating {sc._meta.db_table}"))
                    yield truncate_sql(sc)
                self.stdout.write(self.style.SUCCESS(f"Importing data to {sc._meta.db_table}"))
                yield upsert_sql(sc)

            # Also do the "tags" table
            if truncate:
                yield truncate_sql(Tags)  # type: ignore
            yield upsert_sql(Tags)  # type: ignore

            # And the "unitable", if specified
            if unitable:
                if truncate:
                    yield truncate_sql(Unitable)  # type: ignore
                yield upsert_sql(Unitable, exclude_fields=["id"])  # type: ignore

        with transaction.atomic():
            with connection.cursor() as c:
                for query in update_all_from_flex(truncate=options["truncate"], unitable=options["unitable"]):
                    try:
                        c.execute(query)
                    except Exception as E:
                        self.stdout.write(self.style.ERROR("There was a problem running SQL"))
                        self.stdout.write(self.style.ERROR(f"{E}"))
                        self.stdout.write(self.style.ERROR(query.as_string(c.cursor)))
                    else:
                        if options["verbosity"] > 0:
                            self.stdout.write(self.style.SUCCESS(query.as_string(c.cursor)))

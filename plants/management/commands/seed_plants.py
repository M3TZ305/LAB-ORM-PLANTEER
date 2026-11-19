import json
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from plants.models import Plant


class Command(BaseCommand):
    help = "Add the bundled plants and restore missing bundled photos."

    def handle(self, *args, **options):
        folder = Path(__file__).resolve().parents[2] / "seed_data"
        entries = json.loads((folder / "plants.json").read_text(encoding="utf-8"))
        storage = Plant._meta.get_field("image").storage
        missing = [entry["slug"] for entry in entries
                   if not (folder / f'{entry["slug"]}.webp').is_file()]
        if missing:
            raise CommandError("Missing bundled photographs: " + ", ".join(missing))

        created = 0
        with transaction.atomic():
            for entry in entries:
                filename = f'{entry["slug"]}.webp'
                media_name = f"plants/seed/{filename}"
                plant = Plant.objects.filter(name=entry["name"]).first()
                if plant and plant.image.name != media_name:
                    continue
                if not storage.exists(media_name):
                    with (folder / filename).open("rb") as source:
                        media_name = storage.save(media_name, File(source))
                if plant is None:
                    fields = {key: value for key, value in entry.items() if key != "slug"}
                    Plant.objects.create(image=media_name, **fields)
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Added {created} plants."))

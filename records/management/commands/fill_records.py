import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from records.models import RecordEntry, RecordImage


class Command(BaseCommand):
    help = 'Fill RecordEntry objects with data from prompts/init-data/data.json'

    def handle(self, *args, **options):
        # Path to the data file
        data_file_path = os.path.join('prompts', 'init-data', 'data.json')
        
        try:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {data_file_path}')
            )
            return
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON in file: {data_file_path}')
            )
            return

        created_count = 0
        skipped_count = 0

        for record_data in data:
            title = record_data.get('title')
            
            # Check if record with this title already exists
            if RecordEntry.objects.filter(title=title).exists():
                self.stdout.write(
                    self.style.WARNING(f'Record with title "{title}" already exists. Skipping.')
                )
                skipped_count += 1
                continue

            # Create new record
            record = RecordEntry(
                title=title,
                description=record_data.get('description', ''),
                is_approved=True  # Auto-approve initial data
            )

            # Handle preview image
            preview_image_path = record_data.get('image_previe')
            if preview_image_path and os.path.exists(preview_image_path):
                with open(preview_image_path, 'rb') as img_file:
                    record.preview_image.save(
                        os.path.basename(preview_image_path),
                        File(img_file),
                        save=False
                    )

            # Save record first to get ID
            record.save()

            # Handle additional images
            images_paths = record_data.get('images', [])
            for image_path in images_paths:
                if os.path.exists(image_path):
                    # Create RecordImage object
                    record_image = RecordImage()
                    with open(image_path, 'rb') as img_file:
                        record_image.image.save(
                            os.path.basename(image_path),
                            File(img_file),
                            save=True
                        )
                    # Add to record's many-to-many relationship
                    record.images.add(record_image)

            self.stdout.write(
                self.style.SUCCESS(f'Created record: "{title}"')
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Completed! Created {created_count} records, skipped {skipped_count} existing records.'
            )
        )
import csv
from django.core.management.base import BaseCommand
from criminal_rec.models import CriminalRec
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Import criminal records from CSV files, handling multiple marks and photo"

    def handle(self, *args, **kwargs):
        # Step 1: Load marks data into a dict of lists for fast lookup
        marks_data = {}
        marks_file_path = os.path.join(settings.BASE_DIR, 'criminal_rec', 'data', 'marks.csv')
        if not os.path.exists(marks_file_path):
            self.stdout.write(self.style.ERROR(f"Error: {marks_file_path} not found."))
            return

        with open(marks_file_path, newline='', encoding='utf-8') as marks_file:
            reader = csv.DictReader(marks_file, delimiter=';')
            for row in reader:
                criminal_id = row['id']
                scars_or_mark = row.get('mark', '').strip()
                if criminal_id in marks_data:
                    if scars_or_mark:
                        marks_data[criminal_id].append(scars_or_mark)
                else:
                    marks_data[criminal_id] = [scars_or_mark] if scars_or_mark else []

        # Step 2: Read main criminal info
        person_file_path = os.path.join(settings.BASE_DIR, 'criminal_rec', 'data', 'person.csv')
        if not os.path.exists(person_file_path):
            self.stdout.write(self.style.ERROR(f"Error: {person_file_path} not found."))
            return

        with open(person_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            processed_count = 0
            for row in reader:
                if processed_count >= 20:
                    break

                criminal_id = row['id']
                scars_or_marks_list = marks_data.get(criminal_id, [])
                scars_or_marks_combined = ", ".join(scars_or_marks_list)

                # Build description from selected fields
                description_parts = []
                for field in ['race', 'eyes', 'weight', 'hair', 'height']:
                    value = row.get(field, '').strip()
                    if value:
                        description_parts.append(f"{field.capitalize()}: {value}")
                description_combined = "; ".join(description_parts)

                # Person.csv has a column named 'photo_path'
                photo_path = row.get('photo_path', '').strip()
                criminal_photo = None
                if photo_path:
                    full_photo_path = os.path.join(settings.BASE_DIR, 'criminal_rec', 'data', photo_path)
                    if os.path.exists(full_photo_path):
                        criminal_photo = os.path.relpath(full_photo_path, settings.MEDIA_ROOT)
                    else:
                        self.stdout.write(self.style.WARNING(f"Warning: Photo file not found at {full_photo_path} for criminal {criminal_id}."))

                CriminalRec.objects.update_or_create(
                    criminal_id=criminal_id,
                    defaults={
                        'criminal_name': row.get('name', '').strip(),
                        'description': description_combined,
                        'crime': '',  
                        'parent_institution': row.get('parent_institution', '').strip(),
                        'parole_status': row.get('offender_status','').strip(),
                        #'parole_end_date': row.get('parole_date', '').strip() or None, 
                        'scars_or_marks': scars_or_marks_combined,
                        'authorized': True,
                        'criminal_photo': criminal_photo, # Assign the photo path
                    }
                )
                processed_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {processed_count} criminal records.'))
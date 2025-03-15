# import os
# import csv
# from django.core.management.base import BaseCommand
# from course_registration.models import Course

# class Command(BaseCommand):
#     help = 'Load course data from CSV file into the Course model'

#     def handle(self, *args, **kwargs):
#         base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#         csv_path = os.path.join(base_dir,'data', 'courses.csv')

#         try:
#             with open(csv_path, 'r') as file:
#                 reader = csv.DictReader(file)
#                 for row in reader:
#                     branch_name = row['branch_name'].replace("CSE & IT", "CSE/IT")
#                     if not Course.objects.filter(
#                         semester=row['semester'],
#                         course_code=row['course_code'],
#                         branch_name=branch_name
#                     ).exists():
#                         Course.objects.create(
#                             semester=row['semester'],
#                             course_code=row['course_code'],
#                             name=row['name'],
#                             credits=row['credits'],
#                             branch_name=branch_name
#                         )
#                         self.stdout.write(
#                             self.style.SUCCESS(
#                                 f"Added {row['course_code']} - {row['name']} for {branch_name}"
#                             )
#                         )
#                     else:
#                         self.stdout.write(
#                             self.style.WARNING(
#                                 f"Skipped duplicate: {row['course_code']} for {branch_name}"
#                             )
#                         )
#             self.stdout.write(self.style.SUCCESS('Successfully loaded all course data'))
#         except FileNotFoundError:
#             self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Error loading data: {str(e)}"))


import os
import csv
from django.core.management.base import BaseCommand
from course_registration.models import Course

class Command(BaseCommand):
    help = 'Load course data from CSV file into the Course model'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(base_dir, 'data', 'courses.csv')

        # Valid branch choices
        valid_branches = [choice[0] for choice in Course.BRANCH_CHOICES]  # ["CSE", "IT", "CSE/IT"]

        try:
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                # Verify CSV headers
                expected_headers = {'semester', 'course_code', 'name', 'credits', 'branch_name'}
                if not expected_headers.issubset(reader.fieldnames):
                    self.stdout.write(self.style.ERROR(f"CSV missing required headers. Found: {reader.fieldnames}"))
                    return

                for row in reader:
                    # Map "CSE & IT" to "CSE/IT"
                    branch_name = row['branch_name'].replace("CSE & IT", "CSE/IT")
                    course_code = row['course_code']

                    # Validate branch_name
                    if branch_name not in valid_branches:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Invalid branch_name '{branch_name}' for course {course_code}. Skipping."
                            )
                        )
                        continue

                    # Check course_code length (max_length=10)
                    if len(course_code) > 10:
                        self.stdout.write(
                            self.style.ERROR(
                                f"course_code '{course_code}' exceeds max_length=10. Skipping."
                            )
                        )
                        continue

                    # Check for duplicates
                    if not Course.objects.filter(
                        semester=row['semester'],
                        course_code=course_code,
                        branch_name=branch_name
                    ).exists():
                        Course.objects.create(
                            semester=row['semester'],
                            course_code=course_code,
                            name=row['name'],
                            credits=row['credits'],
                            branch_name=branch_name
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Added {course_code} - {row['name']} for {branch_name}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Skipped duplicate: {course_code} for {branch_name}"
                            )
                        )
            self.stdout.write(self.style.SUCCESS('Successfully loaded all course data'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {str(e)}"))
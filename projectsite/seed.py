import os
import django
from faker import Faker
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from tasks.models import Priority, Category, Task, Note, SubTask

fake = Faker()

def seed_data():
    print("Starting seeding...")

    priorities = ["High", "Medium", "Low", "Critical", "Optional"]
    categories = ["Work", "School", "Personal", "Finance", "Projects"]
    
    p_objs = [Priority.objects.get_or_create(name=p)[0] for p in priorities]
    c_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

    for _ in range(10):
        dt = timezone.make_aware(fake.date_time_this_month()) 
        
        task = Task.objects.create(
            title=fake.sentence(nb_words=5), 
            description=fake.paragraph(nb_sentences=3), 
            deadline=dt,
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"]), 
            priority=fake.random_element(p_objs),
            category=fake.random_element(c_objs)
        )
        
        Note.objects.create(task=task, content=fake.paragraph())
        SubTask.objects.create(parent_task=task, title=fake.sentence(), status="Pending")
    
    print("Seeding completed successfully!")
    
if __name__ == "__main__":
    seed_data()
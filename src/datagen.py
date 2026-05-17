from core.database import SessionLocal
from sqlalchemy.orm import Session
from account.models import UserModel
from tasks.models import TaskModel
from faker import Faker


fake = Faker()

def seed_users(db):
    user = UserModel(username=fake.user_name())
    user.password("1234")
    db.add_user(user)
    db.commit()
    db.refresh(user)
    return user

def seed_tasks(db, user, count=10):
    task_list = []
    for _ in range(10):
        task_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=count),
                description=fake.sentence(nb_words=count),
                is_completed=fake.boolean()
            )
        )
    db.add_all(task_list)
    db.commit()


def main():
    db = SessionLocal()
    try:
        user = seed_users(db)
        seed_tasks(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()
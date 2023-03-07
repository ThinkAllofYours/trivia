from flaskr import create_app
from models import Question, Category


def setUp():
    """Define test variables and initialize app."""
    database_name = "trivia_test"
    database_path = "postgresql://{}/{}".format("localhost:5432", database_name)
    app = create_app(test_config=database_path)
    client = app.test_client()
    with app.app_context():
        # delete test categories
        items = Category.query.filter(Category.type.ilike("%Test%")).all()
        for item in items:
            item.delete()

    with app.app_context():
        # print categories
        items = Category.query.all()
        for item in items:
            print(f"Category: {item.id} {item.type}")


setUp()

from django.db import connection
from appuser.models import Appuser
from devices.models import Hub


def initDB():
    pass
    """
    # Delete all the data from the database
    Appuser.objects.all().delete()
    Hub.objects.all().delete()

    # Reset the autoincrement counter for IDs
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sqlite_sequence")
    cursor.execute("VACUUM")

    print(">> Database initialized")
    """

def populateDB():
    pass
    """
    # Create new users [ username, password ]
    users = [
    #   Username,   Password
        ("mario",   "flora1"),
        ("luigi",   "flora1"),
        ("peach",   "flora1"),
        ("toad",    "flora1"),
        ("yoshi",   "flora1"),
    ]

    for user in users:
        Appuser.objects.create_user(user[0], password=user[1])

    print(">> Appuser populated")

    # Create new hubs [ owner, name, location ]
    hubs = [
        (1, "City House", "21 Main St, Springfield, IL"),
        (1, "Country House", "312 Standsted St, Boston, MA"),
        (1, "Small House", "1234 Main St, Springfield, IL"),
    ]

    for hub in hubs:
        owner = Appuser.objects.get(id=hub[0])
        Hub.objects.create(owner=owner, name=hub[0], location=hub[1])
    
    print(">> Hubs populated")
    """
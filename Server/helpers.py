import random
import string
import time
from random_address import real_random_address


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


def get_sample_events(collection):
    data = []

    categories = ("Music", "Science", "Health", "Sport")
    statuses = ("Popular", "Recent", "Finished", "Soon")

    for i in range(25):
        dict = {
            "name": "Event " + str(i),
            "description": "Magna occaecat in qui est ipsum aute laboris consequat. Pariatur sit aute nisi incididunt velit cupidatat laborum deserunt voluptate. Dolore minim nulla sunt nostrud dolor adipisicing voluptate. Sint cillum mollit velit in culpa commodo quis ex deserunt nisi aute velit magna eu. Quis voluptate irure aute aliqua nostrud. Labore et cupidatat tempor enim cillum irure dolore eu quis.",
            "location": real_random_address(),
            "promoter": "Promoter " + str(i),
            "price": random.randint(10, 100),
            "category": random.choice(categories),
            "status": random.choice(statuses),
            "date": random_date("1/1/2022 1:30 PM", "1/1/2024 4:50 AM", random.random())
        }

        x = collection.insert_one(dict)

        print(x.inserted_id)


def get_sample_sales(sales, events):
    ids = list(events.find({}, {"_id": 1}))
    print(ids)
    for i in range(10):
        customerId = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        eventId = str(random.choice(ids)["_id"])
        data = {
            "eventId": eventId,
            "customerId": customerId
        }

        sales.insert_one(data)

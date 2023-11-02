from models.models import Salary
from datetime import timedelta
from mongoengine import connect

# Define a connection to MongoDB
connect(db='test', host='localhost', port=27017)

def get_data_per_month(dt_from, dt_upto):
    # Get aggregated data by month.
    result_dict = {}

    result = Salary.objects(dt__gte=dt_from, dt__lte=dt_upto).aggregate(
       [
            {
                "$group": {
                    "_id": {
                        "year": { "$year": "$dt" },
                        "month": { "$month": "$dt" },
                    },
                    "total_value": { "$sum": "$value" },
                    },
                    
                },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                }
            }
        ]
    )

    dataset = []
    labels = []
    for doc in list(result):
        label = f"{doc['_id']['year']}-{doc['_id']['month']:02d}-01T00:00:00"
        dataset.append(doc["total_value"])
        labels.append(label)
    result_dict["dataset"] = dataset
    result_dict["labels"] = labels

    return result_dict

def get_data_per_day(dt_from, dt_upto):
    # Get aggregated data by days.
    result_dict = {}

    # create labels for all days of the month
    all_days = [dt_from + timedelta(days=i) for i in range((dt_upto - dt_from).days + 1)]
    labels = [day.strftime("%Y-%m-%dT00:00:00") for day in all_days]

    result = Salary.objects(dt__gte=dt_from, dt__lte=dt_upto).aggregate(
       [
            {
                "$group": {
                    "_id": {
                        "year": { "$year": "$dt" },
                        "month": { "$month": "$dt" },
                        "day": { "$dayOfMonth": "$dt" },
                    },
                    "total_value": { "$sum": "$value" },
                    },
                    
                },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                    "_id.day": 1,
                }
            }
        ]
    )

    # adding existing data and empty values for days that are not in the database
    total_value_dict = {
        (doc["_id"]["year"], doc["_id"]["month"], doc["_id"]["day"]): 
                doc["total_value"] for doc in list(result)
    }
    dataset = [
        total_value_dict.get((date.year, date.month, date.day), 0) 
            for date in all_days
    ]
    result_dict["dataset"] = dataset
    result_dict["labels"] = labels
    
    return result_dict

def get_data_per_hour(dt_from, dt_upto):
    # Get aggregated data by hours.
    result_dict = {}

    all_hours = [
        dt_from + timedelta(hours=i) 
            for i in range((dt_upto - dt_from).days * 24 + 1)
    ]

    labels = [hour.strftime("%Y-%m-%dT%H:00:00") for hour in all_hours]

    result = Salary.objects(dt__gte=dt_from, dt__lte=dt_upto).aggregate(
       [
            {
                "$group": {
                    "_id": {
                        "year": { "$year": "$dt" },
                        "month": { "$month": "$dt" },
                        "day": { "$dayOfMonth": "$dt" },
                        "hour": { "$hour": "$dt" },
                    },
                    "total_value": { "$sum": "$value" },
                    },
                    
                },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                    "_id.day": 1,
                    "_id.hour": 1,
                }
            }
        ]
    )

    total_value_dict = {
        (doc["_id"]["year"], doc["_id"]["month"], doc["_id"]["day"], doc["_id"]["hour"]): 
            doc["total_value"] for doc in list(result)
    }
    dataset = [
        total_value_dict.get((date.year, date.month, date.day, date.hour), 0) 
            for date in all_hours
    ]
    result_dict["dataset"] = dataset
    result_dict["labels"] = labels
    
    return result_dict


def get_agregated_data(dt_from, dt_upto, group_type):
    """
        Get aggregated data depending on the type of grouping.

        Args:
        dt_from (datetime): start date.
        dt_upto (datetime): end date.
        group_type (str): grouping type ("month", "day" or "hour").

        Returns:
        dict: Dictionary with data and lables

    """

    if group_type == "month":
        data_agregate = get_data_per_month(dt_from, dt_upto)
    elif group_type == "day":
        data_agregate = get_data_per_day(dt_from, dt_upto)
    elif group_type == "hour":
        data_agregate = get_data_per_hour(dt_from, dt_upto)
    else:
        return "Неверный тип группировки"
    return data_agregate
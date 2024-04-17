from datetime import datetime, timedelta

from db.base import create_async_mongo_client
from db.db import MONGO_CONFIG
from db.models.enums import TimeInterval, TimeIntervalPatterns

from .strings import INVALID_MESSAGE

client = create_async_mongo_client()
db = client[MONGO_CONFIG.MONGO_DB]


async def aggregate_salaries(dt_from, dt_upto, group_type):
    pipeline = [
        {
            "$match": {
                "dt": {
                    "$gte": datetime.strptime(dt_from, TimeIntervalPatterns.FULL.value),
                    "$lte": datetime.strptime(dt_upto, TimeIntervalPatterns.FULL.value),
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "group_type": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {"$eq": [group_type, TimeInterval.HOUR.value]},
                                "then": {
                                    "$dateToString": {
                                        "format": TimeIntervalPatterns.HOUR.value,
                                        "date": "$dt",
                                    }
                                },
                            },
                            {
                                "case": {"$eq": [group_type, TimeInterval.DAY.value]},
                                "then": {
                                    "$dateToString": {
                                        "format": TimeIntervalPatterns.DAY.value,
                                        "date": "$dt",
                                    }
                                },
                            },
                            {
                                "case": {"$eq": [group_type, TimeInterval.MONTH.value]},
                                "then": {
                                    "$dateToString": {
                                        "format": TimeIntervalPatterns.MONTH.value,
                                        "date": "$dt",
                                    }
                                },
                            },
                        ],
                        "default": "Invalid group_type",
                    }
                },
                "value": 1,
            }
        },
        {"$group": {"_id": "$group_type", "total_value": {"$sum": "$value"}}},
        {"$project": {"_id": 0, "group_type": "$_id", "total_value": 1}},
    ]

    result = await db.sample_collection.aggregate(pipeline).to_list(None)

    return result


def sort_and_format(input_data, group_type, dt_from, dt_upto):

    sorted_data = sorted(input_data, key=lambda x: x["group_type"])

    dataset = [item["total_value"] for item in sorted_data]

    try:
        current_pattern = TimeIntervalPatterns[TimeInterval(group_type).name].value
    except:
        return INVALID_MESSAGE

    labels = [
        str(datetime.strptime(item["group_type"], current_pattern).isoformat())
        for item in sorted_data
    ]

    formatted_data = {"dataset": dataset, "labels": labels}
    s_date = datetime.strptime(dt_from, TimeIntervalPatterns.FULL.value)
    days = abs(
        (
            datetime.strptime(dt_from, TimeIntervalPatterns.FULL.value)
            - datetime.strptime(dt_upto, TimeIntervalPatterns.FULL.value)
        ).days
    )

    match group_type:
        case TimeInterval.HOUR.value:
            labels_ideal = [
                (s_date + timedelta(hours=idx)).strftime(
                    TimeIntervalPatterns.FULL.value
                )
                for idx in range(24)
            ]

            if days > 0:
                for day in range(1, days + 1):
                    labels_ideal.extend(
                        [
                            (
                                s_date + timedelta(hours=idx) + timedelta(days=day)
                            ).strftime(TimeIntervalPatterns.FULL.value)
                            for idx in range(24)
                        ]
                    )

            dataset_ideal = [0 for i in range(len(labels_ideal))]

            ideal_data = {"dataset": dataset_ideal, "labels": labels_ideal}

            for i, label in enumerate(formatted_data["labels"]):
                if label in labels_ideal:
                    index_ideal = labels_ideal.index(label)
                    ideal_data["dataset"][index_ideal] = formatted_data["dataset"][i]

        case TimeInterval.DAY.value:
            if days > 0:
                labels_ideal = [
                    (s_date + timedelta(days=idx)).strftime(
                        TimeIntervalPatterns.FULL.value
                    )
                    for idx in range(days)
                ]

            dataset_ideal = [0 for _ in range(len(labels_ideal))]

            ideal_data = {"dataset": dataset_ideal, "labels": labels_ideal}

            for i, label in enumerate(formatted_data["labels"]):
                if label in labels_ideal:
                    index_ideal = labels_ideal.index(label)
                    ideal_data["dataset"][index_ideal] = formatted_data["dataset"][i]
        case TimeInterval.MONTH.value:
            months_count = (
                abs(
                    (
                        s_date.year
                        - datetime.strptime(
                            dt_upto, TimeIntervalPatterns.FULL.value
                        ).year
                    )
                    * 12
                    + s_date.month
                    - datetime.strptime(dt_upto, TimeIntervalPatterns.FULL.value).month
                )
                + 1
            )

            labels_ideal = [
                s_date.replace(day=1, month=s_date.month + month).strftime(
                    TimeIntervalPatterns.FULL.value
                )
                for month in range(months_count)
            ]

            dataset_ideal = [0 for _ in range(len(labels_ideal))]

            ideal_data = {"dataset": dataset_ideal, "labels": labels_ideal}

            for i, label in enumerate(formatted_data["labels"]):
                if label in labels_ideal:
                    index_ideal = labels_ideal.index(label)
                    ideal_data["dataset"][index_ideal] = formatted_data["dataset"][i]

    return ideal_data


async def find_salaries(dt_from, dt_upto, group_type):
    if dt_from is None or dt_upto is None or group_type is None:
        return INVALID_MESSAGE

    result = await aggregate_salaries(dt_from, dt_upto, group_type)

    res_better = sort_and_format(result, group_type, dt_from, dt_upto)

    return res_better

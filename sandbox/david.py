data = {
    "2020-06-28": {
        "humidity": {
            "01": 12,
            "02": 23,
            "03": 21
        },
        "pressure": {
            "01": 1,
            "02": 2,
            "03": 3
        },
        "wind": {
            "01": 23532,
            "02": 4352,
            "03": 325
        },
        "temperature": {
            "01": 12,
            "02": 14,
            "03": 15
        }
    },

    "2020-05-12": {
        "humidity": {
            "01": 23,
            "02": 544,
            "03": 223
        },
        "pressure": {
            "01": 213,
            "02": 3,
            "03": 4
        },
        "wind": {
            "01": 324,
            "02": 35,
            "03": 4632
        },
        "temperature": {
            "01": 11,
            "02": 12,
            "03": 16
        }
    }

}


def find_max_temperature():
    return_data = {
        "max_temp": 0,
        "date": "",
        "hour": ""
    }
    for k, v in data.items():
        for hour, temp in v.get("temperature").items():
            if temp > return_data["max_temp"]:
                return_data["max_temp"] = temp
                return_data["date"] = k
                return_data["hour"] = hour

    return return_data



if __name__ == '__main__':
    print(find_max_temperature())

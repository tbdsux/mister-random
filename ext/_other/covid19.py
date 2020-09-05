import requests


class COVID19:
    api_url = "http://covid19ph-api.herokuapp.com/api/cases/all"

    @staticmethod
    def get_covid19():
        resp = requests.get(COVID19.api_url).json()["cases"]
        return (
            resp["confirmed"],
            resp["active"],
            resp["recovered"],
            resp["deaths"],
            resp["severe"],
            resp["fatality_rate"],
        )

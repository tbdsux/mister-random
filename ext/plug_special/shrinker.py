import requests

class Shrinker:
    website = 'https://grue.cf/api/generate'

    # shrink the url
    @staticmethod
    async def SHRINK_URL(url):
        if Shrinker.validate_Url(url):
            data = {}
            data['grue-link'] = url

            # request to the api
            resp = requests.post(Shrinker.website, data=data)

            if resp.status_code == 200:
                # convert to json
                data = resp.json()

                # check if the key exists or not
                if 'link' in data:
                    return data['link'] # return the link if it exists
                elif 'error' in data:
                    return data['error'] # return the error if exists
                else:
                    return 'There was a problem with your request.'
            else:
                return 'There was a problem with your request.'

        return 'Invalid URL!'

    # validate the url before parsing
    @staticmethod
    def validate_Url(url):
        # it will return true if requests.get is successful and false if not
        try:
            requests.get(url)
        except Exception:
            return False

        return True
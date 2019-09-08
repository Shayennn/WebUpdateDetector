import requests


def send(msg):
    line_url = 'https://notify-api.line.me/api/notify'
    line_token = ''
    line_headers = {'content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer '+line_token}
    return requests.post(
        line_url, headers=line_headers,
        data={'message': msg}
    )

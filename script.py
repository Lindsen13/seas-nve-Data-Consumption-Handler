import pymysql
import requests
from config import db as db_credentials
from config import user_id, auth, last_update_of_auth

def create_connection():
    return pymysql.connect(host=db_credentials.get("host"),
                           user=db_credentials.get("username"),
                           password=db_credentials.get("password"),
                           db=db_credentials.get("db"),
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def get_power_data(user_id, auth):
    url = f'https://prod.copi.obviux.dk/consumptionPage/{user_id}/daily'
    headers = {
        "accept": "application/json, text/plain, */*",
        "x-customer-ip":"194.251.71.73",
        "authorization": auth,
        "cache-control": "no-cache",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "origin": "https://selvbetjening.energi.seas-nve.dk",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"
        }
    return requests.get(url, headers=headers)

def create_query(output):
    query = 'REPLACE INTO powerConsumptionData (start, end, kwH) VALUES'
    if output.status_code == 200:
        for element in output.json().get('data')[0].get('consumptions'):
            data = {
                'start': element.get('start').replace('T',' ').replace('.000Z',''),
                'end': element.get('end').replace('T',' ').replace('.000Z',''),
                'KwH': element.get('kWh')
            }
            query += f' ("{data.get("start")}", "{data.get("end")}", {data.get("KwH")}),'
    return query[:-1]

def store_data(query):
    connection = create_connection()
    with connection.cursor() as cursor:
            cursor.execute(query)
    connection.commit()
    connection.close()

def process_all():
    print('Fetching data')
    output = get_power_data(user_id, auth)
    if output.status_code == 200:
        print('Data fetched. Creating query')
        query = create_query(output)
        print('Query Created. Storing in Database')
        store_data(query)
        print('Done storing in Database')
    else:
        print(f'Cant fetch data. Is the Auth token up to date? Seems like last update was at {last_update_of_auth}')

if __name__ == "__main__":
    process_all()
import requests as rq
import datetime as dt
import schedule
import time
import pandas as pd



def parse_mts_music(date_since, date_until):
    token = ''
    params = dict(application_id='61853',
                  date_since=str(date_since),
                  date_until=str(date_until),
                  fields='event_datetime,event_json',
                  event_name='Artists_Play')


    while True:
        r = rq.get('https://api.appmetrica.yandex.ru/logs/v1/export/events.csv',
                   headers={'Authorization': f'OAuth {token}'},
                   params=params)
        r.encoding = 'utf-8'
        data = r.text
        
        if len(data) > 100:
            break
        else:
            time.sleep(60)



    with open(f"data/raw_data.csv", "w", encoding="utf-8") as file:
        file.write(str(data))

    data = pd.read_csv('data/raw_data.csv')

    data['event_json'] = data['event_json'].str[18:-2]
    data['event_json'] = data['event_json'].str.lower()
    data['event_datetime'] = pd.to_datetime(data['event_datetime'])
    data['iso_week'] = data['event_datetime'].dt.isocalendar().week




    data_grouped = data.groupby(['iso_week','event_json'], as_index=False) \
        .count().sort_values(['iso_week', 'event_datetime'], ascending=[True, False]) \
        .rename(columns={"event_json": "artist",
                         "event_datetime": "plays"})

    data_grouped = data_grouped.query('plays > 100')
    data_grouped = data_grouped.reset_index().drop(columns=['index'])

    artists_plays_DF = pd.read_csv('data/artists_plays_DF.csv')
    artists_plays_DF = pd.concat([artists_plays_DF, data_grouped], ignore_index=True)

    artists_plays_DF.to_csv('data/artists_plays_DF.csv', index=False)
    




date_since = dt.datetime.today().date() - dt.timedelta(days=7)
date_until = dt.datetime.today().date() - dt.timedelta(days=1)

schedule.every().monday.at("04:00").do(parse_mts_music, date_since, date_until)
while True:
   schedule.run_pending()
   time.sleep(10)
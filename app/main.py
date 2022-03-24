import os
from io import BytesIO
import flask
import pandas
import matplotlib.pyplot as plt
from datetime import datetime


def get_data(request):
    datadir = f"{os.environ['DATA']}"
    haillist = []
    hailtemp = pandas.read_csv(datadir, infer_datetime_format=True, parse_dates=[0],
                           date_parser=lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S'))
    haillist.append(hailtemp)
    hailtemp["YEAR"] = pandas.to_datetime(hailtemp['event_begin_time']).dt.year
    haillist.append(hailtemp['YEAR'])
    hailtemp["BEGIN_DAY"] = pandas.to_datetime(hailtemp['event_begin_time']).dt.day
    haillist.append(hailtemp['BEGIN_DAY'])
    haildf = pandas.DataFrame().append(haillist)
    plt.figure(figsize=(20, 10))
    ax = (haildf["YEAR"].groupby(haildf["BEGIN_DAY"]).count()).plot(kind="bar", color="#805ac3", rot=0)
    ax.set_facecolor("#eeeeee")
    ax.set_xlabel('Day of Month')
    ax.set_ylabel('Frequency')
    ax.set_title('Hail in March')
    x = haildf["YEAR"].groupby(haildf["BEGIN_DAY"]).count()
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return flask.send_file(img, mimetype='image/png')

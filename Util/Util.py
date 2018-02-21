import datetime
import re

TODAY = datetime.datetime.today().strftime("%Y%m")
BEFOREDAY = datetime.datetime.today() - datetime.timedelta(days=1) # 시작일 선정
STARTDT = BEFOREDAY.strftime('%Y-%m-%d')
ENDDT = TODAY
now = datetime.datetime.now()



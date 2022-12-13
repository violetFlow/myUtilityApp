import pandas as pd
import datetime as dt
UPLOAD_FOLDER = '/app/upload/'
class icsReader:
  def get_total_time_working(filename, startDate, endDate):
    path = UPLOAD_FOLDER + filename
    print(path)
    # ファイル読み込み
    with open(path) as f:
      lines = f.readlines()
    events = []

    # フィールド定義
    flg = False
    dtstart = ""
    dtend = ""
    summary = ""

    # 1行ずつ読み込む
    for l in lines:
      l = l.strip()
      # スケジュール開始を確認
      if l.find("BEGIN:VEVENT") > -1:
        flg = True

      if flg:
        # 開始時間を取得
        if l.find('DTSTART') > -1:
          dtstart = pd.to_datetime(l.split(":")[-1])
          dtdate_str = dtstart.strftime('%Y/%m/%d')
          dtdate = dt.datetime.strptime(dtdate_str, '%Y/%m/%d')
        # 終了時間を取得
        if l.find('DTEND') > -1:
          dtend = pd.to_datetime(l.split(":")[-1])
        # スケジュール内容を取得
        if l.find('SUMMARY') > -1:
          summary =l.split(":")[-1]
        # スケジュール終了を確認
        if l.find('END:VEVENT') > -1:
          flg = False
          events.append([dtstart, dtend, dtend - dtstart, summary, dtdate])

    # データフレーム化
    df = pd.DataFrame(events, columns=["dtstart","dtend","hours", "summary", "dtdate"])
    df.index = df.dtstart

    # 集計用データフレームの作成
    df_sum = df[startDate:endDate]

    # 内容別の時間集計
    sumH = 0
    list = []
    strList = []
    for s in df_sum.summary.value_counts().index:
      t = df_sum[df_sum.summary == s].hours.sum()
      hours = t.delta / (10**9 * 60 * 60)
      strDic = {}
      strDic["name"] = s 
      strDic["hours"] = hours
      numberHours = float(hours)
      # 終時以外
      if numberHours < 24.0:
        strList.append(strDic)
        # 全体時間集計
        sumH += hours

    # 全体時間出力
    sumDic = {}
    sumDic["name"] = "合計時間"
    sumDic["hours"] = sumH
    strList.append(sumDic)
    
    # 日別集計
    dateList = []
    for d in df_sum.dtdate.value_counts().index:
      t = df_sum[df_sum.dtdate == d].hours.sum()
      hours = t.delta / (10**9 * 60 * 60)
      dateDic = {}
      dateDic["date"] = d
      dateDic["hours"] = hours
      if hours != 24.0:
        dateList.append(dateDic)

    list.append(strList)
    list.append(sorted(dateList, key=lambda x : x["date"]))
    return list

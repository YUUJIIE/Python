
import requests
import slackweb

# 気象庁の天気予報JSONデータを取得
url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/010000.json'
r = requests.get(url).json()

#東京はr[8]。他の地域を選択する場合は上記URLを参照
region = r[8]
#地域名を取得
area_name = region["name"]
#今日、明日の日付を取得
today_date = region["srf"]["timeSeries"][0]["timeDefines"][0][0:10]
tommorrow_date = region["srf"]["timeSeries"][0]["timeDefines"][1][0:10]
#今日、明日の天気予報を取得
today_weather = region["srf"]["timeSeries"][0]["areas"]["weathers"][0]
tommorow_weather = region["srf"]["timeSeries"][0]["areas"]["weathers"][1]

#Slackと連携するため、Incoming Webhooksを設定する
#https://myworkspace-hiu2746.slack.com/apps/new/A0F7XDUAZ--incoming-webhook-
#「Incoming Webhooks インテグレーションを追加する」をクリックし、出てきたURLをコピーする。
slack = slackweb.Slack(url="ここにWEB_HOOK_URLを入力")

#メッセージのレイアウトを整える
#attachmentについて詳しくは　https://api.slack.com/messaging/composing/layouts
attachments = []
attachment = {
  "color":"#008DD5",
  "fields":[
    {
      "title": today_date,
      "value": today_weather
    },
    {
      "title": tommorrow_date,
      "value": tommorow_weather
    }
  ]
}
attachments.append(attachment)

#Slackに通知する
slack.notify(text="今日、明日の天気予報",username=area_name+"の天気",attachments=attachments)

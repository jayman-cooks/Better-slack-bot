

import requests
import json
import os
import sys
from slack_bolt import App
import slack_bolt
import logging
import time
logging.basicConfig(level=logging.DEBUG)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
slack_tok = os.environ.get("SLACK_BOT_TOKEN")
slack_sign = os.environ.get("SLACK_SIGNING_SECRET")
plane_api = os.environ.get("PLANE_API_TOK")

Client = WebClient(token=slack_tok)
def send_msg(message="Hello from your app! :tada:"):
    try:
        response = Client.chat_postMessage(
            channel="C077KC9NAFN",
            text=message
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

# Initialize your app with your bot token and signing secret
app = App(
    token=slack_tok,
    signing_secret=slack_sign
)

# New functionality
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home tab_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

# Ready? Start your app!
#if __name__ == "__main__":
#    app.start(port=int(os.environ.get("PORT", 3000)))
def check_rate_limit(start_time, current_time, requests):
   if current_time - start_time > requests:
      return 0 
   else:
      return (abs(current_time - start_time - requests) + 0.1)
   
  #


url_base = "https://api.plane.so/api/v1/workspaces/852-robotics-testing/"
url = f"{url_base}projects/"
PLANE_API_TOK = plane_api
headers = {"x-api-key": PLANE_API_TOK}
#url = "https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/issues/"
response = requests.request("GET", url, headers=headers)
data = json.loads(response.text)
list_of_projects = []
project_ids = []
issues = []
issue_ids = []
issue_proj_ids = []
iss_activity_count = []
dif_activity_count = 0
new_update_count = 0
debugging = False
issues_count = 0
requests_pm = 0


for i in range(len(data['results'])):
    list_of_projects.append(data['results'][i]['name'])
    project_ids.append(data['results'][i]['id'])
    print(data['results'][i]['name'])
    #send_msg(str(data['results'][i]['name']))
    print(data['results'][i]['id'])
    #send_msg(str(data['results'][i]['id']))


if debugging:
    print(data['next_page_results'])
    print(data)
    print("\n -----HEADER----")
    print(response.text)

timer_start = time.time()
for i in range(len(list_of_projects)):
    url = f"{url_base}projects/{project_ids[i]}/issues/"
    print(f"url selectd is: {url}")
    #time.sleep(check_rate_limit(timer_start, time.time(), requests_pm))
    response = requests.request("GET", url, headers=headers)
    data2 = json.loads(response.text)
    requests_pm += 1
    cur_issues_num = data2['count']
    print(f"There are {cur_issues_num} issues in {list_of_projects[i]}")
    issues_count += int(cur_issues_num)
    for x in range(len(data2['results'])):
       issue_ids.append(data2['results'][x]['id'])
       issue_proj_ids.append(project_ids[i])
       #third request
       url = f"{url_base}projects/{project_ids[i]}/issues/{data2['results'][x]['id']}/activities/"
       response2 = requests.request("GET", url, headers=headers)
       requests_pm += 1
       data3 = json.loads(response2.text)
       iss_activity_count.append(len(data3['results']))
   
print(f"There are {issues_count} issues in total. {len(issue_ids)}")
send_msg(f"You have {issues_count} issues total in your project.")
print(iss_activity_count)
if requests_pm < 30:
    time.sleep(20)
    requests_pm = 0
else:
   time.sleep(40)
   requests_pm = 0

iss_activity_count2 = []
for i in range(len(list_of_projects)):
    url = f"{url_base}projects/{project_ids[i]}/issues/"
    print(f"url selectd is: {url}")
    response = requests.request("GET", url, headers=headers)
    data2 = json.loads(response.text)
    requests_pm += 1
    cur_issues_num = data2['count']
    print(f"There are {cur_issues_num} issues in {list_of_projects[i]}")
    issues_count += int(cur_issues_num)
    for x in range(len(data2['results'])):
       issue_ids.append(data2['results'][x]['id'])
       #third request
       url = f"{url_base}projects/{project_ids[i]}/issues/{data2['results'][x]['id']}/activities/"
       response2 = requests.request("GET", url, headers=headers)
       data3 = json.loads(response2.text)
       requests_pm += 1
       iss_activity_count2.append(len(data3['results']))
print(iss_activity_count)
print(iss_activity_count2)
time.sleep(5)
if iss_activity_count == iss_activity_count2:
   print("lists are identical")
   send_msg("No changes have been made since the first loop excecuted")
else:
   print("lists aren't identical or you messed up the code")

   for i in range(len(iss_activity_count)):
      if iss_activity_count2[i] != iss_activity_count[i]:
         dif_activity_count += 1
         new_update_count = iss_activity_count2[i] - iss_activity_count[i]
         url = f"{url_base}projects/{issue_proj_ids[i]}/issues/{issue_ids[i]}/activities/"
         response2 = requests.request("GET", url, headers=headers)
         requests_pm += 1
         data3 = json.loads(response2.text)
         for y in range(new_update_count):
            print(f"\n \n \n  {response2.text} \n \n")
            if data3['results'][-(y+1)]['field'] == 'state' and data3['results'][-(y+1)]['new_value'] == 'Done':
               send_msg(f"Issue with id {issue_ids[i]} was completed!")
   send_msg(f"{dif_activity_count} issues have been changed since the last loop excecuted")
   print(f"{dif_activity_count} issues have been changed since the last loop excecuted") 

#for i in range(len(data2['results'])):
#    issues.append(data2['results'][i]['name'])
#    issue_ids.append(data2['results'][i]['id'])
#    print(data2['results'][i]['name'])
#    print(data2['results'][i]['id'])
#selected_issue = int(input(f"Please make your selection from the following issues: {issues}"))



#text = response.text.split(",")[1:-1]
#for i in range(len(text)):
#    print(text[i])

#print(f"there are {text[3][8:]} projects. ")
#projects = text[6:]
#print(f"")

#{"stuff":"More stuff", "things":"additional things", "results":[{"id":"iofdhs", "number":"6"}]}


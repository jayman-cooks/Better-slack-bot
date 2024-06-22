

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
def make_request(inurl): # sends a request while making sure we are under the rate limit (60)
    if requests_remaining > 2:
        return requests.request("GET", inurl, headers=headers)
    elif time.time() > rl_reset:
        return requests.request("GET", inurl, headers=headers)
    else:
        print("rate limit reached. Waiting...")
        time.sleep(rl_reset - time.time() + 2)
        return requests.request("GET", inurl, headers=headers)
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



url_base = "https://api.plane.so/api/v1/workspaces/852-robotics-testing/"
url = f"{url_base}projects/"
PLANE_API_TOK = plane_api
headers = {"x-api-key": PLANE_API_TOK}
#url = "https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/issues/"
response = requests.request("GET", url, headers=headers)
data = json.loads(response.text)
requests_remaining = int(response.headers['x-ratelimit-remaining'])
print(requests_remaining)
rl_reset = int(response.headers['x-ratelimit-reset'])
list_of_projects = []
project_ids = []
issues = []
temp_issue_ids = []
issue_ids = []
issue_ids2 = []
temp_issue_stats = []
issue_stats = []
issue_stats2 = []

temp_issue_proj_ids = []
issue_proj_ids = []
issue_proj_ids2 = []
dif_activity_count = 0
new_update_count = 0
debugging = False
issues_count = 0
loop_count = 0


timer_start = time.time()
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

for w in range(2):
    loop_count += 1
    for i in range(len(list_of_projects)):
        url = f"{url_base}projects/{project_ids[i]}/issues/"
        print(f"url selectd is: {url}")
        response = make_request(url)
        data2 = json.loads(response.text)
        requests_remaining = int(response.headers['x-ratelimit-remaining'])
        rl_reset = int(response.headers['x-ratelimit-reset'])
        cur_issues_num = data2['count']
        print(f"There are {cur_issues_num} issues in {list_of_projects[i]}")
        if loop_count % 2 == 0:
            issues_count += int(cur_issues_num)
        for x in range(len(data2['results'])):
            temp_issue_ids.append(data2['results'][x]['id'])
            temp_issue_proj_ids.append(project_ids[i])
            if (data2['results'][x]['completed_at']) == None:
                temp_issue_stats.append(0)
            else:
                temp_issue_stats.append(1)
    if loop_count % 2 == 1:
       print("USING FIRST LIST")
       time.sleep(1)
       issue_ids = temp_issue_ids
       issue_stats = temp_issue_stats
       issue_proj_ids = temp_issue_proj_ids
    else:
       print("USING SECOND LIST")
       time.sleep(1)
       issue_ids2 = temp_issue_ids
       issue_stats2 = temp_issue_stats
       issue_proj_ids2 = temp_issue_proj_ids
    temp_issue_stats = []
    temp_issue_ids = []
    temp_issue_proj_ids = []
    print(f"THIS SHOULD BE BLANK: {temp_issue_proj_ids}")
    if loop_count % 2 == 0:
        print(f"There are {issues_count} issues in total. {len(issue_ids)}")
        send_msg(f"You have {issues_count} issues total in your project.")
    if w == 0:
        print("waiting... make your change!")
        time.sleep(10)

print("\n \n HERE IS FIRST LIST:")
print(issue_stats)
print("\n \n HERE IS SECOND LIST:")
print(issue_stats2)
time.sleep(2)
if issue_stats == issue_stats2:
   print("lists are identical")
   send_msg("No changes have been made since the first loop excecuted")
else:
   print("lists aren't identical or you messed up the code")

   for i in range(len(issue_stats)):
      if issue_stats2[i] != issue_stats[i]:
         dif_activity_count += 1
         if issue_stats2[i] == 1:
             send_msg(f"Issue with id {issue_ids[i]} was completed!")
   send_msg(f"{dif_activity_count} issues have been changed since the last loop excecuted")
   print(f"{dif_activity_count} issues have been changed since the last loop excecuted") 
loop_time = time.time() - timer_start
print(f"It took {loop_time} seconds to finish one loop.")



#text = response.text.split(",")[1:-1]
#for i in range(len(text)):
#    print(text[i])

#print(f"there are {text[3][8:]} projects. ")
#projects = text[6:]
#print(f"")

#{"stuff":"More stuff", "things":"additional things", "results":[{"id":"iofdhs", "number":"6"}]}

# old method:
# Find all projects + index
# Find all issues + index
# Count all changes for all issues
# Wait
# Repeat previous steps
# Check any new changes made it complete
# Report if so
# 
# 
# 
# Better way:
# Find all projects + index
# Find all issues + index
# Index all status of issues
# Wait
# Check if any issues' statuses were changed to complete
# Report if so   

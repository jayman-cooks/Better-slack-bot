# Better Plane Slack Integration		
 One of the immediate weaknesses I saw within Plane project management(https://github.com/makeplane/plane) was the lack of a good notification system. I quickly turned to the Slack integration, thinking it would allow for more efficient communication. However, the custimization features were extremely lacking, as the slack bot reported on all activity(which would not be checked regularly by team members). To combat this, I have created a more customizable Slack bot.  
## Features
The program loops a certain number of times according to the loops variable. Currently, the program reports on: No issues being updated during the loop, how many issues were updated in the loop, and which issues were completed during the loop.
## Docker 
 To build the docker image, you need to your api keys into the second python file. Here are the necessary variables:
 - `slack_tok`: Your Slack bot token
 - `slack_sign`: Your Slack signing key
 - `plane_api`: Your Plane API key

You can replace the os.environ.get("SLACK_BOT_TOKEN") part with the string form of these tokens. Be careful with your Docker image as it now contains these important keys!

 Then to cd into the repo and build the image run: 
```bash
cd "Better slack bot"
docker build -t SlackBotImage
```


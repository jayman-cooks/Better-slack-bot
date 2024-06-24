# Better Plane Slack Integration		
 One of the immediate weaknesses I saw within Plane project management(https://github.com/makeplane/plane) was the lack of a good notification system. I quickly turned to the Slack integration, thinking it would allow for more efficient communication. However, the custimization features were extremely lacking, as the slack bot reported on all activity(which would not be checked regularly by team members). To combat this, I have created a more customizable Slack bot.  
## Features
The program loops a certain number of times according to the loops variable. Currently, the program reports on: No issues being updated during the loop, how many issues were updated in the loop, and which issues were completed during the loop.
## How to get necessary tokens:
You will need these variables to make your own instance of this bot:
 - `SLACK_BOT_TOKEN`: Your Slack bot token
 - `SLACK_SIGNING_SECRET`: Your Slack signing key
 - `PLANE_API_TOK`: Your Plane API key
 - `SLACK_CHANNEL`: The channel you want to recieve messages in
 - `PLANE_WORKSPACE_SLUG`: The slug of the Plane workspace you want to track
### Plane token:
To get your Plane API key, go to workspace settings --> API tokens --> add API token. I would recomend adding an expiration date for added security (which means you would have to update it).
### Slack token:
To get your slack token and signing key, you need to create a slack app. To do so, go to https://api.slack.com/apps?new_app=1, and click create app --> from scratch. Add what you want the name of your bot to be, and the workspace you want it in. After you created you app, go to OAuth & Permissions --> Scopes, and Add an OAuth scope. Type: chat:write. Once you have done this, you need to install it into your workspace. Go to OAuth Tokens for Your Workspace and Install to Workspace. Click Allow. Your token will now be under "OAuth Tokens for Your Workspace" and should start with "xoxb".
### Slack signing key:
In settings go to Basic Information --> App Credentials --> Signing Secret
### Slack channel:
Right click the channel you want --> view channel details --> scroll down to channel ID
### Workspace slug:
Finding the slug is very easy; simply navigate to your workspace and copy the section after https://app.plane.so/ but before the slash.


All of these variables are stored using environment variables under the names above(I would recommend looking it up if you don't know that that is.). 

## Running without Docker
Install dependancies in requirements.txt, and run the python script. 
## Docker 
 To build the docker image, you first need to put the above variables into the second python script (Better slack bot\Better_slack_bot) string form. Be careful with your Docker image as it now contains these important keys!

 Then to cd into the repo(if you haven't already) and build the image run: 
```bash
cd "Better slack bot"
docker build -t SlackBotImage
```
and to run it:
```bash
docker run -d -p 5000:5000 myimage
```
Your docker image should now run in a container!

## Using AWS:
To run this on AWS is a bit complicated. I will update the instructions soon, but you need to create an ECR repo, push the docker image, and create a Lambda function using it. 
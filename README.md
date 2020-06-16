# Dynamic Skill For Microsoft Bot Composer (Python)

## Setup

### Clone Repository

Run:
```
  git clone https://github.com/ConversationalComponents/coco-dynamic-skill-for-microsoft-bot-composer.git
```

### Install Requirements

Go to the copied folder and run:
```
  pip install -r requirements.txt
```

### Configure Skill
* Go to **./wwwroot/manifest/echoskillbot-manifest-1.0.json** and paste your **Microsoft App ID** to the **msAppId** key.
* Go to **config.py** and paste your **Microsoft App ID** and **Microsoft App Password** to **APP_ID** and **APP_PASSWORD** parameters.

### Add Skill To Composer And Add Skill To Conversation
At the skills window at the composer press **Connect To A New Skill** and paste at the following url: ``` http://localhost:39783/api/manifest ``` at **Manifest url**

### Pass Component ID To The Skill
At the **Connect To Skill** form at the **Activity** pass the component ID as at the following example:
```
 - namer_vp3
```

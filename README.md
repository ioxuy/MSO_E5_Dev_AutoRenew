# **MSO_E5_Dev_AutoRenew**

MSO_E5_Dev_AutoRenew is a Python application based on Git Actions that uses Microsoft Graph API to activate Microsoft Office 365 E5 Developer Trail membership auto-renewal automatically. This guide will provide you with easy-to-understand steps for setting up and running the application.

### Special Notes/Thanks ###
* Normal version address: [https://github.com/kylierst/MSO_E5_Dev_AutoRenew_REVISION_2](https://github.com/kylierst/MSO_E5_Dev_AutoRenew)
* Thanks to Ken5998 for code improvements and fix job skipping

## **Prerequisites**

- A GitHub account
- An existing or new Microsoft Developer E5 account with trial Subscription
- An Azure Portal account
- Basic knowledge of GitHub, Python, and Azure Portal

## **Setup Steps (Encrypted Secure Version)**

1. Fork the MSO_E5_Dev_AutoRenew repository to your GitHub account.
2. Register a new application in Azure Active Directory.
    - Select any organization directory, select "Web" for the redirect URL, and enter "**[http://localhost:53682/](http://localhost:53682/)**" for the redirect URL.
    - Save the Application ID and Secret.
3. Set application permissions.
    - Select the following permissions: **`files.read.all`**, **`files.readwrite.all`**, **`sites.read.all`**, **`sites.readwrite.all`**, **`user.read.all`**, **`user.readwrite.all`**, **`directory.read.all`**, **`directory.readwrite.all`**, **`mail.read`**, **`mail.readwrite`**, **`mailboxsetting.read`**, and **`mailboxsetting.readwrite`**.
    - Grant permission for all 13 selected permissions.
4. install rclone in your system. It is required to get refresh token (one time only)
5. Execute the command **`rclone authorize "onedrive" "id" "secret"`**.
    - Confirm the prompt and save the refresh token.
    - **id** is the Application ID you get it from previous steps
    - **secret** is the Application secret you get it from previous steps
6. Install JsonHandle chrome extention and open it. Paste the access_token acquired from previous step in the dialog box and copy the refresh token from it
7. Keep Application ID, Secret, Refresh_token handly you will need it in the next step
8. Go to the project settings and from the left hand side menu select Secrets and Variables > Actions
9. Click **New repository secrets.** and create three variables and set the value as given below
    - Name: **`CLIENT_ID`**
    - Name: **`CLIENT_SECRET`**
    - Name: **`REFRESH_TOKEN`**
    - If you require Telegram bot notifications, please set the **`TG_BOT_TOKEN`** and **`TG_CHAT_ID`**.
10. Goto the project setting again and choose Actions menu and scroll down until you see **Workflow permissions click Read and write permission option**
11. Go to your personal settings page on GitHub, select Developer settings > Personal access tokens > Generate new token.
    - Set the name to **`GITHUB_TOKEN`**.
    - Check the options **`repo`**, **`admin:repo_hook`**, and **`workflow`**.
    - Generate the token.
12. Click on the star button at the top right corner of the page to call it once.
13. Click on the Actions tab above to see the log of each run and check if the API is called correctly and if there are any errors.

## **Additional Information**

- The default setting is to run three rounds every six hours from Monday to Friday. You can modify your own crontab to change the frequency and time.
- If you need to modify the API calls, you can check the Graph Explorer at **[https://developer.microsoft.com/graph/graph-explorer/preview](https://developer.microsoft.com/graph/graph-explorer/preview)**.
- The GitHub Action provides a virtual environment with 2-core CPU, 7 GB RAM memory, and 14 GB SSD hard disk space.
- Each repository can only support 20 concurrent calls.

# jsd_job_bot

Shows which jobs are in my JSD queue

Installation: `pip install jsd-job-bot`

You need a `jsd_job_bot.ini` config file:

    [DEFAULT]
    JSD_API_KEY=<your api key>
    JSD_HOSTNAME=<your instance>.atlassian.net
    JSD_USERNAME=<your email address>

You can also set `SHOW_ALL_JOBS` which will show everything regardless of status.

The config file needs to be in one of these places:

* The current working directory.
* `~/.config`
* `~/etc/`

Run it, it'll show you what you've got assigned to you.

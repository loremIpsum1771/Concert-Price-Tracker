from crontab import CronTab
 
"""
Here the object can take two parameters one for setting 
the user cron jobs, it defaults to the current user 
executing the script if ommited. The fake_tab parameter 
sets a testing variable. So you can print what could be 
written to the file onscreen instead or writting directly
into the crontab file. 
"""
tab = CronTab(user='www',fake_tab='True')
cmd = '/var/www/pjr-env/bin/python /var/www/PRJ/job.py'
# You can even set a comment for this command
cron_job = tab.new(cmd, comment='This is the main command')
cron_job.minute().on(0)
cron_job.hour().on(12)
#writes content to crontab
tab.write()
print tab.render()
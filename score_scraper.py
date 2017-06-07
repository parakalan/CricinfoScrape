import dryscrape
import os
import sys

try:
    filepath = os.path.abspath(os.path.join(__file__, "../teams"))
    f = open(filepath)
    l = f.readlines()
    team1 = l[0].strip('\n')
    team2 = l[1].strip('\n')
except IOError:
    print "Starting for the first time"
    from crontab import CronTab
    cron = CronTab()
    job = cron.new(command = sys.executable + ' ' +  os.path.abspath(__file__))
    import getpass
    cron.write(user=getpass.getuser())
    team1 = raw_input("Team 1 : ")
    team2 = raw_input("Team 2 : ")
    interval = int(input("Notification interval : "))
    job.minute.every(interval)
    f = open('teams', 'w')
    f.write(team1 + '\n' + team2)

dryscrape.start_xvfb()
s = dryscrape.Session(
    base_url="http://www.espncricinfo.com/ci/engine/match/index.html")
s.visit('?view=live')
live_match_data = s.xpath('//*[@data-matchstatus="current"]')

for item in live_match_data:
        if team1 in item.text() and team2 in item.text():
            message = item.at_xpath('./*[@class="innings-info-1"]').text() \
                + '\\n' + item.at_xpath('./*[@class="innings-info-2"]').text()
            message = message.replace('&', '')
            notif = 'export DISPLAY=:0.0 && notify-send "%s vs %s" "%s" ' % \
                (team1, team2, message)
            os.system(notif)
            break
else:
    notif = 'export DISPLAY=:0.0 && notify-send "Sorry, live match not found"'
    os.system(notif)

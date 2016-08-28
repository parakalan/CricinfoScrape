import dryscrape
import os

try:
    f = open('teams')
    l = f.readlines()
    team1 = l[0].strip('\n')
    team2 = l[1].strip('\n')
except IOError:
    print "Starting for the first time"
    team1 = raw_input("Enter team 1 : ")
    team2 = raw_input("Enter team 2 : ")
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
            print notif
            os.system(notif)
            break

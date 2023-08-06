from bs4 import BeautifulSoup
import requests


def get_live_matches():
    response = []
    url = 'https://www.hltv.org/matches'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    live_matches = soup.find("div", class_="liveMatchesContainer").find_all("div", class_="liveMatch-container")

    
    for match in live_matches:
        match_link = "https://www.hltv.org" + match.find("a", class_="match")["href"]
        match_info = create_match_dictionary(match_link)
        response.append(match_info)

    return response

def create_match_dictionary(match_link):
    r = requests.get(match_link)
    soup = BeautifulSoup(r.text, "html.parser")

    match_info = {}

    #finding match box (there is some useful info there)
    match_box = soup.find("div", class_="teamsBox")
    
    #adding event details to match info
    event_details = {}
    event_name = match_box.find("div", class_="event").get_text()
    event_time = match_box.find("div", class_="time").get_text()
    event_date = match_box.find("div", class_="date").get_text()
    event_link = "https://www.hltv.org" + match_box.find("div", class_="event").find("a")["href"]
    event_id = event_link[28:].split('/', 1)[0]

    event_details["id"] = event_id
    event_details["name"] = event_name
    event_details["time"] = event_time
    event_details["date"] = event_date
    event_details["link"] = event_link

    match_info["event"] = event_details

    #adding teams details to the match info
    teams = match_box.find_all("div", class_="team")
    for idx, team in enumerate(teams):
        team_details = {}
        team_name = team.find("div", class_="teamName").get_text()
        team_link = "https://www.hltv.org" + team.find("a")["href"]
        team_id = team_link[26:].split('/', 1)[0]

        team_details['id'] = team_id
        team_details["team"] = team_name
        team_details["link"] = team_link
        match_info["team" + str(idx + 1)] = team_details
    

    return match_info

sus = get_live_matches()
print(sus)
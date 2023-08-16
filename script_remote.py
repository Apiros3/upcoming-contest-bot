from urllib.request import urlopen
import json
import datetime
import requests
import os

WEBHOOK_URL = os.environ["WEBHOOK"]
url = os.environ["CLISTURL"]

site_list = ["atcoder.jp", "codeforces.com", "leetcode.com", "codechef.com"]
site_name = ["AtCoder", "CodeForces", "LeetCode", "Codechef"]

response = urlopen(url)
dataset = json.loads(response.read())

def main():
    print("running...")

    lst = []
    now = datetime.datetime.now()
    # print(dataset["objects"])
    for info in dataset["objects"]:
        #YYYY-MM-DDTHH:MM:SS
        st = info["start"]
        contest_date = datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S")
        delta = contest_date - now 
        if (delta.days > 14 or delta.days < 0):
            continue

        site = ""
        for i in range(len(site_list)):
            if (info["host"] == site_list[i]):
                site = site_name[i]
        if (site != ""):
            lst.append([site, info["event"], info["href"], contest_date, info["duration"]])
    lst.reverse()
    post_message(lst)
    
    print("done!")

def duration(num):
    tn = "{:02d}".format(int(num%60))
    return f"{int(num/60)}:{tn}"

def post_message(message):
    # sends message to discord server
    payload = {
        "username" : "Upcoming Contests",
        "embeds" : [
            {
                "title": f"Contests starting within 14 days from {datetime.datetime.today().strftime('%Y-%m-%d')}",
                "description": "",
                # "color" : "002147",
                "fields" : []
            }
        ]
    }
    for contest in message:
        dt = contest[3].strftime("%Y/%m/%d %H:%M")
        payload["embeds"][0]["fields"].append({
            "name": f"{contest[0]}: {dt} ({duration(contest[4]/60)})",
            "value": f"[{contest[1]}]({contest[2]})",
        })

    with requests.post(WEBHOOK_URL, json=payload) as response :
        print(response.status_code)
    
if __name__ == "__main__":
    main()
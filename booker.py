from multiprocessing import Process
import sys, requests, time, logging, ast, credentials

#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

def main(shift):
    with requests.Session() as s:
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116"

        print "==================== Logging in ===================="
        login = s.post("https://chopeshift.challenger.sg/login/login_validation", credentials.logindata)
        print login.status_code
        print login.text

        if not login.ok:
            sys.exit("Login failed")

        cookiestring = ""
        for k, v in s.cookies.iteritems():
            if not k.startswith("_"):
                cookiestring += k + "=" + v +"; "

        s.headers["cookie"] = cookiestring[:-1]

        print "=" * 20 + " Getting calendar " + "=" * 20
        calendar = s.get("https://chopeshift.challenger.sg/schedule/scheduleCalendar")
        if not calendar.ok:
            sys.exit("Get calendar failed")
        print calendar.status_code

        result = ast.literal_eval(calendar.text.encode("UTF-8").replace("null", "None").strip())

        calendar_dict = {}
        for r in result:
            calendar_dict[str(r["description"]).strip()] = ["{0}/{1}/{2}".format(str(r["day"].zfill(2)), str(r["month"].zfill(2)), str(r["year"])), str(r["time"]).strip(), str(r["location"]).strip()]

        print "=" * 20 + " Booking shifts " + "=" * 20
        for k, v in calendar_dict.iteritems():
            if v == shift:
                chope = s.post("https://chopeshift.challenger.sg/schedule/book", {"slotNo": k, "extend": None})
                print chope.status_code
                print chope.text
                if chope.ok:
                    return

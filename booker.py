import sys, requests, time, logging, ast, credentials
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

def logout(s, shifttext):
    try:
        print "{0}: Logging out ...".format(shifttext)
        logout = s.get("https://chopeshift.challenger.sg/login/logout", timeout=10)
        print "{0}: Successfully logged out".format(shifttext)
    except Exception as exc:
        print "{0}: Log out failed with error: {1}".format(shifttext, str(exc))

def main(shift):
    shifttext = str(shift)

    with requests.Session() as s:
        retries = Retry(total=5,
                        backoff_factor=1,
                        method_whitelist=('GET', 'POST'),
                        status_forcelist=(500, 502, 504))
        adapter = HTTPAdapter(max_retries=retries)
        s.mount('http://', adapter)
        s.mount('https://', adapter)
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116"

        try:
            print "{0}: Logging in ...".format(shifttext)
            login = s.post("https://chopeshift.challenger.sg/login/login_validation", credentials.logindata, timeout=10)
        except Exception as exc:
            print "{0}: Login failed with error: {1}".format(shifttext, str(exc))
            return

        print "{0}: Login success".format(shifttext)

        cookiestring = ""
        for k, v in s.cookies.iteritems():
            if not k.startswith("_"):
                cookiestring += k + "=" + v +"; "

        s.headers["cookie"] = cookiestring[:-1]

        try:
            print "{0}: Getting calendar ...".format(shifttext)
            calendar = s.get("https://chopeshift.challenger.sg/schedule/scheduleCalendar", timeout=10)
        except Exception as exc:
            print "{0}: Get calendar failed with error: {1}".format(shifttext, str(exc))
            logout(s, shifttext)
            return

        print "{0}: Get calendar success".format(shifttext)

        result = ast.literal_eval(calendar.text.encode("UTF-8").replace("null", "None").strip())
        calendar_dict = {}
        accepted_dict = {}

        for r in result:
            statusslot = str(r["statusslot"]).strip().lower()
            slotno = str(r["slotno"]).strip()
            date = "{0}/{1}/{2}".format(str(r["day"].zfill(2)), str(r["month"].zfill(2)), str(r["year"]))
            time = str(r["time"]).strip().upper()
            location = str(r["location"]).strip().upper()

            if statusslot == "open":
                calendar_dict[slotno] = [date, time, location]

            elif statusslot == "accepted":
                accepted_dict.setdefault(date, []).append(time)

        if shift[0] in accepted_dict:
            if shift[1] in accepted_dict[shift[0]]:
                print "{0}: Already have a shift at this time slot".format(shifttext)
                logout(s, shifttext)
                return

        print "{0}: Try booking ...".format(shifttext)
        found = False

        for k, v in calendar_dict.iteritems():
            if v == shift:
                try:
                    chope = s.post("https://chopeshift.challenger.sg/schedule/book", {"slotNo": k, "extend": None}, timeout=10)
                    print "{0}: Shift booked successfully with status code {1} ({2})".format(shifttext, str(chope.status_code), str(chope.text))
                    found = True
                    break
                except Exception as exc:
                    print  "{0}: Shift booked failed with error: {1}".format(str(exc))

        if found == False:
            print "{0}: No matching shift found".format(shifttext)

        logout(s, shifttext)



        return

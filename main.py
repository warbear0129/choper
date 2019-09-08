from booker import main
from multiprocessing import Pool

toBook = [["09/09/2019", "06:30 PM - 09:31 PM", "PARKWAY PARADE"]]
#          ["09/11/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
#          ["09/12/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
#          ["09/10/2020", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
#          ["20/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
#          ["21/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
#          ["20/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"]]


if __name__ == "__main__":
    pool = Pool(4)
    results = pool.map(main, toBook)

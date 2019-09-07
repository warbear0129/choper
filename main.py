from booker import main
from multiprocessing import Pool

toBook = [["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
          ["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
          ["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
          ["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
          ["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
          ["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"],
          ["09/10/2019", "06:30 PM - 09:30 PM", "PARKWAY PARADE"]]


if __name__ == "__main__":
    pool = Pool(4)
    results = pool.map(main, toBook)

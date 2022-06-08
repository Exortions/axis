import threading

from requests import get
from time import sleep

class Ping:
    def ping_url(self, url, delay, thread, max=-1, verbose=False):
        attempts = 0
        
        while True:
            if max != -1 and attempts >= max:
                break

            res = get(url)
            
            if verbose:
                print(f'[{thread + 1}] Pinged {url} - {res.status_code} #{attempts + 1}')

            sleep(delay)
            attempts += 1

    def ping(self, url, threads, delay, max=-1, verbose=False):
        for i in range(threads):
            t = threading.Thread(target=ping_url, args=(url, delay, i, max, verbose))
            t.start()
        
        while True:
            if threading.active_count() == 1:
                break
        
        if verbose:
            print('Done')
    
    def start(self, url, threads, delay, max=-1, verbose=False):
        self.ping(url, threads, delay, max, verbose)
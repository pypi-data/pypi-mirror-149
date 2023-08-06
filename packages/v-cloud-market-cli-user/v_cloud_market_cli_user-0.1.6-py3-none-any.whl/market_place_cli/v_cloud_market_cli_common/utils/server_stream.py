from threading import Lock
import requests
import time
import json

class ServerStream(object):
    def __init__(self, max_retries=10, wait_seconds=5):
        self.is_open = False
        self.max_retries = max_retries
        self.wait_seconds = wait_seconds
        self.lock = Lock()
        self.response = None
        self.iterator = None

    def open(self, url: str, headers: dict, payload: dict, func: callable):
        self.lock.acquire()
        if self.is_open:
            self.lock.release()
            return
        self.is_open = True
        self.retry_time = self.max_retries
        self.lock.release()
        # print new data if stream reconnected
        total_line_num = 0
        while self.retry_time > 0:
            try:
                line_num = 0
                self.response = requests.get(url,
                                    headers=headers,
                                    params=payload,
                                    stream=True,
                                    timeout=(3, 3))
                if self.response.status_code != 200:
                    raise Exception(
                        "Cannot get stream (HTTP {}): {}".format(
                            self.response.status_code, self.response.text
                        )
                    )
                self.iterator = self.response.iter_lines()
                while self.is_open:
                    self.lock.acquire()
                    data = next(self.iterator)
                    self.lock.release()
                    # filter out keep-alive new lines
                    if data:
                        self.retry_time = self.max_retries
                        line_num += 1
                        if line_num > total_line_num:
                            func(data)
                        total_line_num = max(total_line_num, line_num)
            except requests.exceptions.RequestException:
                pass
            except requests.exceptions.ChunkedEncodingError:
                time.sleep(self.wait_seconds)
            except Exception as err:
                if len(str(err)) != 0:
                    self.retry_time -= 1
                time.sleep(self.wait_seconds)
            finally:
                if self.lock.locked():
                    self.lock.release()
        else:
            if self.is_open:
                print("User cli tool failed to reconnect to server!")
            self.close()

    def close(self):
        self.lock.acquire()
        self.is_open = False
        self.retry_time = 0
        if self.iterator:
            self.iterator.close()
        if self.response:
            self.response.close()
        self.lock.release()

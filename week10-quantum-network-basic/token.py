import time
from config import TOKEN_EXPIRY

class Token:
    def __init__(self, message):
        self.message = message
        self.read = False
        self.timestamp = time.time()

    def read_token(self):
        # ❌ อ่านซ้ำไม่ได้ หรือหมดอายุ
        if self.read or (time.time() - self.timestamp > TOKEN_EXPIRY):
            return None

        # ✅ อ่านครั้งเดียว = collapse
        self.read = True
        return self.message
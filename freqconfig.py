import json

class Freqconf:
    def __init__(self):
        self.fname = "freq_cfg.py"
    def get_freq(self):
        f = open(self.fname)
        dic = json.loads(f.read())
        f.close()
        return dic["freq"]
    def set_freq(self, freq):
        f = open(self.fname, mode = 'w+')
        dic = f'"freq":{freq}'
        dic = "{" + dic + "}"
        f.write(dic)
        f.close()


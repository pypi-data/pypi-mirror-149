from wolfpackutil.util import Log, Parser, Session, DB


class WolfpackUtil:
    url = "https://addons-ecs.forgesvc.net"
    github_url = "https://api.github.com/repos/{}/{}/releases"
    author = "WolfpackMC"
    repo = ""
    headers = {'User-Agent': 'WolfpackMC (made by Kalka) business inquiries: b@kalka.io'}

    def __init__(self):
        print("Wolfpackutil")
        self.log = Log()
        self.Session = Session
        self.Parser = Parser
        self.DB = DB



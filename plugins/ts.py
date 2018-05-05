# Roubado / adaptado de https://github.com/benediktschmitt/py-ts3/blob/master/ts3/examples/viewer.py

from pprint import pprint
from api import send_message
import ts3
import os

__all__ = ["ChannelTreeNode",
           "view"]

result = ""

class ChannelTreeNode(object):
    def __init__(self, info, parent, root, clients=None):
        self.info = info
        self.childs = list()

        # Init a root channel
        if root is None:
            self.parent = None
            self.clients = None
            self.root = self

        # Init a real channel
        else:
            self.parent = parent
            self.root = root
            self.clients = clients if clients is not None else list()
        return None

    @classmethod
    def init_root(cls, info):
        return cls(info, None, None, None)

    def is_root(self):
        return self.parent is None

    def is_channel(self):
        return self.parent is not None

    @classmethod
    def build_tree(cls, ts3conn, sid):
        ts3conn.use(sid=sid, virtual=True)

        resp = ts3conn.serverinfo()
        serverinfo = resp.parsed[0]

        resp = ts3conn.channellist()
        channellist = resp.parsed

        resp = ts3conn.clientlist()
        clientlist = resp.parsed
        # channel id -> clients
        clientlist = {cid: [client for client in clientlist \
                            if client["cid"] == cid]
                      for cid in map(lambda e: e["cid"], channellist)}

        root = cls.init_root(serverinfo)
        for channel in channellist:
            resp = ts3conn.channelinfo(cid=channel["cid"])
            channelinfo = resp.parsed[0]
            # This makes sure, that *cid* is in the dictionary.
            channelinfo.update(channel)

            channel = cls(
                info=channelinfo, parent=root, root=root,
                clients=clientlist[channel["cid"]])
            root.insert(channel)
        return root

    def insert(self, channel):
        self.root._insert(channel)
        return None

    def _insert(self, channel):
        if self.is_root():
            i = 0
            while i < len(self.childs):
                child = self.childs[i]
                if channel.info["cid"] == child.info["pid"]:
                    channel.childs.append(child)
                    self.childs.pop(i)
                else:
                    i += 1

        # This is not the root and the channel is a direct child of this one.
        elif channel.info["pid"] == self.info["cid"]:
            self.childs.append(channel)
            return True

        # Try to insert the channel recursive.
        for child in self.childs:
            if child._insert(channel):
                return True

        # If we could not find a parent in the whole tree, assume, that the
        # channel is a child of the root.
        if self.is_root():
            self.childs.append(channel)
        return False

    def generate_repr(self, indent=0):
        global result

        if self.is_root():
            # print(" "*(indent*3) + "|-", self.info["virtualserver_name"])
            result += str(" "*(indent*3)) + "|- " + self.info["virtualserver_name"] + "\n"
        else:
            #print(" "*(indent*3) + "|-", self.info["channel_name"])
            result += str(" "*(indent*3)) + "|- " + self.info["channel_name"] + "\n"
            for client in self.clients:
                # Ignore query clients
                if client["client_type"] == "1":
                    continue
                # print(" "*(indent*3+3) + "->", client["client_nickname"])
                result += str(" "*(indent*3+3)) + "-> " + client["client_nickname"] + "\n"

        for child in self.childs:
            child.generate_repr(indent=indent + 1)
        return None


def view(ts3conn, sid=1):
    global result
    result = ""

    tree = ChannelTreeNode.build_tree(ts3conn, sid)
    tree.generate_repr()

    return result


def on_msg_received(msg, matches):
    with ts3.query.TS3Connection("localhost") as ts3conn:
        ts3conn.login(client_login_name="serveradmin", client_login_password=os.environ["TS3PASS"])
        message = view(ts3conn, sid=1)

        send_message(msg["chat"]["id"], "```" + message + "```")
        send_message("14160874", "ts")


# Main
# ------------------------------------------------
if __name__ == "__main__":
    with ts3.query.TS3Connection("localhost") as ts3conn:
        ts3conn.login(client_login_name="serveradmin", client_login_password=os.environ["TS3PASS"])
        print(view(ts3conn, sid=1))

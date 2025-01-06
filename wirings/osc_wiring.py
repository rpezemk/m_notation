from utils.osc_udp.heartbeat_checker import HeartbeatChecker

hbck = HeartbeatChecker()

def all_message_handler(address, *args):
    print(args)
    ...

def heartbeat_handler(address, *args):
    print(args)
    ...

msg_handlers = [
    ("/*", all_message_handler),
    ("/heartbeat", heartbeat_handler)
    ]

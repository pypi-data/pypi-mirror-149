from time import sleep

from client.gui.main_window import start_main_window
from client.client_classfile import Client, ClientDataPreparation


def client_start():
    try:
        data = ClientDataPreparation()
        addr, port, name, pswd = data.client_parse_args()
        client = Client(addr, port, name, pswd)
        client.key_load()
        client.client_connect()
        client.start()
        sleep(2)
        start_main_window(client)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


if __name__ == '__main__':
    client_start()

#!/usr/bin/env python3

from decouple import config

import socket
import emoji
import re


class DefaultUser(Exception):
    """Raised when you try send a message with the default user"""
    pass


class CallbackFunction(Exception):
    """Raised when the callback function does not have (only)
    one required positional argument"""
    pass


class TwitchChatIRC:
    __HOST = 'irc.chat.twitch.tv'
    __DEFAULT_NICK = 'justinfan67420'
    __DEFAULT_PASS = 'SCHMOOPIIE'
    __PORT = 6667

    __PATTERN = re.compile(r'@(.+?(?=\s+:)).*PRIVMSG[^:]*:([^\r\n]*)')

    __CURRENT_CHANNEL = None

    def __init__(self, username=None, password=None, suppress_print=False):
        # try get from environment variables (.env)
        self.__NICK = config('NICK', self.__DEFAULT_NICK)
        self.__PASS = config('PASS', self.__DEFAULT_PASS)

        # overwrite if specified
        if(username is not None):
            self.__NICK = username
        if(password is not None):
            self.__PASS = f'oauth:{str(password).lstrip("oauth:")}'

        self.suppress_print = suppress_print

        # create new socket
        self.__SOCKET = socket.socket()

        # start connection
        self.__SOCKET.connect((self.__HOST, self.__PORT))
        if not self.suppress_print:
            print(f"Connected to {self.__HOST} on port {self.__PORT}")

        # log in
        self.__send_raw('CAP REQ :twitch.tv/tags')
        self.__send_raw(f'PASS {self.__PASS}')
        self.__send_raw(f'NICK {self.__NICK}')

    def __send_raw(self, string):
        self.__SOCKET.send((string+'\r\n').encode())

    def __print_message(self, message):
        demojized = emoji.demojize(
            message['message']).encode().decode(errors='ignore')
        print(f"[{message['tmi-sent-ts']}] "
              f"{message['display-name']}: {demojized}")

    def __recvall(self, buffer_size):
        data = b''
        while True:
            part = self.__SOCKET.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data.decode()  # ,'ignore'

    def __join_channel(self, channel_name):
        channel_lower = channel_name.lower()

        if(self.__CURRENT_CHANNEL != channel_lower):
            self.__send_raw(f'JOIN #{channel_lower}')
            self.__CURRENT_CHANNEL = channel_lower

    def is_default_user(self):
        return self.__NICK == self.__DEFAULT_NICK

    def close_connection(self):
        self.__SOCKET.close()
        if not self.suppress_print:
            print("Connection closed")

    def listen(self, channel_name, messages=[], timeout=None,
               message_timeout=1.0, on_message=None,
               buffer_size=4096, message_limit=None, output=None):
        self.__join_channel(channel_name)
        self.__SOCKET.settimeout(message_timeout)

        if(on_message is None):
            on_message = self.__print_message

        if not self.suppress_print:
            print("Begin retrieving messages:")

        time_since_last_message = 0
        readbuffer = ''
        try:
            while True:
                try:
                    new_info = self.__recvall(buffer_size)
                    readbuffer += new_info

                    if('PING :tmi.twitch.tv' in readbuffer):
                        self.__send_raw('PONG :tmi.twitch.tv')

                    matches = list(self.__PATTERN.finditer(readbuffer))

                    if(matches):
                        time_since_last_message = 0

                        if(len(matches) > 1):
                            # assume last one is incomplete
                            matches = matches[:-1]

                        last_index = matches[-1].span()[1]
                        readbuffer = readbuffer[last_index:]

                        for match in matches:
                            data = {}
                            for item in match.group(1).split(';'):
                                keys = item.split('=', 1)
                                data[keys[0]] = keys[1]
                            data['message'] = match.group(2)

                            messages.append(data)

                            if(callable(on_message)):
                                try:
                                    on_message(data)
                                except TypeError:
                                    raise Exception(
                                        f"Incorrect number of parameters for "
                                        f"function {on_message.__name__}")

                            if(message_limit is not None and
                               len(messages) >= message_limit):
                                return messages

                except socket.timeout:
                    if(timeout is not None):
                        time_since_last_message += message_timeout

                        if(time_since_last_message >= timeout):
                            if not self.suppress_print:
                                print(f"No data received in {timeout} "
                                      f"seconds. Timing out.")
                            break

        except KeyboardInterrupt:
            print("Interrupted by user.")
        except Exception as e:
            print("Unknown Error:", e)
            raise e

        return messages

    def send(self, channel_name, message):
        self.__join_channel(channel_name)

        # check that is using custom login, not default
        if(self.is_default_user()):
            raise DefaultUser
        else:
            self.__send_raw(f'PRIVMSG #{channel_name.lower()} :{message}')
            if not self.suppress_print:
                print(f"Sent '{message}' to {channel_name}")

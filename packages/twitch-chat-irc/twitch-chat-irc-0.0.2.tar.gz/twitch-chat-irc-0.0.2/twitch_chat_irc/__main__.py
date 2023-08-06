#!/usr/bin/env python3

from twitch_chat_irc import twitch_chat_irc

import argparse
import json
import csv


parser = argparse.ArgumentParser(
    description=("Send and receive Twitch chat messages over IRC "
                 "with python web sockets. For more info, go to "
                 "https://dev.twitch.tv/docs/irc/guide"))
parser.add_argument('channel_name',
                    help='Twitch channel name (username)')
parser.add_argument('-timeout', '-t',
                    default=None, type=float,
                    help=("Time in seconds needed to close connection "
                          "after not receiving any new data "
                          "(default: None = no timeout)"))
parser.add_argument('-message_timeout', '-mt',
                    default=1.0, type=float,
                    help=("Time in seconds between checks for new data "
                          "(default: 1 second)"))
parser.add_argument('-buffer_size', '-b',
                    default=4096, type=int,
                    help="Buffer size (default: 4096 bytes = 4 KB)")
parser.add_argument('-message_limit', '-l',
                    default=None, type=int,
                    help=("Maximum amount of messages to get "
                          "(default: None = unlimited)"))
parser.add_argument('-username', '-u',
                    default=None,
                    help="Username (default: None)")
parser.add_argument('-oauth', '-password', '-p',
                    default=None,
                    help=("oath token (default: None). "
                          "Get custom one from "
                          "https://twitchapps.com/tmi/"))
parser.add_argument('--send',
                    action='store_true',
                    help="Send mode (default: False)")
parser.add_argument('-output', '-o',
                    default=None,
                    help=("Output file "
                          "(default: None = print to standard output)"))

args = parser.parse_args()

twitch_chat = twitch_chat_irc.TwitchChatIRC(username=args.username,
                                            password=args.oauth)

if(args.send):
    if(twitch_chat.is_default_user()):
        print("Unable to send messages with default user. "
              "Please provide valid authentication.")
    else:
        try:
            while True:
                message = input(">>> Enter message (blank to exit): \n")
                if(not message):
                    break
                twitch_chat.send(args.channel_name, message)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")

else:
    messages = twitch_chat.listen(
        args.channel_name,
        timeout=args.timeout,
        message_timeout=args.message_timeout,
        buffer_size=args.buffer_size,
        message_limit=args.message_limit)

    if(args.output is not None):
        if(args.output.endswith('.json')):
            with open(args.output, 'w') as fp:
                json.dump(messages, fp)
        elif(args.output.endswith('.csv')):
            with open(
                    args.output, 'w', newline='', encoding='utf-8') as fp:
                fieldnames = []
                for message in messages:
                    fieldnames += message.keys()

                if len(messages) > 0:
                    fc = csv.DictWriter(fp,
                                        fieldnames=list(set(fieldnames)))
                    fc.writeheader()
                    fc.writerows(messages)
        else:
            f = open(args.output, 'w', encoding='utf-8')
            for message in messages:
                print(f"[{message['tmi-sent-ts']}] "
                      f"{message['display-name']}: {message['message']}",
                      file=f)
            f.close()

        print(f"Finished writing {len(messages)} messages "
              "to {args.output}")

twitch_chat.close_connection()

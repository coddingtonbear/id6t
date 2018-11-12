import json
import socketserver
import time
import traceback
import uuid

import redis

from id6t.maxwell.models import Data, DataSet

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.management.base import BaseCommand

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 30224  # Arbitrary non-privileged port


class MaxwellHandler(socketserver.StreamRequestHandler):
    def update(self):
        try:
            ds = DataSet.objects.all().order_by(
                '-created'
            )[0]
            self.redis_connection.set(
                'maxwell.state',
                json.dumps(ds.as_dict()).encode('utf-8')
            )
            self.redis_connection.publish(
                'maxwell.events',
                json.dumps(ds.as_dict()).encode('utf-8')
            )
        except IndexError:
            pass

    def handle(self):
        authenticated = False
        dataset = None

        self.redis_connection = redis.Redis(
            settings.REDIS_HOST,
            settings.REDIS_PORT,
        )

        for raw_line in self.rfile:
            line = raw_line.strip()
            is_command = False

            if line == b'\x04':
                if dataset:
                    self.update()

            if line.startswith(b"^"):
                is_command = True

                line = line[1:]

            try:
                if is_command:
                    try:
                        cmd_name, value = line.decode('utf-8').split('=', 1)
                    except ValueError:
                        cmd_name = line.decode('utf-8')
                        value = None

                    if cmd_name == 'authenticate':
                        username, password = value.split('|')
                        # Wait 1s regardless of authentication success
                        # to circumvent timing attacks
                        wait_until = time.time() + 1
                        if authenticate(
                            username=username,
                            password=password
                        ) is not None:
                            authenticated = True
                            print("Authentication succeeded")
                        else:
                            print("Authentication failed")
                        while(time.time() < wait_until):
                            time.sleep(0.1)
                    if cmd_name == 'dataset':
                        if dataset:
                            self.update()
                        print("New dataset started")
                        dataset = str(uuid.uuid4())
                    continue
                else:
                    type_name, value = line.decode('utf-8').split('=', 1)

                if value.strip():
                    if authenticated and dataset:
                        print(
                            Data.create(
                                dataset,
                                type_name,
                                value,
                            )
                        )
                    # Send ACK regardless of authentication status to prevent
                    # making it clear when auth has succeeded
                    self.request.send(b'\x06')
                else:
                    self.request.send(b'\x15')
            except (ValueError, TypeError):
                traceback.print_exc()
                self.request.send(b'\x15')


class Command(BaseCommand):
    def handle(self, *args, **options):
        with socketserver.TCPServer((HOST, PORT, ), MaxwellHandler) as server:
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                server.server_close()

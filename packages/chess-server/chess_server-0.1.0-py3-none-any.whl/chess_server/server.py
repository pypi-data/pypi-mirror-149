#!/usr/bin/env python

import asyncio
import websockets
import chess
import secrets


class ChessServer(object):
    def __init__(self):
        self.board = chess.Board()
        self.socket = None
        self.running = False
        self.sockets = set()

    # receives FEN message
    def processMessage(self, fen):
        print('received: ' + fen)
        try:
            self.board.set_fen(fen)
            return fen
        except:
            return 'invalid move!'

    def start(self):
        if self.running:
            pass

        async def sockethandler(socket):
            self.socket = socket
            self.sockets.add(socket)
            async for message in socket:
                fen = self.processMessage(message)
                deleted = set()
                for s in self.sockets:
                    try:
                        print('sending: ' + fen)
                        await s.send(fen)
                    except:
                        deleted.add(s)
                for d in deleted:
                    self.sockets.remove(d)


        async def startserver():
            async with websockets.serve(sockethandler, "localhost", 8765):
                self.running = True
                await asyncio.Future()  # run forever

        asyncio.run(startserver())


c = ChessServer()
c.start()
from shared.c2s.ChooseTeamC2S import ChooseTeamC2S
from shared.c2s.HandshakeC2S import HandshakeC2S
from shared.c2s.SwitchSpymasterC2S import SwitchSpymasterC2S
from shared.PacketHandler import PacketHandler
from shared.s2c.ChooseTeamS2C import ChooseTeamS2C
from shared.s2c.HandshakeS2C import HandshakeS2C
from shared.s2c.PlayerJoinedS2C import PlayerJoinedS2C
from shared.synchronized import synchronized

from server.ClientHandler import ClientHandler
from server.Server import Server


class ServerPacketHandler():

    def __init__(self, server: Server):
        self.server = server
        self.packetHandler = PacketHandler()
        self.packetHandler.register(HandshakeC2S, self.handleHandshake)
        self.packetHandler.register(ChooseTeamC2S, self.handleChooseTeam)
        self.packetHandler.register(
            SwitchSpymasterC2S, self.handleSwitchSpymaster)

    @synchronized
    def handle(self, packet, param):
        self.packetHandler.handleWithParam(packet, param)

    def sendToOthers(self, data, param):
        for handler in self.server.clientHandlers:
            if handler is not param:
                handler.send(data)

    def handleHandshake(self, data: HandshakeC2S, param: ClientHandler):
        param.player.name = data.name

        param.send(HandshakeS2C(self.server.game.players))

        self.server.game.players.append(param.player)
        self.sendToOthers(PlayerJoinedS2C(param.player), param)

    def handleChooseTeam(self, data: ChooseTeamC2S, param: ClientHandler):
        param.player.team = data.team
        self.sendToOthers(ChooseTeamS2C(data.team, param.player.name), param)

    def handleSwitchSpymaster(self, data: SwitchSpymasterC2S, param: ClientHandler):
        pass

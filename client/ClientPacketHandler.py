import pickle
from PyQt5.QtCore import QObject
from shared.s2c.SpymasterHintS2C import SpymasterHintS2C
from shared.c2s.SpymasterHintC2S import SpymasterHintC2S
from shared.s2c.GameEndS2C import GameEndS2C
from shared.s2c.SwitchPlayingSideS2C import SwitchPlayingSideS2C
from shared.s2c.TeamScoreS2C import TeamScoreS2C
from shared.CardColor import CardColor
from shared.Team import Team
from shared.s2c.CardSelectS2C import CardSelectS2C
from shared.c2s.CardSelectC2S import CardSelectC2S
from shared.c2s.CardVoteC2S import CardVoteC2S
from shared.c2s.ChooseTeamC2S import ChooseTeamC2S
from shared.c2s.GameStartC2S import GameStartC2S
from shared.c2s.HandshakeC2S import HandshakeC2S
from shared.c2s.SwitchSpymasterC2S import SwitchSpymasterC2S
from shared.PacketHandler import PacketHandler
from shared.s2c.CardVoteS2C import CardVoteS2C
from shared.s2c.ChooseTeamS2C import ChooseTeamS2C
from shared.s2c.GameStartS2C import GameStartS2C
from shared.s2c.HandshakeS2C import HandshakeS2C
from shared.s2c.PlayerJoinedS2C import PlayerJoinedS2C
from shared.s2c.SwitchSpymasterS2C import SwitchSpymasterS2C


class ClientPacketHandler(QObject):
    def __init__(self, netClient):
        QObject.__init__(self)
        netClient.onPacketReceive.connect(self.onPacket)

    def onPacket(self, buff):
        data = pickle.loads(buff)
        print(data)

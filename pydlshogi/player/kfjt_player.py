import numpy as np
import chainer
from chainer.backends import cuda 
from chainer import Variable
from chainer import serializers
import chainer.functions as F

import shogi

from pydlshogi.common import *
from pydlshogi.features import *
from pydlshogi.network.policy import *
from pydlshogi.player.base_player import *

from random import choice
from heapq import nlargest

# def greedy(logits):
#     return logits.index(max(logits))

# def boltzmann(logits, temperature):
#     logits /= temperature
#     logits -= logits.max()
#     probabilities = np.exp(logits)
#     probabilities /= probabilities.sum()
#     return np.random.choice(len(logits), p=probabilities)

class PolicyPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.modelfile = r'C:\kfjt-dlshogi\model\model_policy'
        self.model = None

    def usi(self):
        print('id name kfjt_player')
        print('option name modelfile type string default ' + self.modelfile)
        print('usiok')

    def setoption(self, option):
        if option[1] == 'modelfile':
            self.modelfile = option[3]

    def isready(self):
        if self.model is None:
            self.model = PolicyNetwork()
            self.model.to_gpu()
        serializers.load_npz(self.modelfile, self.model)
        print('readyok')

    def go(self):
        if self.board.is_game_over():
            print('bestmove resign')
            return

        xp = cuda.cupy
        features = make_input_features_from_board(self.board)
        x = Variable(xp.array([features], dtype=xp.float32))

        with chainer.no_backprop_mode():
            y = self.model(x)

            logits = cuda.to_cpu(y.data)[0]
            probabilities = cuda.to_cpu(F.softmax(y).data)[0]

        # 全ての合法手について
        turn = self.board.turn
        legal_moves = []
        legal_logits = []
        for move in self.board.legal_moves:
            # ラベルに変換
            label = make_output_label(move, turn)
            # 合法手とその指し手の確率(logits)を格納
            legal_moves.append(move)
            legal_logits.append(logits[label])
            # 確率を表示
            print('info string {:5} : {:.5f}'.format(move.usi(), probabilities[label]))
            
        # 確率が最大の手を選ぶ(グリーディー戦略)
        # selected_index = greedy(legal_logits)
        # 確率に応じて手を選ぶ(ソフトマックス戦略)
        # selected_index = boltzmann(np.array(legal_logits, dtype=np.float32), 0.5)
        # 確率上位３からランダム選択
        selected_index = legal_logits.index(choice(nlargest(3, legal_logits)))
        bestmove = legal_moves[selected_index]

        print('bestmove', bestmove.usi())

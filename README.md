# kfjt-shogi

clone https://github.com/TadaoYamaoka/python-dlshogi

## train

+ [http://wdoor.c.u-tokyo.ac.jp/shogi/](http://wdoor.c.u-tokyo.ac.jp/shogi/)
  + year: 2018
  + rate: 3800
  + moves: 150
+ pydlshogi.network.policy.PolicyNetwork

## player

+ fork pydlshogi.player.policy_player.PolicyPlayer
  + chainer 5 compatible
  + Random selection from probability top 3

## 将棋所

### エンジン管理

#### 追加

+ kfjt-shogi.bat

#### エンジン設定

+ model_policy
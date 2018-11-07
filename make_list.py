import argparse
from pathlib import Path
import re
import random

from logging import basicConfig, getLogger, DEBUG, FileHandler
basicConfig(level=DEBUG)
logger = getLogger(__name__)
# fh = FileHandler('usi.log')
# logger.addHandler(fh)

parser = argparse.ArgumentParser()
parser.add_argument('--kifudir', type=str, default=".")
parser.add_argument('--rate', type=int, default=3800)
parser.add_argument('--moves', type=int, default=150)
parser.add_argument('--outdir', type=str, default=".")
parser.add_argument('--outfile', type=str, default="kifulist")
parser.add_argument('--ratio', type=float, default=0.9)
args = parser.parse_args()

p = Path(args.kifudir)
ptn_rate = re.compile(r"^'(black|white)_rate:.*:(.*)$")

kifu_list = []
for filepath in p.glob("**/*.csa"):
    rate = {}
    move_len = 0
    for line in open(filepath, 'r', encoding='utf-8'):
        line = line.strip()
        m = ptn_rate.match(line)
        if m:
            rate[m.group(1)] = float(m.group(2))
        if line[:1] == '+' or line[:1] == '-':
            move_len += 1
        if line == '%TORYO' \
        and len(rate) == 2 \
        and args.rate < min(rate.values()) \
        and args.moves < move_len:
            kifu_list.append(filepath.resolve())
            logger.debug("[{}]rate:{}/move:{}".format(len(kifu_list), min(rate.values()), move_len))
            break

random.shuffle(kifu_list)

train_len = int(len(kifu_list) * args.ratio)
with open(Path(args.outdir, '{}_train.txt'.format(args.outfile)), 'w') as f:
    [f.write('{}\n'.format(kifu)) for kifu in kifu_list[:train_len]]

with open(Path(args.outdir, '{}_test.txt'.format(args.outfile)), 'w') as f:
    [f.write('{}\n'.format(kifu)) for kifu in kifu_list[train_len:]]

logger.debug('total kifu num = {}'.format(len(kifu_list)))
logger.debug('train kifu num = {}'.format(train_len))
logger.debug('test kifu num = {}'.format(len(kifu_list[train_len:])))

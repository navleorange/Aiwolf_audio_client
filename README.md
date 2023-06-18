# Aiwolf_audio_client
このプログラムは人間同士が会話をして行う人狼ゲームにAIエージェントが参加できることを目的として作成されたプログラムの内の人間用クライアントプログラムです。このプログラムでは人狼ゲームゲームマスターのサーバプログラム(後述)に接続するほか、話している人間の声をテキストに変換してサーバに渡し、AIエージェントに伝える役割を持っています。

<br>

## リリース
以下にあります。

[https://github.com/navleorange/Aiwolf_audio_client/releases/tag/v1.0-alpha](https://github.com/navleorange/Aiwolf_audio_client/releases/tag/v1.0-alpha)

<br>

## 注意点
リリースはNuitkaでexe化したため、製作者が作成を行ったOSであるWindowsでのみ動作するようです。
> (他の環境を持っていないためプログラムの実行はどうなるか不明)

<br>

## サーバプログラムについて
後日公開します... 

<br>

## ゲームの始め方
基本的に1プレイヤー、1つプログラムを実行してください。(プレイヤー毎別々のPCでやることを想定しています。)

1. hostとportを設定してください

	<details><summary>./res/config.iniを以下に従って書き換えてください。</summary><div>
	
	```
	[connection]
	host = ここにサーバのIP
	port = ここにサーバのポート
	```

	</div></details>
	<br>

1. サーバプログラム起動確認後、`人狼ゲーム.exe`を起動する。

<br>

## ゲームの起動後
1. 名前の入力を促すポップアップが出てくるので名前を入力してください

	![name](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/56772706-9cee-431f-96db-98cdd30cee0b)

	> 入力するまでこのポップアップは消えません(空欄等でも)

1. どのオーディオデバイスを使用するか聞かれるので答えてください

	![devide_index](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/4c58fc11-17d4-4726-ae8b-7b4d30ddebda)


1. 他のプレイヤーの接続を待ちます

	![waiting](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/fd4cff7d-df41-4eb8-8ab8-328d8584fc50)


1. 全プレイヤー接続後、ルール説明が開始されます

	![rule](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/b5af83ef-f2bc-4484-b282-902a8660c74c)

1. 確認後、あなたの役職が発表されます

	![role](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/ff43f47e-f894-4c3e-b5e6-57ba4da1c4a5)

<br>

## ゲームの行動について
1. 指名する行動 (投票、占い師の占い、人狼の襲撃、etc...)
	
	以下のような感じで、自身以外のその対象となる人の一覧が現れるので、指名したい相手の名前をクリックしてください。

	![vote](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/14b8466a-90a8-448e-b94d-26f0486c1aa5)


1. 会話

	以下のような感じで、右側にあなたが発言した内容を文字起こしした内容が表示されます。
	
	![audio](https://github.com/navleorange/Aiwolf_audio_client/assets/74340680/7fb6e0d2-1455-47dd-9285-674bce7188b8)
	
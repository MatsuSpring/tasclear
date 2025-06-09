# TasClear

大学生の課題管理に特化したToDoアプリ。

毎日のように課される課題（***Task***）を明確（***Clear***）に管理し、確実に完了（***Clear***）することをサポートします。


## 実行方法
### 1. `git clone`
リポジトリを任意の場所へクローン
```bash
git clone https://github.com/MatsuSpring/tasclear.git
```
### 2. `uv sync`
このプロジェクトはuvで環境とライブラリを管理しています。
リポジトリディレクトリ内で以下のコマンドを実行すると依存する環境が自動でインストールされます。
```bash
uv sync
```
### 3. 環境のアクティベート
uvにより構築された環境を有効化します。

**Linux/MacOS**
```bash
. ./.venv/bin/activate
```

**Windows(recommend git bash)**
```bash
. ./.venv/Scripts/activate
```
### 4. `flet run`
Fletアプリを実行します。
```bash
flet run
```
> [!TIP]
> 初回実行時には自動的に`main.db`が作成されますが、これは正常な動作です。


## モバイルデバイスへのインストール
> [!NOTE]
> 現在Android端末でのみ動作を確認しています
### 1. `git clone`
リポジトリを任意の場所へクローン
```bash
git clone https://github.com/MatsuSpring/tasclear.git
```
### 2. `uv sync`
このプロジェクトはuvで環境とライブラリを管理しています。
リポジトリディレクトリ内で以下のコマンドを実行すると依存する環境が自動でインストールされます。
```bash
uv sync
```
### 3. 環境のアクティベート
uvにより構築された環境を有効化します。

**Linux/MacOS**
```bash
. ./.venv/bin/activate
```

**Windows(recommend git bash)**
```bash
. ./.venv/Scripts/activate
```

### 4. `flet build apk`
FletアプリをAndroidアプリとしてビルドします。
> [!WARNING]
> 初回実行時には、Flutter SDK, Android SDK, Java(JDK)が自動的に環境にインストールされます（存在しない場合）。
> ご注意ください。
> 詳しくは[Flet公式ドキュメント](https://flet.dev/docs/publish/android/)をご覧ください。

```bash
flet build apk
```

### 5. デバイスにインストール
`build/apk`ディレクトリに作成された`app-release.apk`をAndroidデバイスに送信し、インストールを行います。

データはローカルにのみ保存されます。

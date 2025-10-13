---
lab:
  title: Azure AI Voice Live 音声エージェントを開発する
  description: Azure AI Voice Live エージェントとのリアルタイムの音声対話を可能にする Web アプリの作成方法を学習します。
---

# Azure AI Voice Live 音声エージェントを開発する

この演習では、エージェントとのリアルタイムの音声対話を可能にする Flask ベースの Python Web アプリを完成します。 セッションを初期化し、セッション イベントを処理するコードを追加します。 デプロイ スクリプトを使用します。このスクリプトでは、AI モデルをデプロイし、Azure Container Registry (ACR) タスクを使用して ACR にアプリのイメージを作成し、そのイメージをプルする Azure App Service インスタンスを作成します。 アプリをテストするには、マイクとスピーカーの機能を備えたオーディオ デバイスが必要です。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用して同様のアプリケーションを開発できます。

- [.NET 用 Azure VoiceLive クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.VoiceLive/)

この演習で実行されるタスク:

* アプリのベース ファイルをダウンロードする
* コードを追加して Web アプリを完成する
* コード ベース全体を確認する
* デプロイ スクリプトを更新して実行する
* アプリケーションの表示とテスト

この演習の所要時間は約 **30** 分です。

## Azure Cloud Shell を起動してファイルをダウンロードする

演習のこのセクションでは、アプリのベース ファイルを含む ZIP ファイルをダウンロードします。

1. お使いのブラウザーで Azure portal ([https://portal.azure.com](https://portal.azure.com)) に移動し、メッセージに応じて Azure 資格情報を使用してサインインします。

1. ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal 内に新しいクラウド シェルを作成します。***Bash*** 環境を選択すること。 Azure portal の下部にあるペインに、Cloud Shell のコマンド ライン インターフェイスが表示されます。

    > **注**: *PowerShell* 環境を使用するクラウド シェルを以前に作成している場合は、それを ***Bash*** に切り替えること。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

1. **Bash** シェルで次のコマンドを実行して、演習ファイルをダウンロードし、解凍します。 2 番目のコマンドではさらに、演習ファイル用のディレクトリに移動します。

    ```bash
    wget https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/downloads/python/voice-live-web.zip
    ```

    ```
    unzip voice-live-web.zip && cd voice-live-web
    ```

## コードを追加して Web アプリを完成する

演習ファイルがダウンロードされたので、次の手順では、コードを追加してアプリケーションを完成します。 以下の手順は Cloud Shell で実行されます。 

>**ヒント:** 上部の境界線をドラッグして Cloud Shell のサイズを変更すると、より多くの情報とコードが表示されます。 最小化ボタンと最大化ボタンを使用して、Cloud Shell とメイン ポータル インターフェイスを切り替えることもできます。

演習を続行する前に、次のコマンドを実行して *src* ディレクトリに移動します。

```bash
cd src
```

### 音声ライブ アシスタントを実装するコードを追加する

このセクションでは、音声ライブ アシスタントを実装するコードを追加します。 **\_\_init\_\_** メソッドは、Azure VoiceLive 接続パラメーター (エンドポイント、資格情報、モデル、音声、システム命令) を格納し、接続ライフサイクルの管理と会話中のユーザーによる中断の処理を行うためのランタイム状態変数を設定して、音声アシスタントを初期化します。 **start** メソッドは、WebSocket 接続の確立とリアルタイム音声セッションの構成に使用するために必要な Azure VoiceLive SDK コンポーネントをインポートします。

1. 編集するために、次のコマンドを実行して *flask_app.py* ファイルを開きます。

    ```bash
    code flask_app.py
    ```

1. コード内で、コメント **# BEGIN VOICE LIVE ASSISTANT IMPLEMENTATION - ALIGN CODE WITH COMMENT** を検索します。 次のコードをコピーし、そのコメントのすぐ下に入力します。 インデントを必ず確認してください。

    ```python
    def __init__(
        self,
        endpoint: str,
        credential,
        model: str,
        voice: str,
        instructions: str,
        state_callback=None,
    ):
        # Store Azure Voice Live connection and configuration parameters
        self.endpoint = endpoint
        self.credential = credential
        self.model = model
        self.voice = voice
        self.instructions = instructions
        
        # Initialize runtime state - connection established in start()
        self.connection = None
        self._response_cancelled = False  # Used to handle user interruptions
        self._stopping = False  # Signals graceful shutdown
        self.state_callback = state_callback or (lambda *_: None)

    async def start(self):
        # Import Voice Live SDK components needed for establishing connection and configuring session
        from azure.ai.voicelive.aio import connect  # type: ignore
        from azure.ai.voicelive.models import (
            RequestSession,
            ServerVad,
            AzureStandardVoice,
            Modality,
            InputAudioFormat,
            OutputAudioFormat,
        )  # type: ignore
    ```

1. **Ctrl + s** キーを入力して変更を保存します。次のセクションでも使用するため、エディターは開いたままにしておきます。

### 音声ライブ アシスタントを実装するコードを追加する

このセクションでは、音声ライブ セッションを構成するコードを追加します。 これにより、モダリティ (API では、オーディオのみはサポートされていません)、アシスタントの動作を定義するシステム命令、応答用の Azure TTS 音声、入力と出力の両方のストリームのオーディオ形式、ユーザーが話し始めたときと話し終えたときをモデルが検出する方法を指定するサーバー側音声アクティビティ検出 (VAD) を指定します。

1. コード内で、コメント **# BEGIN CONFIGURE VOICE LIVE SESSION - ALIGN CODE WITH COMMENT** を検索します。 次のコードをコピーし、そのコメントのすぐ下に入力します。 インデントを必ず確認してください。

    ```python
    # Configure VoiceLive session with audio/text modalities and voice activity detection
    session_config = RequestSession(
        modalities=[Modality.TEXT, Modality.AUDIO],
        instructions=self.instructions,
        voice=voice_cfg,
        input_audio_format=InputAudioFormat.PCM16,
        output_audio_format=OutputAudioFormat.PCM16,
        turn_detection=ServerVad(threshold=0.5, prefix_padding_ms=300, silence_duration_ms=500),
    )
    await conn.session.update(session=session_config)
    ```

1. **Ctrl + s** キーを入力して変更を保存します。次のセクションでも使用するため、エディターは開いたままにしておきます。

### セッション イベントを処理するコードを追加する

このセクションでは、音声ライブ セッションのイベント ハンドラーを追加するコードを追加します。 イベント ハンドラーは、会話のライフサイクル中に主要な VoiceLive セッション イベントに応答します。**_handle_session_updated** は、セッションがユーザー入力の準備ができたときに通知します。**_handle_speech_started** は、ユーザーが話し始めたことを検出すると、進行中のアシスタントのオーディオ再生を停止し、進行中の応答をキャンセルして、中断ロジックを実装し、自然な会話フローを可能にします。**_handle_speech_stopped** は、ユーザーが話し終えてアシスタントが入力の処理を開始したときの処理を行います。

1. コード内で、コメント **# BEGIN HANDLE SESSION EVENTS - ALIGN CODE WITH COMMENT** を検索します。 次のコードをコピーし、そのコメントのすぐ下に入力します。インデントを必ず確認してください。

    ```python
    async def _handle_event(self, event, conn, verbose=False):
        """Handle Voice Live events with clear separation by event type."""
        # Import event types for processing different Voice Live server events
        from azure.ai.voicelive.models import ServerEventType
        
        event_type = event.type
        if verbose:
            _broadcast({"type": "log", "level": "debug", "event_type": str(event_type)})
        
        # Route Voice Live server events to appropriate handlers
        if event_type == ServerEventType.SESSION_UPDATED:
            await self._handle_session_updated()
        elif event_type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
            await self._handle_speech_started(conn)
        elif event_type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
            await self._handle_speech_stopped()
        elif event_type == ServerEventType.RESPONSE_AUDIO_DELTA:
            await self._handle_audio_delta(event)
        elif event_type == ServerEventType.RESPONSE_AUDIO_DONE:
            await self._handle_audio_done()
        elif event_type == ServerEventType.RESPONSE_DONE:
            # Reset cancellation flag but don't change state - _handle_audio_done already did
            self._response_cancelled = False
        elif event_type == ServerEventType.ERROR:
            await self._handle_error(event)

    async def _handle_session_updated(self):
        """Session is ready for conversation."""
        self.state_callback("ready", "Session ready. You can start speaking now.")

    async def _handle_speech_started(self, conn):
        """User started speaking - handle interruption if needed."""
        self.state_callback("listening", "Listening… speak now")
        
        try:
            # Stop any ongoing audio playback on the client side
            _broadcast({"type": "control", "action": "stop_playback"})
            
            # If assistant is currently speaking or processing, cancel the response to allow interruption
            current_state = assistant_state.get("state")
            if current_state in {"assistant_speaking", "processing"}:
                self._response_cancelled = True
                await conn.response.cancel()
                _broadcast({"type": "log", "level": "debug", 
                          "msg": f"Interrupted assistant during {current_state}"})
            else:
                _broadcast({"type": "log", "level": "debug", 
                          "msg": f"User speaking during {current_state} - no cancellation needed"})
        except Exception as e:
            _broadcast({"type": "log", "level": "debug", 
                      "msg": f"Exception in speech handler: {e}"})

    async def _handle_speech_stopped(self):
        """User stopped speaking - processing input."""
        self.state_callback("processing", "Processing your input…")

    async def _handle_audio_delta(self, event):
        """Stream assistant audio to clients."""
        if self._response_cancelled:
            return  # Skip cancelled responses
            
        # Update state when assistant starts speaking
        if assistant_state.get("state") != "assistant_speaking":
            self.state_callback("assistant_speaking", "Assistant speaking…")
        
        # Extract and broadcast Voice Live audio delta as base64 to WebSocket clients
        audio_data = getattr(event, "delta", None)
        if audio_data:
            audio_b64 = base64.b64encode(audio_data).decode("utf-8")
            _broadcast({"type": "audio", "audio": audio_b64})

    async def _handle_audio_done(self):
        """Assistant finished speaking."""
        self._response_cancelled = False
        self.state_callback("ready", "Assistant finished. You can speak again.")

    async def _handle_error(self, event):
        """Handle Voice Live errors."""
        error = getattr(event, "error", None)
        message = getattr(error, "message", "Unknown error") if error else "Unknown error"
        self.state_callback("error", f"Error: {message}")

    def request_stop(self):
        self._stopping = True
    ```

1. **Ctrl + s** キーを入力して変更を保存します。次のセクションでも使用するため、エディターは開いたままにしておきます。

### アプリのコードを確認する

これまで、エージェントを実装してエージェント イベントを処理するコードをアプリに追加しました。 アプリがクライアントの状態と操作をどのように処理しているかをより深く理解するために、数分をかけてコード全体とコメントを確認してください。

1. 完了したら、**Ctrl+ q** キーを入力してエディターを終了します。 

## デプロイ スクリプトを更新して実行する

このセクションでは、**azdeploy.sh** デプロイ スクリプトに小さな変更を加えて、デプロイを実行します。 

### デプロイ スクリプトを更新する

**azdeploy.sh** デプロイ スクリプトの先頭で変更する必要がある値は 2 つだけです。 

* **rg** 値は、デプロイを含むリソース グループを指定します。 既定値をそのまま使用するか、特定のリソース グループにデプロイする必要がある場合は独自の値を入力することができます。

* **location** 値は、デプロイのリージョンを設定します。 演習で使用する *gpt-4o* モデルを他のリージョンにデプロイすることはできますが、特定のリージョンでは制限が存在する場合があります。 選択したリージョンでデプロイが失敗した場合は、**eastus2** または **swedencentral**を試してください。 

    ```
    rg="rg-voicelive" # Replace with your resource group
    location="eastus2" # Or a location near you
    ```

1. Cloud Shell で次のコマンドを実行して、デプロイ スクリプトの編集を開始します。

    ```bash
    cd ~/01-voice-live-web
    ```
    
    ```bash
    code azdeploy.sh
    ```

1. ニーズに合わせて **rg** と **location** の値を更新し、**Ctrl + s** キーを入力して変更を保存し、**Ctrl + q** キーを入力してエディターを終了します。

### 展開スクリプトを実行する

デプロイ スクリプトは、AI モデルをデプロイし、App Service でコンテナー化されたアプリを実行するために必要なリソースを Azure に作成します。

1. Cloud Shell で次のコマンドを実行して、Azure リソースとアプリケーションのデプロイを開始します。

    ```bash
    bash azdeploy.sh
    ```

1. 初期デプロイの場合は、**オプション 1** を選択します。

    デプロイは 5 分から 10 分で完了します。 デプロイ中に、次の情報またはアクションを求められる場合があります。
    
    * Azure に対する認証を求められた場合は、表示される指示に従います。
    * サブスクリプションを選択するように求められた場合は、方向キーを使用してサブスクリプションを強調表示し、**Enter** キーを押します。 
    * デプロイ中にいくつかの警告が表示される可能性がありますが、これらは無視できます。
    * AI モデルのデプロイ中にデプロイが失敗した場合は、デプロイ スクリプトのリージョンを変更して、もう一度試してください。 
    * Azure のリージョンは時々ビジー状態になり、デプロイのタイミングが中断されることがあります。 モデルのデプロイ後にデプロイが失敗した場合は、デプロイ スクリプトを再実行します。

## アプリの表示とテスト

デプロイが完了したら、"Deployment complete!"  メッセージが、Web アプリへのリンクと共にシェル内に表示されます。 そのリンクを選択するか、App Service リソースに移動してそこからアプリを起動できます。 アプリケーションの読み込みには数分かかる場合があります。 

1. **[セッションの開始]** ボタンを選択して、モデルに接続します。
1. オーディオ デバイスへのアクセス権をアプリケーションに付与するように求められます。
1. アプリから話し始めるように指示されたら、モデルに話しかけます。

トラブルシューティング:

* アプリから環境変数の不足が報告された場合は、App Service でアプリケーションを再起動します。
* アプリケーションに表示されるログに過剰な "オーディオ チャンク" メッセージが表示された場合は、**[セッションの停止]** を選択し、セッションをもう一度開始します。** 
* アプリがまったく機能しない場合は、すべてのコードを追加したこと、およびインデントが適切であるかどうかを確認します。 変更を加える必要がある場合は、デプロイを再実行し、**オプション 2** を選択してイメージのみを更新します。

## リソースをクリーンアップする

Cloud Shell で次のコマンドを実行して、この演習用にデプロイしたすべてのリソースを削除します。 リソースの削除を確認するメッセージが表示されます。

```
azd down --purge
```
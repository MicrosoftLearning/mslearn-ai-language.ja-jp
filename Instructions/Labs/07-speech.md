---
lab:
  title: 音声の認識と合成
  description: 音声テキスト変換およびテキスト読み上げを行うスピーキング クロックを実装します。
---

# 音声の認識と合成

**Azure AI 音声**は、次のような音声関連機能を提供するサービスです。

- 音声認識 (音声の話し言葉をテキストに変換する) を実装できるようにする *speech-to-text* API。
- 音声合成 (テキストを可聴音声に変換する) を実装できるようにする*text-to-speech* API。

この演習では、これらの API の両方を使用して、スピーキング クロック アプリケーションを実装します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用して音声アプリケーションを開発できます。

- [Azure AI Speech SDK for Python](https://pypi.org/project/azure-cognitiveservices-speech/)
- [Azure AI Speech SDK for .NET](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech)
- [Azure AI Speech SDK for JavaScript](https://www.npmjs.com/package/microsoft-cognitiveservices-speech-sdk)

この演習は約 **30** 分かかります。

> **注** この演習は、コンピューターのサウンド ハードウェアへの直接アクセスがサポートされていない Azure Cloud Shell で完了するように設計されています。 そのため、ラボでは音声入力ストリームと出力ストリームにオーディオ ファイルが使用されます。 マイクとスピーカーを使用して同じ結果を得るためのコードが参照用に用意されています。

## "Azure AI 音声" リソースを作成する

まず、Azure AI 音声リソースを作成します。

1. [Azure portal](https://portal.azure.com) (`https://portal.azure.com`) を開き、お使いの Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部の検索フィールドで、**音声サービス**を検索します。 一覧からそれを選択し、**[作成]** を選択します。
1. 次の設定を使用してリソースをプロビジョニングします。
    - **[サブスクリプション]**: *お使いの Azure サブスクリプション*。
    - **リソース グループ**: *リソース グループを選択または作成します*。
    - **[リージョン]**: *使用できるリージョンを選択します*。
    - **[名前]**: *一意の名前を入力します*。
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[リソース管理]** セクションで、**[キーとエンドポイント]** ページを表示します。 このページの情報は、演習の後半で必要になります。

## スピーキング クロック アプリを準備して構成する

1. **[キーとエンドポイント]** ページを開いたまま、ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal に新しい Cloud Shell を作成し、***PowerShell*** 環境を選択します。 Azure portal の下部にあるペインに、Cloud Shell のコマンド ライン インターフェイスが表示されます。

    > **注**: *Bash* 環境を使用するクラウド シェルを以前に作成した場合は、それを ***PowerShell*** に切り替えます。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

    **<font color="red">続行する前に、クラシック バージョンの Cloud Shell に切り替えたことを確認します。</font>**

1. PowerShell ペインで、次のコマンドを入力して、この演習用の GitHub リポジトリを複製します。

    ```
   rm -r mslearn-ai-language -f
   git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **ヒント**: Cloud Shell にコマンドを入力すると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。

1. リポジトリが複製されたら、スピーキング クロック アプリケーション コード ファイルを含むフォルダーに移動します。  

    ```
   cd mslearn-ai-language/Labfiles/07-speech/Python/speaking-clock
    ```

1. コマンド ライン ペインで次のコマンドを実行して、**speaking-clock** フォルダー内のコード ファイルを表示します。

    ```
   ls -a -l
    ```

    これらのファイルとしては、構成ファイル (**.env**) とコード ファイル (**speaking-clock.py**) があります。 アプリケーションで使用するオーディオ ファイルは、**audio** サブフォルダー内にあります。

1. 次のコマンドを実行して、Python 仮想環境を作成し、Azure AI Speech SDK パッケージとその他の必要なパッケージをインストールします。

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-cognitiveservices-speech==1.42.0
    ```

1. 次のコマンドを入力して、構成ファイルを編集します。

    ```
   code .env
    ```

    このファイルをコード エディターで開きます。

1. 作成した Azure AI 音声リソースの**リージョン**と**キー** (Azure portal の Azure AI 翻訳リソースの **[キーとエンドポイント]** ページで入手可能) を含めるように構成値を更新します。
1. プレースホルダーを置き換えたら、**Ctrl + S** キー コマンドを使用して変更を保存してから、**Ctrl + Q** キー コマンドを使用して、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

## Azure AI 音声 SDK を使用するコードを追加する

> **ヒント**: コードを追加する際は、必ず正しいインデントを維持してください。

1. 次のコマンドを入力して、提供されているコード ファイルを編集します。

    ```
   code speaking-clock.py
    ```

1. コード ファイルの上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Azure AI 音声 SDK を使用するために必要な名前空間をインポートします。

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   import azure.cognitiveservices.speech as speech_sdk
    ```

1. **main** 関数では、**Get config settings** というコメントの下にあるコードで、構成ファイルで定義したキーとリージョンが読み込まれることに注意してください。

1. **Configure speech service** というコメントを見つけて、AI サービス キーとリージョンを使用して Azure AI サービス音声エンドポイントへの接続を構成する次のコードを追加します。

    ```python
   # Configure speech service
   speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
   print('Ready to use speech service in:', speech_config.region)
    ```

1. 変更を保存しますが (*CTRL + S*)、コード エディターは開いたままにします。

## アプリを実行する

ここまで、アプリは、Azure AI 音声サービスに接続する以外には何も行いませんが、音声機能を追加する前にアプリを実行して動作することを確認すると有用です。

1. コマンド ラインで、次のコマンドを入力して、スピーキング クロック アプリを実行します。

    ```
   python speaking-clock.py
    ```

    コードは、アプリケーションが使用する音声サービスリソースの領域を表示する必要があります。 実行の成功は、アプリが Azure AI 音声リソースに接続されたことを示します。

## 音声を認識するコードを追加する

プロジェクトの Azure AI 音声リソースに音声サービス用の **SpeechConfig** があるので、**音声テキスト変換** API を使用して音声を認識し、文字起こしすることができます。

この手順では、音声入力がオーディオ ファイルからキャプチャされ、ここで再生できます。

<video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/Time.mp4" title="今何時?" width="150"></video>

1. コード ファイルでは、コードで **TranscribeCommand** 関数を使用して音声入力を受け入れることに注意してください。 次に、**TranscribeCommand** 関数で、**Configure speech recognition** というコメントを見つけ、その下に適切なコードを追加して、オーディオ ファイルの音声を認識して文字起こしするために使用できる **SpeechRecognizer** クライアントを作成します。

    ```python
   # Configure speech recognition
   current_dir = os.getcwd()
   audioFile = current_dir + '/time.wav'
   audio_config = speech_sdk.AudioConfig(filename=audioFile)
   speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    ```

1. **TranscribeCommand** 関数のコメント **「Process speech input」** の下に、音声入力をリッスンする次のコードを追加します。コマンドを返す関数の最後にあるコードを置き換えないように注意してください。

    ```python
   # Process speech input
   print("Listening...")
   speech = speech_recognizer.recognize_once_async().get()
   if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
   else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)
    ```

1. 変更を保存し (*Ctrl + S* キー)、コード エディターの下のコマンド ラインで、プログラムを実行します。
1. 出力を確認します。オーディオ ファイルの音声が正常に "聞こえて"、適切な応答が返されます (Azure Cloud Shell が別のタイム ゾーンにあるサーバーで実行されている可能性があることに注意してください)。

    > **ヒント**: SpeechRecognizer でエラーが発生した場合は、"Cancelled" の結果が生成されます。 アプリケーションのコードは、エラーメッセージを表示します。 最も可能性の高い原因は、構成ファイルのリージョンの値が正しくないことです。

## 音声を合成する

speaking clock アプリケーションは話し言葉の入力を受け入れますが、実際には話しません。 音声合成用のコードを追加して修正しましょう。

Cloud Shell のハードウェアの制限があるため、もう一度合成された音声出力をファイルに転送します。

1. コード ファイルでは、コードで **TellTime** 関数を使用してユーザーに現在の時刻を通知することに注意してください。
1. **TellTime** 関数のコメント **「Configure speech synthesis」** の下に、次のコードを追加して、音声出力の生成に使用できる **SpeechSynthesizer** クライアントを作成します。

    ```python
   # Configure speech synthesis
   output_file = "output.wav"
   speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
   audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config,)
    ```

1. **TellTime** 関数のコメント **「Synthesize spoken output」** の下に、次のコードを追加して音声出力を生成します。応答を出力する関数の最後にあるコードを置き換えないように注意してください。

    ```python
   # Synthesize spoken output
   speak = speech_synthesizer.speak_text_async(response_text).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
   else:
        print("Spoken output saved in " + output_file)
    ```

1. 変更を保存し (*Ctrl + S* キー)、プログラムを再実行します。音声出力がファイルに保存されたことが示されます。

1. .wav オーディオ ファイルを再生できるメディア プレーヤーを使用する場合は、次のコマンドを入力して、生成されたファイルをダウンロードします。

    ```
   download ./output.wav
    ```

    ダウンロード コマンドを実行すると、ブラウザーの右下にポップアップ リンクが作成され、ここからファイルをダウンロードして開くことができます。

    ファイルは次のようになるはずです。

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/Output.mp4" title="時刻は 2:15 です。" width="150"></video>

## 音声合成マークアップ言語を使用する

音声合成アップ言語 (SSML) を使用すると、XML ベースの形式を使用して音声を合成する方法をカスタマイズできます。

1. **TellTime** 関数で、コメント **「Synthesize spoken output」** の下にある現在のすべてのコードを次のコードに置き換えます (コメント **Print the response** の下にコードを残します)。

    ```python
   # Synthesize spoken output
   responseSsml = " \
       <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
           <voice name='en-GB-LibbyNeural'> \
               {} \
               <break strength='weak'/> \
               Time to end this lab! \
           </voice> \
       </speak>".format(response_text)
   speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
       print(speak.reason)
   else:
       print("Spoken output saved in " + output_file)
    ```

1. 変更を保存し、プログラムを再実行します。音声出力がファイルに保存されたことが示されます。
1. 生成されたファイルをダウンロードして再生します。次のように聞こえます。
    
    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/Output2.mp4" title="時刻は 5:30 です。 このラボの終了時間です。" width="150"></video>

## (省略可能) マイクとスピーカーを使用する場合

この演習では、音声の入力と出力にオーディオ ファイルを使用しました。 オーディオ ハードウェアを使用するようにコードを変更する方法を見てみましょう。

### マイクによる音声認識の使用

マイクがある場合は、次のコードを使用して音声認識用の音声入力をキャプチャできます。

```python
# Configure speech recognition
audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
print('Speak now...')

# Process speech input
speech = speech_recognizer.recognize_once_async().get()
if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
    command = speech.text
    print(command)
else:
    print(speech.reason)
    if speech.reason == speech_sdk.ResultReason.Canceled:
        cancellation = speech.cancellation_details
        print(cancellation.reason)
        print(cancellation.error_details)

```

> **注**: システムの既定のマイクは既定のオーディオ入力であるため、AudioConfig を完全に省略することもできます。

### スピーカーによる音声合成の使用

スピーカーがある場合は、次のコードを使用して音声を合成できます。

```python
response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)

# Configure speech synthesis
speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)

# Synthesize spoken output
speak = speech_synthesizer.speak_text_async(response_text).get()
if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print(speak.reason)
```

> **注**: システムの既定のスピーカーは既定のオーディオ出力であるため、AudioConfig を完全に省略することもできます。

## クリーンアップ

Azure AI Speech の探索が終わったら、不要な Azure コストが発生しないように、この演習で作成したリソースを削除する必要があります。

1. Azure Cloud Shell ペインを閉じます。
1. Azure portal で、このラボで作成した Azure AI 音声リソースを参照します。
1. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細

**Speech-to-text** および **Text-to-speech** API の使用の詳細については、[Speech-to-text ドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text)および [Text-to-speech ドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech)を参照してください。

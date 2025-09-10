---
lab:
  title: 音声の翻訳
  description: 言語を音声間で翻訳し、独自のアプリを実装します。
---

# 音声の翻訳

Azure AI 音声には、話し言葉の翻訳に使用できる Speech Translation API が含まれています。 たとえば、現地の言語を話さない場所を旅行するときに使用できる翻訳アプリケーションを開発するとします。 「駅はどこですか?」のようなフレーズを言ったり、 または、「薬局を見つける必要があります」を独自の言語で言ったり、それを現地の言語に翻訳することができます。 この演習では、Azure AI Speech SDK for Python を使用して、この例に基づいて簡単なアプリケーションを作成します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用して音声翻訳アプリケーションを開発できます。

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

## Cloud Shell でアプリを開発する準備をする

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

1. リポジトリがクローンされたら、コード ファイルが格納されているフォルダーに移動します。

    ```
   cd mslearn-ai-language/Labfiles/08-speech-translation/Python/translator
    ```

1. コマンド ライン ペインで次のコマンドを実行して、**translator** フォルダー内のコード ファイルを表示します。

    ```
   ls -a -l
    ```

    これらのファイルとしては、構成ファイル (**.env**) とコード ファイル (**translator.py**) があります。

1. 次のコマンドを実行して、Python 仮想環境を作成し、Azure AI Speech SDK パッケージとその他の必要なパッケージをインストールします。

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-cognitiveservices-speech==1.42.0
    ```

1. 次のコマンドを入力して、提供されている構成ファイルを編集します。

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
   code translator.py
    ```

1. コード ファイルの上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Azure AI 音声 SDK を使用するために必要な名前空間をインポートします。

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   import azure.cognitiveservices.speech as speech_sdk
    ```

1. **main** 関数では、**Get config settings** というコメントの下にあるコードで、構成ファイルで定義したキーとリージョンが読み込まれることに注意してください。

1. **Configure translation** というコメントの下にある次のコードを見つけて、Azure AI サービス音声エンドポイントへの接続を構成する次のコードを追加します。

    ```python
   # Configure translation
   translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
   translation_config.speech_recognition_language = 'en-US'
   translation_config.add_target_language('fr')
   translation_config.add_target_language('es')
   translation_config.add_target_language('hi')
   print('Ready to translate from',translation_config.speech_recognition_language)
    ```

1. **SpeechTranslationConfig** を使用して音声をテキストに翻訳しますが、**SpeechConfig** を使用して翻訳を音声に合成します。 コメント **「Configure speech」** の下に次のコードを追加します。

    ```python
   # Configure speech
   speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
   print('Ready to use speech service in:', speech_config.region)
    ```

1. 変更を保存しますが (*CTRL + S*)、コード エディターは開いたままにします。

## アプリを実行する

ここまで、アプリは、Azure AI 音声リソースに接続する以外には何も行いませんが、音声機能を追加する前にアプリを実行して動作することを確認すると有用です。

1. コマンド ラインで、次のコマンドを入力して翻訳アプリを実行します。

    ```
   python translator.py
    ```

    コードによって、アプリケーションで使用される音声サービス リソースのリージョンと、en-US から翻訳する準備ができたことを示すメッセージが表示され、ターゲット言語の入力を求められます。 実行の成功は、アプリが Azure AI 音声サービスに接続されたことを示します。 ENTER を押してプログラムを終了します。

## 音声翻訳の実装

Azure AI 音声サービス用の **SpeechTranslationConfig** が用意されたので、Azure AI 音声翻訳 API を使用して音声を認識および翻訳できます。

1. コード ファイルでは、コードで **Translate** 関数を使用して音声入力を翻訳することに注意してください。 **Translate** 関数のコメント **「Translate speech」** の下に、次のコードを追加して、ファイルからの音声を認識して、翻訳するために使用できる **TranslationRecognizer** クライアントを作成します。

    ```python
   # Translate speech
   current_dir = os.getcwd()
   audioFile = current_dir + '/station.wav'
   audio_config_in = speech_sdk.AudioConfig(filename=audioFile)
   translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config_in)
   print("Getting speech from file...")
   result = translator.recognize_once_async().get()
   print('Translating "{}"'.format(result.text))
   translation = result.translations[targetLanguage]
   print(translation)
    ```

1. 変更を保存し (*Ctrl + S* キー)、プログラムを再実行します。

    ```
   python translator.py
    ```

1. メッセージが表示されたら、有効な言語コード (*fr*、*es*、または *hi*) を入力します。 プログラムは、入力ファイルを文字起こしし、指定した言語 (フランス語、スペイン語、またはヒンディー語) に翻訳します。 このプロセスを繰り返し、アプリケーションでサポートされている各言語を試してください。

    > **注**:文字エンコードの問題により、ヒンディー語への翻訳がコンソール ウィンドウに正しく表示されない場合があります。

1. 終了したら、Enter キーを押してプログラムを終了します。

> **メモ**: アプリケーションのコードは、1 回の呼び出しで入力を 3 つの言語すべてに翻訳します。 特定の言語の翻訳のみが表示されますが、結果の **translations** コレクションでターゲット言語コードを指定することにより、任意の翻訳を取得できます。

## 翻訳を音声に合成する

これまでのところ、アプリケーションは音声入力をテキストに翻訳します。旅行中に誰かに助けを求める必要がある場合は、これで十分かもしれません。 ただし、適切な声で翻訳を声に出して話してもらう方がよいでしょう。

> **注**:Cloud Shell のハードウェア制限があるため、合成された音声出力をファイルに転送します。

1. **Translate** 関数で、**Synthesize translation** というコメントを見つけて、**SpeechSynthesizer** を使用して翻訳を音声として合成し、それを .wav ファイルに保存する次のコードを追加します。

    ```python
   # Synthesize translation
   output_file = "output.wav"
   voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
   }
   speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
   audio_config_out = speech_sdk.audio.AudioConfig(filename=output_file)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
   speak = speech_synthesizer.speak_text_async(translation).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
   else:
        print("Spoken output saved in " + output_file)
    ```

1. 変更を保存し (*Ctrl + S* キー)、プログラムを再実行します。

    ```
   python translator.py
    ```

1. アプリケーションからの出力を確認します。音声出力の翻訳がファイルに保存されたことが示されています。 終了したら、**Enter** キーを押してプログラムを終了します。
1. .wav オーディオ ファイルを再生できるメディア プレーヤーを使用する場合は、次のコマンドを入力して、生成されたファイルをダウンロードします。

    ```
   download ./output.wav
    ```

    ダウンロード コマンドを実行すると、ブラウザーの右下にポップアップ リンクが作成され、ここからファイルをダウンロードして開くことができます。

> **注**
> "この例では、**SpeechTranslationConfig** を使用して音声をテキストに翻訳し、**SpeechConfig** を使用して翻訳を音声として合成しました。*実際には、**SpeechTranslationConfig** を使用して翻訳を直接合成できますが、これは単一の言語に翻訳する場合にのみ機能するため、通常はファイルとして保存されるオーディオ ストリームになります。"*

## リソースをクリーンアップする

Azure AI 音声サービスを調べ終えたら、この演習で作成したリソースを削除できます。 方法は以下のとおりです。

1. Azure Cloud Shell ペインを閉じます。
1. Azure portal で、このラボで作成した Azure AI 音声リソースを参照します。
1. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## マイクとスピーカーがある場合

この演習では、音声の入力と出力にオーディオ ファイルを使用しました。 オーディオ ハードウェアを使用するようにコードを変更する方法を見てみましょう。

### マイクでの音声翻訳の使用

1. マイクを使用する場合は、次のコードを使用して音声翻訳用の音声入力をキャプチャできます。

    ```python
   # Translate speech
   audio_config_in = speech_sdk.AudioConfig(use_default_microphone=True)
   translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config_in)
   print("Speak now...")
   result = translator.recognize_once_async().get()
   print('Translating "{}"'.format(result.text))
   translation = result.translations[targetLanguage]
   print(translation)
    ```

> **注**: システムの既定のマイクは既定のオーディオ入力であるため、AudioConfig を完全に省略することもできます。

### スピーカーによる音声合成の使用

1. スピーカーがある場合は、次のコードを使用して音声を合成できます。
    
    ```python
   # Synthesize translation
   voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
   }
   speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
   audio_config_out = speech_sdk.audio.AudioConfig(use_default_speaker=True)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
   speak = speech_synthesizer.speak_text_async(translation).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    ```

> **注**: システムの既定のスピーカーは既定のオーディオ出力であるため、AudioConfig を完全に省略することもできます。

## 詳細

Azure AI 音声翻訳 API の使用の詳細については、「[音声翻訳のドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation)」をご覧ください。

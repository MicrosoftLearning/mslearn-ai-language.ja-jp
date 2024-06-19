---
lab:
  title: 音声の認識と合成
  module: Module 4 - Create speech-enabled apps with Azure AI services
---

# 音声の認識と合成

**Azure AI 音声**は、次のような音声関連機能を提供するサービスです。

- 音声認識 (音声の話し言葉をテキストに変換する) を実装できるようにする *speech-to-text* API。
- 音声合成 (テキストを可聴音声に変換する) を実装できるようにする*text-to-speech* API。

この演習では、これらの API の両方を使用して、スピーキング クロック アプリケーションを実装します。

> **注** この演習では、スピーカーやヘッドフォンを備えたコンピューターを使用している必要があります。 最良のエクスペリエンスのため、マイクも必要です。 一部のホストされる仮想環境では、ローカル マイクから音声をキャプチャできる場合があります。しかし、これが機能しない場合 (または、マイクがない場合)、音声入力用に付属の音声ファイルを使用できます。 マイクまたは音声ファイルを使用するかどうかに応じて、ことなるオプションを選択する必要があるろきは、慎重に手順に従ってください。

## *Azure AI 音声*リソースをプロビジョニングする

サブスクリプションにまだない場合は、**Azure AI 音声**リソースをプロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部の検索フィールドで、「**Azure AI サービス**」を検索して **Enter** キーを押し、結果の **[スピーチ サービス]** の下にある **[作成]** を選択します。
1. 次の設定を使ってリソースを作成します。
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **[リソース グループ]**: *リソース グループを作成または選択します*
    - **[リージョン]**: *使用できるリージョンを選択します*
    - **[名前]**: *一意の名前を入力します*
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **責任ある AI 通知**: 同意。
1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## Visual Studio Code でアプリの開発準備をする

Visual Studio Code を使用して音声アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

> **ヒント**: mslearn-ai-language** リポジトリを**既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
1. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
1. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。

    > **注**:Visual Studio Code に、開いているコードを信頼するかどうかを求めるポップアップ メッセージが表示された場合は、ポップアップの **[はい、作成者を信頼します]** オプションをクリックします。

1. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるプロンプトが表示された場合は、**[今はしない]** を選択します。

## アプリケーションを構成する

C# と Python の両方のアプリケーションが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI 音声リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/07-speech** フォルダーを参照し、言語の設定とそこに含まれている **speaking-clock** フォルダーに応じて **CSharp** または **Python** フォルダーを展開します。 各フォルダーには、Azure AI 音声機能を統合するアプリの言語固有のコード ファイルが含まれています。
1. コード ファイルを含んだ **speaking-clock** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適したコマンドを実行して、Azure AI 音声 SDK パッケージをインストールします。

    **C#**

    ```
    dotnet add package Microsoft.CognitiveServices.Speech --version 1.30.0
    ```

    **Python**

    ```
    pip install azure-cognitiveservices-speech==1.30.0
    ```

1. **[エクスプローラー]** ペインの **speaking-clock** フォルダーで、優先する言語の構成ファイルを開きます。

    - **C#**: appsettings.json
    - **Python**: .env

1. 作成した Azure AI 音声リソースの**リージョン**と**キー**を含むように構成値を更新します (リージョンとキーは、Azure portal の Azure AI 音声リソースの **[キーとエンドポイント]** ページで入手できます)。

    > **注**: エンドポイントでは<u>なく</u>、必ずリソースの*リージョン*を追加してください。

1. 構成ファイルを保存します。

## Azure AI 音声 SDK を使用するコードを追加する

1. **speaking-clock** フォルダーには、クライアント アプリケーションのコード ファイルが含まれていることに注意してください。

    - **C#** : Program.cs
    - **Python**: speaking-clock.py

    コード ファイルを開き、上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Azure AI 音声 SDK を使用するために必要な名前空間をインポートします。

    **C#** : Program.cs

    ```csharp
    // Import namespaces
    using Microsoft.CognitiveServices.Speech;
    using Microsoft.CognitiveServices.Speech.Audio;
    ```

    **Python**: speaking-clock.py

    ```python
    # Import namespaces
    import azure.cognitiveservices.speech as speech_sdk
    ```

1. **Main** 関数では、構成ファイルからサービスのキーとリージョンをロードするコードがすでに用意されていることに注意してください。 Azure AI 音声リソースの **SpeechConfig** を作成するには、これらの変数を使用する必要があります。 コメント **「Configure speech service」** の下に次のコードを追加します。

    **C#** : Program.cs

    ```csharp
    // Configure speech service
    speechConfig = SpeechConfig.FromSubscription(aiSvcKey, aiSvcRegion);
    Console.WriteLine("Ready to use speech service in " + speechConfig.Region);
    
    // Configure voice
    speechConfig.SpeechSynthesisVoiceName = "en-US-AriaNeural";
    ```

    **Python**: speaking-clock.py

    ```python
    # Configure speech service
    speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
    print('Ready to use speech service in:', speech_config.region)
    ```

1. 変更を保存して、**speaking-clock** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python speaking-clock.py
    ```

1. C# を使用している場合は、非同期メソッドで **await** 演算子を使用することに関する警告を無視できます。これは後で修正します。 コードは、アプリケーションが使用する音声サービスリソースの領域を表示する必要があります。

## 音声を認識するコードを追加する

Azure AI 音声リソースにスピーチ サービス用の **SpeechConfig** ができたので、**音声テキスト変換** API を使用して音声を認識し、テキストに文字起こしすることができます。

> **重要**: このセクションには、2 つの代替手順の手順が含まれています。 マイクが動作している場合は、最初の手順に従います。 オーディオ ファイルを使用して音声入力をシミュレートする場合は、2 番目の手順に従います。

### マイクが機能する場合

1. プログラムの **Main** 関数で、コードが **TranscribeCommand** 関数を使用して音声入力を受け入れることに注意してください。
1. **TranscribeCommand** 関数のコメント **「Configure speech recognition」** の下に、次のコードを追加して、入力用のデフォルトのシステムマイクを使用して音声を認識および転写するために使用できる **SpeechRecognizer** クライアントを作成します。

    **C#**

    ```csharp
    // Configure speech recognition
    using AudioConfig audioConfig = AudioConfig.FromDefaultMicrophoneInput();
    using SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
    Console.WriteLine("Speak now...");
    ```

    **Python**

    ```python
    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')
    ```

1. 以下の「**コードを追加して書き起こしたマンドを処理する**」のセクションにスキップします。

---

### または、ファイルからの音声入力を使用します

1. ターミナル ウィンドウで、次のコマンドを入力して、音声ファイルの再生に使用できるライブラリをインストールします。

    **C#**

    ```
    dotnet add package System.Windows.Extensions --version 4.6.0 
    ```

    **Python**

    ```
    pip install playsound==1.2.2
    ```

1. プログラムのコード ファイルで、既存の名前空間のインポートの下に、次のコードを追加して、インストールしたライブラリをインポートします。

    **C#** : Program.cs

    ```csharp
    using System.Media;
    ```

    **Python**: speaking-clock.py

    ```python
    from playsound import playsound
    ```

1. **Main** 関数で、コードが **TranscribeCommand** 関数を使用して音声入力を受け入れることに注意してください。 **TranscribeCommand** 関数のコメント **「Configure speech recognition」** の下に、適切なコードを追加して、音声ファイルからの音声を認識して、書き起こすために使用できる **SpeechRecognizer** クライアントを作成します。

    **C#** : Program.cs

    ```csharp
    // Configure speech recognition
    string audioFile = "time.wav";
    SoundPlayer wavPlayer = new SoundPlayer(audioFile);
    wavPlayer.Play();
    using AudioConfig audioConfig = AudioConfig.FromWavFileInput(audioFile);
    using SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
    ```

    **Python**: speaking-clock.py

    ```python
    # Configure speech recognition
    current_dir = os.getcwd()
    audioFile = current_dir + '\\time.wav'
    playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    ```

---

### コードを追加して書き起こしたコマンドを処理する

1. **TranscribeCommand** 関数のコメント **「Process speech input」** の下に、音声入力をリッスンする次のコードを追加します。コマンドを返す関数の最後にあるコードを置き換えないように注意してください。

    **C#** : Program.cs

    ```csharp
    // Process speech input
    SpeechRecognitionResult speech = await speechRecognizer.RecognizeOnceAsync();
    if (speech.Reason == ResultReason.RecognizedSpeech)
    {
        command = speech.Text;
        Console.WriteLine(command);
    }
    else
    {
        Console.WriteLine(speech.Reason);
        if (speech.Reason == ResultReason.Canceled)
        {
            var cancellation = CancellationDetails.FromResult(speech);
            Console.WriteLine(cancellation.Reason);
            Console.WriteLine(cancellation.ErrorDetails);
        }
    }
    ```

    **Python**: speaking-clock.py

    ```python
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

1. 変更を保存して、**speaking-clock** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python speaking-clock.py
    ```

1. マイクを使用している場合、明瞭に話、"what time is it?" と言ってください。 プログラムは、音声入力を書き起こし、時刻を表示する必要があります (コードが実行されているコンピューターの現地時間に基づいており、現在の時刻とは異なる場合があります)。

    SpeechRecognizer を使用すると、約 5 秒で話すことができます。 音声入力が検出されない場合は、[一致なし] の結果が生成されます。

    SpeechRecognizer でエラーが発生した場合は、"Cancelled" の結果が生成されます。 アプリケーションのコードは、エラーメッセージを表示します。 最も可能性の高い原因は、構成ファイルのキーまたはリージョンが正しくないことです。

## 音声を合成する

speaking clock アプリケーションは話し言葉の入力を受け入れますが、実際には話しません。 音声合成用のコードを追加して修正しましょう。

1. プログラムの **Main** 関数で、コードが **TellTime** 関数を使用してユーザーに現在の時刻を通知することに注意してください。
1. **TellTime** 関数のコメント **「Configure speech synthesis」** の下に、次のコードを追加して、音声出力の生成に使用できる **SpeechSynthesizer** クライアントを作成します。

    **C#** : Program.cs

    ```csharp
    // Configure speech synthesis
    speechConfig.SpeechSynthesisVoiceName = "en-GB-RyanNeural";
    using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig);
    ```

    **Python**: speaking-clock.py

    ```python
    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    ```

    > **メモ** 既定のオーディオ構成では、出力に既定のシステム オーディオ デバイスが使用されるので、**AudioConfig** を明示的に指定する必要はありません。 オーディオ出力をファイルにリダイレクトする必要がある場合は、ファイルパスと **AudioConfig** を使用します。

1. **TellTime** 関数のコメント **「Synthesize spoken output」** の下に、次のコードを追加して音声出力を生成します。応答を出力する関数の最後にあるコードを置き換えないように注意してください。

    **C#** : Program.cs

    ```csharp
    // Synthesize spoken output
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(responseText);
    if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
    {
        Console.WriteLine(speak.Reason);
    }
    ```

    **Python**: speaking-clock.py

    ```python
    # Synthesize spoken output
    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    ```

1. 変更を保存して、**speaking-clock** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python speaking-clock.py
    ```

1. プロンプトが表示されたら、マイクに向かってはっきりと話し、"what time is it?" と言います。 プログラムが時間を教えくれるはずです。

## 別の音声を使用する

speaking clock アプリケーションは、変更可能なデフォルトの音声を使用します。 Speech サービスは、さまざまな*標準*音声だけでなく、より人間らしい*ニューラル*音声もサポートします。 *カスタム* ボイスを作成することもできます。

> **メモ**: ニューラル音声と標準音声の一覧については、Speech Studio の[音声ギャラリー](https://speech.microsoft.com/portal/voicegallery)をご覧ください。

1. **TellTime** 関数のコメント **「Configure speech synthesis」** で、**SpeechSynthesizer** クライアントを作成する前に、次のようにコードを変更して代替音声を指定します。

   **C#** : Program.cs

    ```csharp
    // Configure speech synthesis
    speechConfig.SpeechSynthesisVoiceName = "en-GB-LibbyNeural"; // change this
    using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig);
    ```

    **Python**: speaking-clock.py

    ```python
    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = 'en-GB-LibbyNeural' # change this
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    ```

1. 変更を保存して、**speaking-clock** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python speaking-clock.py
    ```

1. プロンプトが表示されたら、マイクに向かってはっきりと話し、"何時ですか?" と言います。 プログラムは指定された声で話し、時間を伝えます。

## 音声合成マークアップ言語を使用する

音声合成アップ言語 (SSML) を使用すると、XML ベースの形式を使用して音声を合成する方法をカスタマイズできます。

1. **TellTime** 関数で、コメント **「Synthesize spoken output」** の下にある現在のすべてのコードを次のコードに置き換えます (コメント **Print the response** の下にコードを残します)。

   **C#** : Program.cs

    ```csharp
    // Synthesize spoken output
    string responseSsml = $@"
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='en-GB-LibbyNeural'>
                {responseText}
                <break strength='weak'/>
                Time to end this lab!
            </voice>
        </speak>";
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakSsmlAsync(responseSsml);
    if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
    {
        Console.WriteLine(speak.Reason);
    }
    ```

    **Python**: speaking-clock.py

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
    ```

1. 変更を保存して、**speaking-clock** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python speaking-clock.py
    ```

1. プロンプトが表示されたら、マイクに向かってはっきりと話し、"何時ですか?" と言います。 プログラムは、SSML で指定された音声 (SpeechConfig で指定された音声を上書き) で時間を通知し、一時停止した後、このラボを終了する時間であることを伝えます。

## 詳細

**Speech-to-text** および **Text-to-speech** API の使用の詳細については、[Speech-to-text ドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text)および [Text-to-speech ドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech)を参照してください。

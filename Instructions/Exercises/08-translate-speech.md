---
lab:
  title: 音声の翻訳
  module: Module 8 - Translate speech with Azure AI Speech
---

# 音声の翻訳

Azure AI 音声には、話し言葉の翻訳に使用できる Speech Translation API が含まれています。 たとえば、現地の言語を話さない場所を旅行するときに使用できる翻訳アプリケーションを開発するとします。 「駅はどこですか?」のようなフレーズを言ったり、 または、「薬局を見つける必要があります」を独自の言語で言ったり、それを現地の言語に翻訳することができます。

> **注** この演習では、スピーカーやヘッドフォンを備えたコンピューターを使用している必要があります。 最良のエクスペリエンスのため、マイクも必要です。 一部のホストされる仮想環境では、ローカル マイクから音声をキャプチャできる場合があります。しかし、これが機能しない場合 (または、マイクがない場合)、音声入力用に付属の音声ファイルを使用できます。 マイクまたは音声ファイルを使用するかどうかに応じて、ことなるオプションを選択する必要があるろきは、慎重に手順に従ってください。

## *Azure AI 音声*リソースをプロビジョニングする

サブスクリプションにまだない場合は、**Azure AI 音声**リソースをプロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部の検索フィールドで、「**Azure AI サービス**」を検索して **Enter** キーを押し、結果の **[スピーチ サービス]** の下にある **[作成]** を選択します。
1. 次の設定を使ってリソースを作成します。
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **[リソース グループ]**: *リソース グループを作成または選択します*
    - **[リージョン]**: 使用できるリージョンを選択します**
    - **[名前]**: *一意の名前を入力します*
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **責任ある AI 通知**: 同意。
1. **[Review + create](レビュー + 作成)** を選択します。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## Visual Studio Code でアプリの開発準備をする

Visual Studio Code を使用して音声アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

> **ヒント**: **mslearn-ai-language** リポジトリを既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
1. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
1. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。
1. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるダイアログが表示された場合は、 **[今はしない]** を選択します。

## アプリケーションの構成

C# と Python の両方のアプリケーションが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI 音声リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/08-speech-translation** フォルダーを参照し、言語の設定とそこに含まれている **translator** フォルダーに応じて **CSharp** または **Python** フォルダーを展開します。 各フォルダーには、Azure AI 音声機能を統合するアプリの言語固有のコード ファイルが含まれています。
1. コード ファイルを含んだ **translator** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適したコマンドを実行して、Azure AI 音声 SDK パッケージをインストールします。

    **C#**

    ```
    dotnet add package Microsoft.CognitiveServices.Speech --version 1.30.0
    ```

    **Python**

    ```
    pip install azure-cognitiveservices-speech==1.30.0
    ```

1. **[エクスプローラー]** ペインの **translator** フォルダーで、優先する言語の構成ファイルを開きます。

    - **C#** : appsettings.json
    - **Python**: .env

1. 作成した Azure AI 音声リソースの**リージョン**と**キー**を含むように構成値を更新します (リージョンとキーは、Azure portal の Azure AI 音声リソースの **[キーとエンドポイント]** ページで入手できます)。

    > **注**: エンドポイントでは<u>なく</u>、必ずリソースの*リージョン*を追加してください。

1. 構成ファイルを保存します。

## Speech SDK を使用するコードを追加する

1. **translator** フォルダーには、クライアント アプリケーションのコード ファイルが含まれていることに注意してください。

    - **C#** : Program.cs
    - **Python**: translator.py

    コード ファイルを開き、上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Azure AI 音声 SDK を使用するために必要な名前空間をインポートします。

    **C#** : Program.cs

    ```csharp
    // Import namespaces
    using Microsoft.CognitiveServices.Speech;
    using Microsoft.CognitiveServices.Speech.Audio;
    using Microsoft.CognitiveServices.Speech.Translation;
    ```

    **Python**: translator.py

    ```python
    # Import namespaces
    import azure.cognitiveservices.speech as speech_sdk
    ```

1. **Main** 関数では、構成ファイルから Azure AI 音声サービスのキーとリージョンをロードするコードがすでに提供されていることにご注意ください。 これらの変数を使用して、音声入力の翻訳に使用する Azure AI 音声リソース用の **SpeechTranslationConfig** を作成する必要があります。 コメント **「Configure translation」** の下に次のコードを追加します。

    **C#** : Program.cs

    ```csharp
    // Configure translation
    translationConfig = SpeechTranslationConfig.FromSubscription(aiSvcKey, aiSvcRegion);
    translationConfig.SpeechRecognitionLanguage = "en-US";
    translationConfig.AddTargetLanguage("fr");
    translationConfig.AddTargetLanguage("es");
    translationConfig.AddTargetLanguage("hi");
    Console.WriteLine("Ready to translate from " + translationConfig.SpeechRecognitionLanguage);
    ```

    **Python**: translator.py

    ```python
    # Configure translation
    translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
    translation_config.speech_recognition_language = 'en-US'
    translation_config.add_target_language('fr')
    translation_config.add_target_language('es')
    translation_config.add_target_language('hi')
    print('Ready to translate from',translation_config.speech_recognition_language)
    ```

1. **SpeechTranslationConfig** を使用して音声をテキストに翻訳しますが、**SpeechConfig** を使用して翻訳を音声に合成します。 コメント **「Configure speech」** の下に次のコードを追加します。

    **C#** : Program.cs

    ```csharp
    // Configure speech
    speechConfig = SpeechConfig.FromSubscription(aiSvcKey, aiSvcRegion);
    ```

    **Python**: translator.py

    ```python
    # Configure speech
    speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
    ```

1. 変更を保存して、**translator** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python translator.py
    ```

1. C# を使用している場合は、非同期メソッドで **await** 演算子を使用することに関する警告を無視できます。これは後で修正します。 コードは、en-US からターゲット言語に翻訳する準備ができているというメッセージを表示する必要があります。 ENTER を押してプログラムを終了します。

## 音声翻訳の実装

Azure AI 音声サービス用の **SpeechTranslationConfig** が用意されたので、Azure AI 音声翻訳 API を使用して音声を認識および翻訳できます。

> **重要**: このセクションには、2 つの代替手順の手順が含まれています。 マイクが動作している場合は、最初の手順に従います。 オーディオ ファイルを使用して音声入力をシミュレートする場合は、2 番目の手順に従います。

### マイクが機能する場合

1. プログラムの **Main** 関数で、コードが **Translate** 関数を使用して音声入力を翻訳していることに注意してください。
1. **Translate** 関数のコメント **「Translate speech」** の下に、次のコードを追加して、入力にデフォルトのシステムマイクを使用して音声を認識および翻訳するために使用できる **TranslationRecognizer** クライアントを作成します。

    **C#** : Program.cs

    ```csharp
    // Translate speech
    using AudioConfig audioConfig = AudioConfig.FromDefaultMicrophoneInput();
    using TranslationRecognizer translator = new TranslationRecognizer(translationConfig, audioConfig);
    Console.WriteLine("Speak now...");
    TranslationRecognitionResult result = await translator.RecognizeOnceAsync();
    Console.WriteLine($"Translating '{result.Text}'");
    translation = result.Translations[targetLanguage];
    Console.OutputEncoding = Encoding.UTF8;
    Console.WriteLine(translation);
    ```

    **Python**: translator.py

    ```python
    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Speak now...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)
    ```

    > **メモ** アプリケーションのコードは、1 回の呼び出しで入力を 3 つの言語すべてに翻訳します。 特定の言語の翻訳のみが表示されますが、結果の **translations** コレクションでターゲット言語コードを指定することにより、任意の翻訳を取得できます。

1. 下の「**プログラムを実行する**」セクションにスキップします。

---

### または、ファイルからの温泉入力を使用します

1. ターミナル ウィンドウで、次のコマンドを入力して、音声ファイルの再生に使用できるライブラリをインストールします。

    **C#** : Program.cs

    ```csharp
    dotnet add package System.Windows.Extensions --version 4.6.0 
    ```

    **Python**: translator.py

    ```python
    pip install playsound==1.3.0
    ```

1. プログラムのコード ファイルで、既存の名前空間のインポートの下に、次のコードを追加して、インストールしたライブラリをインポートします。

    **C#** : Program.cs

    ```csharp
    using System.Media;
    ```

    **Python**: translator.py

    ```python
    from playsound import playsound
    ```

1. プログラムの **Main** 関数で、コードが **Translate** 関数を使用して音声入力を翻訳していることに注意してください。 **Translate** 関数のコメント **「Translate speech」** の下に、次のコードを追加して、ファイルからの音声を認識して、翻訳するために使用できる **TranslationRecognizer** クライアントを作成します。

    **C#** : Program.cs

    ```csharp
    // Translate speech
    string audioFile = "station.wav";
    SoundPlayer wavPlayer = new SoundPlayer(audioFile);
    wavPlayer.Play();
    using AudioConfig audioConfig = AudioConfig.FromWavFileInput(audioFile);
    using TranslationRecognizer translator = new TranslationRecognizer(translationConfig, audioConfig);
    Console.WriteLine("Getting speech from file...");
    TranslationRecognitionResult result = await translator.RecognizeOnceAsync();
    Console.WriteLine($"Translating '{result.Text}'");
    translation = result.Translations[targetLanguage];
    Console.OutputEncoding = Encoding.UTF8;
    Console.WriteLine(translation);
    ```

    **Python**: translator.py

    ```python
    # Translate speech
    audioFile = 'station.wav'
    playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)
    ```

---

### プログラムの実行

1. 変更を保存して、**translator** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python translator.py
    ```

1. プロンプトが表示されたら、有効な言語コード (*fr*、*es*、または *hi*) を入力します。マイクを使用している場合は、「駅はどこですか?」、 または、海外旅行するときに使用する可能性のある他のフレーズをはっきり言います。 プログラムは、話された入力を書き起こし、指定した言語 (フランス語、スペイン語、またはヒンディー語) に翻訳します。 このプロセスを繰り返し、アプリケーションでサポートされている各言語を試してください。 終了したら、Enter キーを押してプログラムを終了します。

    TranslationRecognizer を使用すると、約 5 秒で話すことができます。 音声入力が検出されない場合は、"一致なし" の結果が生成されます。 文字エンコードの問題により、ヒンディー語への翻訳がコンソール ウィンドウに正しく表示されない場合があります。

> **メモ**: アプリケーションのコードは、1 回の呼び出しで入力を 3 つの言語すべてに翻訳します。 特定の言語の翻訳のみが表示されますが、結果の **translations** コレクションでターゲット言語コードを指定することにより、任意の翻訳を取得できます。

## 翻訳を音声に合成する

これまでのところ、アプリケーションは音声入力をテキストに翻訳します。旅行中に誰かに助けを求める必要がある場合は、これで十分かもしれません。 ただし、適切な声で翻訳を声に出して話してもらう方がよいでしょう。

1. **Translate** 機能では、コメント **「Synthesize translation」** の下に次のコードを追加して、デフォルトのスピーカーから音声として翻訳を合成するために **SpeechSynthesizer** クライアントを使用します。

    **C#** : Program.cs

    ```csharp
    // Synthesize translation
    var voices = new Dictionary<string, string>
                    {
                        ["fr"] = "fr-FR-HenriNeural",
                        ["es"] = "es-ES-ElviraNeural",
                        ["hi"] = "hi-IN-MadhurNeural"
                    };
    speechConfig.SpeechSynthesisVoiceName = voices[targetLanguage];
    using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig);
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(translation);
    if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
    {
        Console.WriteLine(speak.Reason);
    }
    ```

    **Python**: translator.py

    ```python
    # Synthesize translation
    voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    ```

1. 変更を保存して、**translator** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python translator.py
    ```

1. プロンプトが表示されたら、有効な言語コード (*fr*、*es*、*hi*) を入力し、マイクに向かってはっきりと話し、海外旅行で使用する可能性のあるフレーズを話します。 プログラムは、口頭入力を書き起こし、口頭翻訳で応答します。 このプロセスを繰り返し、アプリケーションでサポートされている各言語を試してください。 終了したら、**Enter** キーを押してプログラムを終了します。

> **メモ**
> *この例では、**SpeechTranslationConfig** を使用して音声をテキストに変換し、**SpeechConfig** を使用して翻訳を音声として合成しました。実際には **SpeechTranslationConfig** を使用して翻訳を直接合成できますが、これは 1 つの言語に翻訳する場合にのみ機能し、通常はスピーカーに直接送信されるのではなく、ファイルとして保存されるオーディオ ストリームになります。*

## 詳細情報

Azure AI 音声翻訳 API の使用の詳細については、「[音声翻訳のドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation)」をご覧ください。

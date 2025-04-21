---
lab:
  title: 音声の認識と合成 (Azure AI Foundry バージョン)
  module: Module 4 - Create speech-enabled apps with Azure AI services
---

<!--
Possibly update to use standalone AI Service instead of Foundry?
-->

# 音声の認識と合成

**Azure AI 音声**は、次のような音声関連機能を提供するサービスです。

- 音声認識 (音声の話し言葉をテキストに変換する) を実装できるようにする *speech-to-text* API。
- 音声合成 (テキストを可聴音声に変換する) を実装できるようにする*text-to-speech* API。

この演習では、これらの API の両方を使用して、スピーキング クロック アプリケーションを実装します。

> **注** この演習は、コンピューターのサウンド ハードウェアへの直接アクセスがサポートされていない Azure Cloud Shell で完了するように設計されています。 そのため、ラボでは音声入力ストリームと出力ストリームにオーディオ ファイルが使用されます。 マイクとスピーカーを使用して同じ結果を得るためのコードが参照用に用意されています。

## Azure AI Foundry プロジェクトを作成する

まず、Azure AI Foundry プロジェクトを作成します。

1. Web ブラウザーで [Azure AI Foundry ポータル](https://ai.azure.com) (`https://ai.azure.com`) を開き、Azure 資格情報を使用してサインインします。 初めてサインインするときに開いたヒントまたはクイック スタート ウィンドウを閉じます。また、必要に応じて左上にある **Azure AI Foundry** ロゴを使用してホーム ページに移動します。それは次の画像のようになります。

    ![Azure AI Foundry ポータルのスクリーンショット。](./ai-foundry/media/ai-foundry-home.png)

1. ホーム ページで、**[+ 作成]** を選択します。
1. **[プロジェクトの作成]** ウィザードで、有効なプロジェクト名を入力し、既存のハブが推奨された場合は、新しいハブを作成するオプションを選択します。 次に、ハブとプロジェクトをサポートするために自動的に作成される Azure リソースを確認します。
1. **[カスタマイズ]** を選択し、ハブに次の設定を指定します。
    - **ハブ名**: *ハブの有効な名前*
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **リソース グループ**: *リソース グループを作成または選択します。*
    - **場所**: 使用できる任意のリージョンを選択します
    - **Azure AI サービスまたは Azure OpenAI への接続**: *新しい AI サービス リソースを作成します*
    - **Azure AI 検索の接続**: *一意の名前で新しい Azure AI 検索リソースを作成する*

1. **[次へ]** を選択し、構成を確認します。 **[作成]** を選択し、プロセスが完了するまで待ちます。
1. プロジェクトが作成されたら、表示されているヒントをすべて閉じて、Azure AI Foundry ポータルのプロジェクト ページを確認します。これは次の画像のようになっているはずです。

    ![Azure AI Foundry ポータルの Azure AI プロジェクトの詳細のスクリーンショット。](./ai-foundry/media/ai-foundry-project.png)

## スピーキング クロック アプリを準備して構成する

1. Azure AI Foundry ポータルで、プロジェクトの **[概要]** ページを表示します。
1. **プロジェクトの詳細**領域で、プロジェクトの**プロジェクト接続文字列**と**場所**をメモします。その接続文字列を使用してクライアント アプリケーションでプロジェクトに接続します。Azure AI サービス音声エンドポイントに接続する場所が必要です。
1. 新しいブラウザー タブを開きます (既存のタブで Azure AI Foundry ポータルを開いたままにします)。 新しいブラウザー タブで [Azure portal](https://portal.azure.com) (`https://portal.azure.com`) を開き、メッセージに応じて Azure 資格情報を使用してサインインします。
1. ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal に新しい Cloud Shell を作成します。***PowerShell*** 環境を選択します。 Azure portal の下部にあるペインに、Cloud Shell のコマンド ライン インターフェイスが表示されます。

    > **注**: *Bash* 環境を使用するクラウド シェルを以前に作成した場合は、それを ***PowerShell*** に切り替えます。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

    > **ヒント**: Cloudshell にコマンドを貼り付けると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。

1. PowerShell ペインで、次のコマンドを入力して、この演習用の GitHub リポジトリを複製します。

    ```
   rm -r mslearn-ai-language -f
   git clone https://github.com/microsoftlearning/mslearn-ai-language mslearn-ai-language
    ```

    ***選択したプログラミング言語の手順に従います。***

1. リポジトリが複製されたら、スピーキング クロック アプリケーション コード ファイルを含むフォルダーに移動します。  

    **Python**

    ```
   cd mslearn-ai-language/labfiles/07b-speech/python/speaking-clock
    ```

    **C#**

    ```
   cd mslearn-ai-language/labfiles/07b-speech/c-sharp/speaking-clock
    ```

1. Cloud Shell コマンド ライン ペインで、次のコマンドを入力して、これから使用するライブラリをインストールします。

    **Python**

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv azure-identity azure-ai-projects azure-cognitiveservices-speech==1.42.0
    ```

    **C#**

    ```
   dotnet add package Azure.Identity
   dotnet add package Azure.AI.Projects --prerelease
   dotnet add package Microsoft.CognitiveServices.Speech --version 1.42.0
    ```

1. 次のコマンドを入力して、提供されている構成ファイルを編集します。

    **Python**

    ```
   code .env
    ```

    **C#**

    ```
   code appsettings.json
    ```

    このファイルをコード エディターで開きます。

1. コード ファイルで、**your_project_endpoint** プレースホルダーと **your_location** プレースホルダーをプロジェクトの接続文字列と場所 (Azure AI Foundry ポータルでプロジェクトの **[概要]** ページからコピーしたもの) に置き換えます。
1. プレースホルダーを置き換えたら、**Ctrl + S** キー コマンドを使用して変更を保存してから、**Ctrl + Q** キー コマンドを使用して、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

## Azure AI 音声 SDK を使用するコードを追加する

> **ヒント**: コードを追加する際は、必ず正しいインデントを維持してください。

1. 次のコマンドを入力して、提供されているコード ファイルを編集します。

    **Python**

    ```
   code speaking-clock.py
    ```

    **C#**

    ```
   code Program.cs
    ```

1. コード ファイルの上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Azure AI Foundry プロジェクトの Azure AI サービス リソースで Azure AI 音声 SDK を使用するために必要な名前空間をインポートします。

    **Python**

    ```python
   # Import namespaces
   from dotenv import load_dotenv
   from azure.ai.projects.models import ConnectionType
   from azure.identity import DefaultAzureCredential
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.projects import AIProjectClient
   import azure.cognitiveservices.speech as speech_sdk
    ```

    **C#**

    ```csharp
   // Import namespaces
   using Azure.Identity;
   using Azure.AI.Projects;
   using Microsoft.CognitiveServices.Speech;
   using Microsoft.CognitiveServices.Speech.Audio;
    ```

1. **main** 関数のコメント**構成設定の取得**で、構成ファイルで定義したプロジェクト接続文字列と場所がコードで読み込まれることに注意してください。

1. **プロジェクトから AI 音声エンドポイントとキーを取得**というコメントの下に次のコードを追加します。

    **Python**

    ```python
   # Get AI Services key from the project
   project_client = AIProjectClient.from_connection_string(
        conn_str=project_connection,
        credential=DefaultAzureCredential())

   ai_svc_connection = project_client.connections.get_default(
      connection_type=ConnectionType.AZURE_AI_SERVICES,
      include_credentials=True, 
    )

   ai_svc_key = ai_svc_connection.key

    ```

    **C#**

    ```csharp
   // Get AI Services key from the project
   var projectClient = new AIProjectClient(project_connection,
                        new DefaultAzureCredential());

   ConnectionResponse aiSvcConnection = projectClient.GetConnectionsClient().GetDefaultConnection(ConnectionType.AzureAIServices, true);

   var apiKeyAuthProperties = aiSvcConnection.Properties as ConnectionPropertiesApiKeyAuth;

   var aiSvcKey = apiKeyAuthProperties.Credentials.Key;
    ```

    このコードは、Azure AI Foundry プロジェクトに接続し、その既定の AI サービス接続リソースを取得し、それを使用するために必要な認証キーを取得します。

1. **音声サービスの構成**というコメントの下に、次のコードを追加して AI サービス キーとプロジェクトのリージョンを使用し、Azure AI サービス音声エンドポイントへの接続を構成します。

   **Python**

    ```python
   # Configure speech service
   speech_config = speech_sdk.SpeechConfig(ai_svc_key, location)
   print('Ready to use speech service in:', speech_config.region)
    ```

    **C#**

    ```csharp
   // Configure speech service
   speechConfig = SpeechConfig.FromSubscription(aiSvcKey, location);
   Console.WriteLine("Ready to use speech service in " + speechConfig.Region);
    ```

1. 変更を保存しますが (*CTRL + S*)、コード エディターは開いたままにします。

## アプリを実行する

ここまで、アプリは、音声サービスを使用するために必要な詳細を取得するために Azure AI Foundry プロジェクトに接続する以外には何も行いませんが、音声機能を追加する前に実行して動作することを確認すると有用です。

1. コード エディターの下のコマンド ラインで、次の Azure CLI コマンドを入力して、セッションにサインインしている Azure アカウントを確認します。

    ```
   az account show
    ```

    結果の JSON 出力には、Azure アカウントと作業中のサブスクリプションの詳細が含まれている必要があります (Azure AI Foundry プロジェクトを作成したのと同じサブスクリプションである必要があります)。

    アプリは、実行されるコンテキストに Azure 資格情報を使用して、プロジェクトへの接続を認証します。 運用環境では、アプリがマネージド ID を使用して実行されるように構成されている場合があります。 この開発環境では、認証された Cloud Shell セッション資格情報が使用されます。

    > **注**: `az login` Azure CLI コマンドを使用して、開発環境で Azure にサインインできます。 この場合、Cloud Shell は、ポータルにサインインした Azure 資格情報を使用して既にログインしています。そのため、改めてサインインする必要はありません。 Azure CLI を使用して Azure に対して認証する方法の詳細については、「[　Azure CLI を使用した Azure への認証](https://learn.microsoft.com/cli/azure/authenticate-azure-cli)」を参照してください。

1. コマンド ラインで、次の言語固有のコマンドを入力して、スピーキング クロック アプリを実行します。

    **Python**

    ```
   python speaking-clock.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. C# を使用している場合は、非同期メソッドで **await** 演算子を使用することに関する警告を無視できます。これは後で修正します。 コードは、アプリケーションが使用する音声サービスリソースの領域を表示する必要があります。 正常な実行は、アプリが Azure AI Foundry プロジェクトに接続され、Azure AI 音声サービスを使用するために必要なキーを取得したことを示します。

## 音声を認識するコードを追加する

プロジェクトの Azure AI 音声リソースに音声サービス用の **SpeechConfig** があるので、**音声テキスト変換** API を使用して音声を認識し、文字起こしすることができます。

この手順では、音声入力がオーディオ ファイルからキャプチャされ、ここで再生できます。

<video controls src="ai-foundry/media/Time.mp4" title="今何時?" width="150"></video>

1. **Main** 関数で、コードが **TranscribeCommand** 関数を使用して音声入力を受け入れることに注意してください。 **TranscribeCommand** 関数のコメント **「Configure speech recognition」** の下に、適切なコードを追加して、音声ファイルからの音声を認識して、書き起こすために使用できる **SpeechRecognizer** クライアントを作成します。

    **Python**

    ```python
   # Configure speech recognition
   current_dir = os.getcwd()
   audioFile = current_dir + '/time.wav'
   audio_config = speech_sdk.AudioConfig(filename=audioFile)
   speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    ```

    **C#**

    ```csharp
   // Configure speech recognition
   string audioFile = "time.wav";
   using AudioConfig audioConfig = AudioConfig.FromWavFileInput(audioFile);
   using SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
    ```

1. **TranscribeCommand** 関数のコメント **「Process speech input」** の下に、音声入力をリッスンする次のコードを追加します。コマンドを返す関数の最後にあるコードを置き換えないように注意してください。

    **Python**

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

    **C#**

    ```csharp
   // Process speech input
   Console.WriteLine("Listening...");
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

1. 変更を保存し (*Ctrl + S* キー)、コード エディターの下のコマンド ラインで、次のコマンドを入力してプログラムを実行します。

    **Python**

    ```
   python speaking-clock.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. アプリケーションからの出力を確認します。オーディオ ファイルの音声が正常に "聞こえて"、適切な応答が返されるはずです (Azure Cloud Shell が別のタイム ゾーンにあるサーバーで実行されている可能性があることに注意してください)。

    > **ヒント**: SpeechRecognizer でエラーが発生した場合は、"Cancelled" の結果が生成されます。 アプリケーションのコードは、エラーメッセージを表示します。 最も可能性の高い原因は、構成ファイルのリージョンの値が正しくないことです。

## 音声を合成する

speaking clock アプリケーションは話し言葉の入力を受け入れますが、実際には話しません。 音声合成用のコードを追加して修正しましょう。

Cloud Shell のハードウェアの制限があるため、もう一度合成された音声出力をファイルに転送します。

1. プログラムの **Main** 関数で、コードが **TellTime** 関数を使用してユーザーに現在の時刻を通知することに注意してください。
1. **TellTime** 関数のコメント **「Configure speech synthesis」** の下に、次のコードを追加して、音声出力の生成に使用できる **SpeechSynthesizer** クライアントを作成します。

    **Python**

    ```python
   # Configure speech synthesis
   output_file = "output.wav"
   speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
   audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config,)
    ```

    **C#**

    ```csharp
   // Configure speech synthesis
   var outputFile = "output.wav";
   speechConfig.SpeechSynthesisVoiceName = "en-GB-RyanNeural";
   using var audioConfig = AudioConfig.FromWavFileOutput(outputFile);
   using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig);
    ```

1. **TellTime** 関数のコメント **「Synthesize spoken output」** の下に、次のコードを追加して音声出力を生成します。応答を出力する関数の最後にあるコードを置き換えないように注意してください。

    **Python**

    ```python
   # Synthesize spoken output
   speak = speech_synthesizer.speak_text_async(response_text).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
       print(speak.reason)
   else:
       print("Spoken output saved in " + outputFile)
    ```

    **C#**

    ```csharp
   // Synthesize spoken output
   SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(responseText);
   if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
   {
       Console.WriteLine(speak.Reason);
   }
   else
   {
       Console.WriteLine("Spoken output saved in " + outputFile);
   }
    ```

1. 変更を保存し (*Ctrl + S* キー)、コード エディターの下のコマンド ラインで、次のコマンドを入力してプログラムを実行します。

   **Python**

    ```
   python speaking-clock.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. アプリケーションからの出力を確認します。これで、読み上げられた出力がファイルに保存されたことが示されるはずです。
1. .wav オーディオ ファイルを再生できるメディア プレーヤーがある場合は、Cloud Shell 画面のツール バーの **[ファイルのアップロード/ダウンロード]** ボタンを使用して、アプリ フォルダーからオーディオ ファイルをダウンロードし、再生します。

    **Python**

    /home/*user*`/mslearn-ai-language/Labfiles/07b-speech/Python/speaking-clock/output.wav`

    **C#**

    /home/*user*`/mslearn-ai-language/Labfiles/07b-speech/C-Sharp/speaking-clock/output.wav`

    ファイルは次のようになるはずです。

    <video controls src="./ai-foundry/media/Output.mp4" title="時刻は 2:15 です。" width="150"></video>

## 音声合成マークアップ言語を使用する

音声合成アップ言語 (SSML) を使用すると、XML ベースの形式を使用して音声を合成する方法をカスタマイズできます。

1. **TellTime** 関数で、コメント **「Synthesize spoken output」** の下にある現在のすべてのコードを次のコードに置き換えます (コメント **Print the response** の下にコードを残します)。

    **Python**

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
       print("Spoken output saved in " + outputFile)
    ```

   **C#**

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
   else
   {
        Console.WriteLine("Spoken output saved in " + outputFile);
   }
    ```

1. 変更を保存して、**speaking-clock** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    **Python**

    ```
   python speaking-clock.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. アプリケーションからの出力を確認します。これで、読み上げられた出力がファイルに保存されたことが示されるはずです。
1. .wav オーディオ ファイルを再生できるメディア プレーヤーがある場合は、もう一度 Cloud Shell 画面のツール バーの **[ファイルのアップロード/ダウンロード]** ボタンを使用して、アプリ フォルダーからオーディオ ファイルをダウンロードし、再生します。

    **Python**

    /home/*user*`/mslearn-ai-language/Labfiles/07b-speech/Python/speaking-clock/output.wav`

    **C#**

    /home/*user*`/mslearn-ai-language/Labfiles/07b-speech/C-Sharp/speaking-clock/output.wav`

    ファイルは次のようになるはずです。
    
    <video controls src="./ai-foundry/media/Output2.mp4" title="時刻は 5:30 です。 このラボの終了時間です。" width="150"></video>

## クリーンアップ

Azure AI Speech の探索が終わったら、不要な Azure コストが発生しないように、この演習で作成したリソースを削除する必要があります。

1. Azure portal が表示されているブラウザー タブに戻り (または、新しいブラウザー タブで `https://portal.azure.com` の [Azure portal](https://portal.azure.com) をもう一度開き)、この演習で使用したリソースがデプロイされているリソース グループの内容を表示します。
1. ツール バーの **[リソース グループの削除]** を選びます。
1. リソース グループ名を入力し、削除することを確認します。

## マイクとスピーカーがある場合

この演習では、音声の入力と出力にオーディオ ファイルを使用しました。 オーディオ ハードウェアを使用するようにコードを変更する方法を見てみましょう。

### マイクによる音声認識の使用

マイクがある場合は、次のコードを使用して音声認識用の音声入力をキャプチャできます。

**Python**

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

**C#**

```csharp
// Configure speech recognition
using AudioConfig audioConfig = AudioConfig.FromDefaultMicrophoneInput();
using SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
Console.WriteLine("Speak now...");

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

> **注**: システムの既定のマイクは既定のオーディオ入力であるため、AudioConfig を完全に省略することもできます。

### スピーカーによる音声合成の使用

スピーカーがある場合は、次のコードを使用して音声を合成できます。

**Python**

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

**C#**

```csharp
var now = DateTime.Now;
string responseText = "The time is " + now.Hour.ToString() + ":" + now.Minute.ToString("D2");

// Configure speech synthesis
speechConfig.SpeechSynthesisVoiceName = "en-GB-RyanNeural";
using var audioConfig = AudioConfig.FromDefaultSpeakerOutput();
using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig);

// Synthesize spoken output
SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(responseText);
if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
{
    Console.WriteLine(speak.Reason);
}
```

> **注**: システムの既定のスピーカーは既定のオーディオ出力であるため、AudioConfig を完全に省略することもできます。

## 詳細

**Speech-to-text** および **Text-to-speech** API の使用の詳細については、[Speech-to-text ドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text)および [Text-to-speech ドキュメント](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech)を参照してください。

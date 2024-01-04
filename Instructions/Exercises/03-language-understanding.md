---
lab:
  title: Azure AI Language サービスで言語理解モデルを作成する
  module: Module 5 - Create language understanding solutions
---

# 言語サービスで言語理解モデルを作成する

> **メモ** Azure AI Language サービスの会話言語理解機能は、現在プレビュー段階であり、変更される可能性があります。 場合によっては、モデルのトレーニングに失敗することがありますが、その場合はもう一度やり直してください。  

Azure AI Language サービスを利用すると、*会話言語理解*モデルを定義できます。このモデルをアプリケーションで使用すると、ユーザーからの自然言語入力を解釈し、ユーザーの*意図* (達成したいこと) を予測し、その意図を適用すべき*エンティティ*を特定することができます。

たとえば、時計アプリケーション用の会話言語モデルは、次のような入力を処理することが期待される場合があります。

*What's the time in London?* (ロンドンの時刻は何時ですか?)

この種の入力は、*発話* (ユーザーが言うまたは入力する可能性のあるもの) の例です。*意図* は、特定の場所 (*エンティティ*) (この場合はロンドン) の時刻を得ることです。

> **メモ** 会話言語モデルのタスクは、ユーザーの意図を予測し、意図が適用されるエンティティを特定することです。 意図を満たすために必要なアクションを実際に実行することは、会話言語モデルの仕事では<u>ありません</u>。 たとえば、時計アプリケーションは会話言語モデルを使用して、ユーザーがロンドンの時刻を知りたいことを識別できます。ただし、クライアント アプリケーション自体は、正しい時刻を決定してユーザーに提示するロジックを実装する必要があります。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションにまだリソースがない場合は、Azure サブスクリプションで **Azure AI Language サービス** リソースをプロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部にある検索フィールドで **Azure AI サービス** を検索します。 次に、結果で、**[言語サービス]** の下の **[作成]** を選択します。
1. **[リソースの作成を続行する]** を選択します。
1. 次の設定を使用してリソースをプロビジョニングします。
    - **[サブスクリプション]**: *お使いの Azure サブスクリプション*。
    - **[リソース グループ]**: *リソース グループを作成または選択します*。
    - **[リージョン]**: *使用できるリージョンを選択します*。
    - **[名前]**: *一意の名前を入力します*。
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **責任ある AI 通知**: 同意。
1. **[Review + create](レビュー + 作成)** を選択します。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## 会話言語理解プロジェクトを作成する

作成リソースを作成したら、それを使って会話言語理解プロジェクトを作成できます。

1. 新しいブラウザー タブで Azure AI Language ポータル (`https://language.cognitive.azure.com/`) を開き、お使いの Azure サブスクリプションに関連付けられている Microsoft アカウントを使ってサインインします。

1. 言語リソースの選択を求めるメッセージが表示されたら、次の設定を選択します。

    - **Azure ディレクトリ**: ご利用のサブスクリプションを含む Azure ディレクトリ
    - **Azure サブスクリプション**: ご利用の Azure サブスクリプション
    - **リソースの種類**: 言語。
    - **言語リソース**: 以前に作成した Azure AI Language リソース。

    言語リソースの選択を求めるメッセージが表示<u>されない</u>場合、原因として、お使いのサブスクリプションに複数の言語リソースが存在していることが考えられます。その場合は、次の操作を行います。

    1. ページの上部にあるバーで、**[設定] (⚙)** ボタンを選択します。
    2. **[設定]** ページで、**[リソース]** タブを表示します。
    3. 作成したばかりの言語リソースを選択し、**[リソースの切り替え]** をクリックします。
    4. ページの上部で、**[Language Studio]** をクリックして、Language Studio のホーム ページに戻ります。

1. ポータルの上部にある **[新規作成]** メニューで、**[会話言語理解]** を選択します。

1. **[プロジェクトの作成]** ダイアログ ボックスの **[基本情報の入力]** ページで、次の詳細を入力したあと、**[次へ]** を選択します。
    - **名前**: `Clock`
    - **発話の主要言語**: 英語
    - **プロジェクトで複数の言語を有効にする**: *オフ*
    - **説明**: `Natural language clock`

1. **[確認と完了]** ページで、**[作成]** を選択します。

### 意図の作成

新しいプロジェクトで最初に行うことは、いくつかの意図を定義することです。 モデルは最終的に、自然言語の発話を送信するときに、これらの意図のうち、どれをユーザーが要求しているかを予測します。

> **ヒント**: プロジェクトの作業中に、ヒントがいくつか表示されていたら、そのヒントを読み、**[了解]** を選択して閉じるか、**[すべてスキップ]** を選択します。

1. **[スキーマ定義]** ページの **[意図]** タブで **[＋ 追加]** を選び、`GetTime` という新しい意図を追加します。
1. **GetTime** 意図が (既定の **None** 意図と共に) 一覧表示されていることを確認します。 次に、次の意図を追加します。
    - `GetDay`
    - `GetDate`

### 各意図にサンプル発話でラベルを付ける

モデルでユーザーが要求している意図を予測できるようにするには、各意図にサンプル発話のラベルを付ける必要があります。

1. 左側のペインで、**[データのラベル付け]** ページを選択します。

> **ヒント**: **>>** アイコン付きのペインを展開してページ名を表示し、**<<** アイコンでもう一度非表示にすることができます。

1. 新しい **GetTime** 意図を選択し、発話 `what is the time?` を入力します。 これにより、発話が意図のサンプル入力として追加されます。
1. **GetTime** 意図に次の発話を追加します。
    - `what's the time?`
    - `what time is it?`
    - `tell me the time`

1. **GetDay** 意図を選択し、その意図の入力の例として次の発話を追加します。
    - `what day is it?`
    - `what's the day?`
    - `what is the day today?`
    - `what day of the week is it?`

1. **GetDate** 意図を選択し、次の発話を追加します。
    - `what date is it?`
    - `what's the date?`
    - `what is the date today?`
    - `what's today's date?`

1. 意図ごとに発話を追加したら、**[変更の保存]** を選択します。

### モデルのトレーニングとテスト

意図をいくつか追加したので、言語モデルをトレーニングして、ユーザー入力から正しく予測できるかどうかを確認しましょう。

1. 左側のペインで、**[トレーニング ジョブ]** を選択します。 **[+ トレーニング ジョブの開始]** を選択します。

1. **[トレーニング ジョブの開始]** ダイアログで、新しいモデルをトレーニングするオプションを選択し、「Clock」という名前を付けます。 **標準トレーニング** モードと既定の **[データ分割]** オプションを選択します。

1. モデルのトレーニング プロセスを開始するには、**[トレーニングする]** をクリックします。

1. トレーニングが完了した場合 (数分かかることがあります)、ジョブの **[状態]** が " **トレーニング成功**" に変わります。

1. **[モデルのパフォーマンス]** ページを選択して、 **[Clock]** モデルを選択します。 全体と意図ごとの評価メトリック ( *"精度"* 、 *"再現率"* 、 *"F1 スコア"* ) と、トレーニング時に行った評価で生成された *"混同行列"* を確認します (サンプル発話数が少ないため、すべての意図が結果に含まれていない可能性がある点に注意してください)。

    > **メモ** 評価メトリックの詳細については、「[ドキュメント](/azure/ai-services/language-service/conversational-language-understanding/concepts/evaluation-metrics)」をご覧ください。

1. **[モデルのデプロイ]** ページに移動して、**[デプロイの追加]** を選択します。

1. **[デプロイの追加]** ダイアログで、**[新しいデプロイ名を作成する]** を選択し、「`production`」と入力します。

1. **[モデル]** フィールドで **[Clock]** モデルを選択し、**[デプロイ]** を選択します。 デプロイには少し時間がかかることがあります。

1. モデルがデプロイされたら、**[デプロイのテスト]** ページを選択し、**[デプロイ名]** フィールドで**運用環境**のデプロイを選択します。

1. 空のテキストボックスに次のテキストを入力し、**[テストの実行]** を選択します。

    `what's the time now?`

    返された結果を確認します。予測された意図 (**GetTime** であるはずです) と、予測された意図に対してモデルが計算した確率を示す信頼スコアが含まれていることに注意してください。 [JSON] タブには、考えられる各意図の信頼度の比較が表示されます (信頼度スコアが最も高いものが予測された意図です)

1. テキスト ボックスをクリアし、次のテキストを使って別のテストを実行します。

    `tell me the time`

    もう一度、予測された意図と信頼スコアを確認します。

1. 次のテキストを試します。

    `what's the day today?`

    うまくいけば、モデルは **GetDay** 意図を予測します。

## 複数エンティティの追加

これまで、意図にマップするいくつかの簡単な発話を定義しました。 ほとんどの実際のアプリケーションには、より複雑な発話が含まれており、意図のコンテキストを増やすために、特定のデータ エンティティを抽出する必要があります。

### 学習済み エンティティを追加する

最も一般的な種類のエンティティは *学習済み* エンティティであり、モデルは例に基づいてエンティティ値を識別することを学習します。

1. Language Studio の **[スキーマ定義]** ページに戻り、 **[エンティティ]** タブで **[&#65291; 追加]** を選んで新しいエンティティを追加します。

1. **[エンティティの追加]** ダイアログ ボックスで、エンティティ名「`Location`」を入力し、**[学習済み]** タブが選ばれていることを確認します。 **[エンティティの追加]** を選択します。

1. **場所**エンティティが作成されたら、**[データのラベル付け]** ページに戻ります。
1. **GetTime** 意図を選択し、次の新しい発話例を入力します。

    `what time is it in London?`

1. 発話が追加されたら、**London** という単語を選び、表示されるドロップダウン リストで **Location** を選んで、"London" が場所の例であることを示します。

1. **GetTime** 意図の発話の例をもう 1 つ追加します。

    `Tell me the time in Paris?`

1. 発話が追加されたら、**Paris** という単語を選び、それを **Location** エンティティにマップします。

1. **GetTime** 意図の発話の例をもう 1 つ追加します。

    `what's the time in New York?`

1. 発話が追加されたら、**New York** という単語を選択し、それらを **Location** エンティティにマップします。

1. **[変更の保存]** を選択して、新しい発話を保存します。

### *リスト* エンティティを追加する

場合によっては、エンティティの有効な値を特定の用語と同義語のリストに制限できます。これは、アプリが発話内のエンティティのインスタンスを識別するのに役立ちます。

1. Language Studio の **[スキーマ定義]** ページに戻り、 **[エンティティ]** タブで **[&#65291; 追加]** を選んで新しいエンティティを追加します。

1. **[エンティティの追加]** ダイアログ ボックスで、エンティティ名「`Weekday`」を入力し、**[リスト]** エンティティ タブを選択します。次に、**[エンティティの追加]** を選択します。

1. **Weekday** エンティティのページの **[学習済み]** セクションで、**[必要なし] **が選択されていることを確認します。 次に、**[リスト]** セクションで、**[＋ 新しいリストの追加]** を選択します。 次の値と同意語を入力し、**[保存]** を選択します。

    | キーの一覧表示 | シノニム|
    |-------------------|---------|
    | `Sunday` | `Sun` |

1. 前の手順を繰り返して、次のリスト コンポーネントを追加します。

    | 値 | シノニム|
    |-------------------|---------|
    | `Monday` | `Mon` |
    | `Tuesday` | `Tue, Tues` |
    | `Wednesday` | `Wed, Weds` |
    | `Thursday` | `Thur, Thurs` |
    | `Friday` | `Fri` |
    | `Saturday` | `Sat` |

1. リスト値を追加して保存した後、「**データのラベル付け**」ページに戻ります。
1. **GetDate** 意図を選択し、次の新しい発話例を入力します。

    `what date was it on Saturday?`

1. 発話が追加されたら、***Saturday*** という単語を選び、表示されるドロップダウン リストで **Weekday** を選びます。

1. **GetDate** 意図の発話例をもう 1 つ追加します。

    `what date will it be on Friday?`

1. 発話が追加されたら、**Friday** を **Weekday** エンティティにマップします。

1. **GetDate** 意図の発話例をもう 1 つ追加します。

    `what will the date be on Thurs?`

1. 発話が追加されたら、**Thurs** を **Weekday** エンティティにマップします。

1. **[変更の保存]** を選択して、新しい発話を保存します。

### *事前構築済み* エンティティを追加する

Azure AI Language サービスには、会話アプリケーションでよく使われる*事前構築済み*エンティティのセットが用意されています。

1. Language Studio の **[スキーマ定義]** ページに戻り、 **[エンティティ]** タブで **[&#65291; 追加]** を選んで新しいエンティティを追加します。

1. **[エンティティの追加]** ダイアログ ボックスで、エンティティ名「`Date`」を入力し、**[事前構築済み]** エンティティ タブを選択します。次に、**[エンティティの追加]** を選択します。

1. **Date** エンティティのページの **[学習済み]** セクションで、**[必要なし]** が選択されていることを確認します。 次に、**[事前構築済み]** セクションで **[＋ 新しい事前構築済みの追加]** を選択します。

1. **[事前構築済みの選択]** リストで **DateTime** を選び、**[保存]** を選択します。
1. 事前構築済みエンティティを追加した後、「**データのラベル付け**」ページに戻ります。
1. **GetDay** 意図を選択し、次の新しい発話例を入力します。

    `what day was 01/01/1901?`

1. 発話が追加されたら、***01/01/1901*** を選び、表示されるドロップダウン リストで **Date** を選びます。

1. **GetDay** 意図の発話例をもう 1 つ追加します。

    `what day will it be on Dec 31st 2099?`

1. 発話が追加されたら、**Dec 31st 2099** を **Date** エンティティにマップします。

1. **[変更の保存]** を選択して、新しい発話を保存します。

### モデルの再トレーニング

スキーマを変更したので、モードを再トレーニングして再テストする必要があります。

1. **[トレーニング ジョブ]** ページで、 **[トレーニング ジョブの開始]** を選択します。

1. **[トレーニング ジョブの開始]** ダイアログで、**[既存のモデルを上書きする]** を選び、**Clock** モデルを指定します。 **[トレーニング]** を選択して、モデルをトレーニングします。 メッセージが表示されたら、既存のモデルを上書きすることを確認します。

1. トレーニングが完了した場合、ジョブの **[状態]** が " **トレーニング成功**" に更新されます。

1. **[モデルのパフォーマンス]** ページを選択して、 **[Clock]** モデルを選択します。 評価メトリック (*精度*、*リコール*、*F1 スコア*) と、トレーニング時に行った評価で生成された*混同行列*を確認します (サンプル発話数が少ないため、必ずしもすべての意図が結果に含まれていない可能性がある点に注意してください)。

1. **[モデルの展開]** ページで、 **[展開の追加]** を選択します。

1. **[展開の追加]** ダイアログで、**[既存の展開名をオーバーライドする]** を選択し、「**production**」を選択します。

1. **[モデル]** フィールドで **[クロック]** モデルを選択し、**[デプロイ]** を選択してモデルをデプロイします。 これには時間がかかる場合があります。

1. モデルが展開されたら、「**デプロイのテスト**」ページで **[デプロイ名]** フィールドの下にある **[実稼働]** のデプロイを選択して、次のテキストでモデルをテストします。

    `what's the time in Edinburgh?`

1. 返された結果を確認します。**GetTime** 意図と、テキスト値が "Edinburgh" の **Location** エンティティが予測されるはずです。

1. 次の発話をテストしてみてください。

    `what time is it in Tokyo?`

    `what date is it on Friday?`

    `what's the date on Weds?`

    `what day was 01/01/2020?`

    `what day will Mar 7th 2030 be?`

## クライアント アプリからモデルを使う

実際のプロジェクトでは、予測パフォーマンスに満足するまで、意図とエンティティを繰り返し改良し、再トレーニングして、再テストします。 次に、モデルをテストしてその予測のパフォーマンスに満足したら、REST インターフェイスまたはランタイム固有の SDK を呼び出してクライアント アプリで使用できます。

### Visual Studio Code でアプリの開発準備をする

Visual Studio Code を使用して、Language Understanding アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

> **ヒント**: **mslearn-ai-language** リポジトリを既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
2. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
3. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。
4. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるダイアログが表示された場合は、 **[今はしない]** を選択します。

### アプリケーションの構成

C# と Python の両方のアプリケーションと、要約のテストに使用するサンプル テキスト ファイルが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI Language リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/03-language** フォルダーを参照し、言語の設定とそこに含まれている **clock-client** フォルダーに応じて **CSharp** または **Python** フォルダーを展開します。 各フォルダーには、Azure AI Language の質問に回答する機能を統合するアプリの言語固有のファイルが含まれています。
2. コード ファイルを含む **clock-client** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適したコマンドを実行して、Azure AI Language 会話言語理解 SDK パッケージをインストールします。

    **C#:**

    ```
    dotnet add package Azure.AI.Language.Conversations --version 1.1.0
    ```

    **Python**:

    ```
    pip install azure-ai-language-conversations
    ```

3. **[エクスプローラー]** ペインの **clock-client** フォルダーで、優先する言語の構成ファイルを開きます。

    - **C#** : appsettings.json
    - **Python**: .env
    
4. 構成値を更新して、作成した Azure Language リソースの**エンドポイント**と**キー**を含めます (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで使用できます)。
5. 構成ファイルを保存します。

### アプリケーションにコードを追加する

これで、必要な SDK ライブラリをインポートするために必要なコードを追加し、デプロイされたプロジェクトへの認証済み接続を確立し、質問を送信する準備ができました。

1. **clock-client** フォルダーには、クライアント アプリケーションのコード ファイルが含まれていることにご注意ください。

    - **C#** : Program.cs
    - **Python**: clock-client.py

    コード ファイルを開き、上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Text Analytics SDK を使用するために必要な名前空間インポートします。

    **C#**: Programs.cs

    ```c#
    // import namespaces
    using Azure;
    using Azure.AI.Language.Conversations;
    ```

    **Python**: clock-client.py

    ```python
    # Import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.conversations import ConversationAnalysisClient
    ```

1. **Main** 関数では、構成ファイルから予測エンドポイント、およびキーを読み込むためのコードが既に提供されていることに注意してください。 次に、コメント "**Create a client for the Language service model**" を見つけ、次のコードを追加して、言語サービス アプリの予測クライアントを作成します。

    **C#**: Programs.cs

    ```c#
    // Create a client for the Language service model
    Uri endpoint = new Uri(predictionEndpoint);
    AzureKeyCredential credential = new AzureKeyCredential(predictionKey);

    ConversationAnalysisClient client = new ConversationAnalysisClient(endpoint, credential);
    ```

    **Python**: clock-client.py

    ```python
    # Create a client for the Language service model
    client = ConversationAnalysisClient(
        ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))
    ```

1. ユーザーが「quit」と入力するまで、**Main** 関数のコードはユーザー入力を求めるプロンプトを表示することにご注意ください。 このループ内で、コメント "**Call the Language service model to get intent and entities**" を見つけて、次のコードを追加します。

    **C#**: Programs.cs

    ```c#
    // Call the Language service model to get intent and entities
    var projectName = "Clock";
    var deploymentName = "production";
    var data = new
    {
        analysisInput = new
        {
            conversationItem = new
            {
                text = userText,
                id = "1",
                participantId = "1",
            }
        },
        parameters = new
        {
            projectName,
            deploymentName,
            // Use Utf16CodeUnit for strings in .NET.
            stringIndexType = "Utf16CodeUnit",
        },
        kind = "Conversation",
    };
    // Send request
    Response response = await client.AnalyzeConversationAsync(RequestContent.Create(data));
    dynamic conversationalTaskResult = response.Content.ToDynamicFromJson(JsonPropertyNames.CamelCase);
    dynamic conversationPrediction = conversationalTaskResult.Result.Prediction;   
    var options = new JsonSerializerOptions { WriteIndented = true };
    Console.WriteLine(JsonSerializer.Serialize(conversationalTaskResult, options));
    Console.WriteLine("--------------------\n");
    Console.WriteLine(userText);
    var topIntent = "";
    if (conversationPrediction.Intents[0].ConfidenceScore > 0.5)
    {
        topIntent = conversationPrediction.TopIntent;
    }
    ```

    **Python**: clock-client.py

    ```python
    # Call the Language service model to get intent and entities
    cls_project = 'Clock'
    deployment_slot = 'production'

    with client:
        query = userText
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": cls_project,
                    "deploymentName": deployment_slot,
                    "verbose": True
                }
            }
        )

    top_intent = result["result"]["prediction"]["topIntent"]
    entities = result["result"]["prediction"]["entities"]

    print("view top intent:")
    print("\ttop intent: {}".format(result["result"]["prediction"]["topIntent"]))
    print("\tcategory: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
    print("\tconfidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

    print("view entities:")
    for entity in entities:
        print("\tcategory: {}".format(entity["category"]))
        print("\ttext: {}".format(entity["text"]))
        print("\tconfidence score: {}".format(entity["confidenceScore"]))

    print("query: {}".format(result["result"]["query"]))
    ```

    言語サービス モデルを呼び出すと、予測または結果が返されます。これには、入力発話で検出されたエンティティだけでなく、最上位の (最も可能性の高い) 意図も含まれます。 クライアント アプリケーションは、その予測を使用して適切なアクションを決定および実行する必要があります。

1. コメント **Apply the appropriate action** を見つけ、次のコードを追加します。このコードは、アプリケーションでサポートされている意図 (**GetTime**、**GetDate**、および **GetDay**) をチェックします。また、適切な応答を生成するために既存の関数を呼び出す前に、関連するエンティティが検出されたかどうかを判断します。

    **C#**: Programs.cs

    ```c#
    // Apply the appropriate action
    switch (topIntent)
    {
        case "GetTime":
            var location = "local";           
            // Check for a location entity
            foreach (dynamic entity in conversationPrediction.Entities)
            {
                if (entity.Category == "Location")
                {
                    //Console.WriteLine($"Location Confidence: {entity.ConfidenceScore}");
                    location = entity.Text;
                }
            }
            // Get the time for the specified location
            string timeResponse = GetTime(location);
            Console.WriteLine(timeResponse);
            break;
        case "GetDay":
            var date = DateTime.Today.ToShortDateString();            
            // Check for a Date entity
            foreach (dynamic entity in conversationPrediction.Entities)
            {
                if (entity.Category == "Date")
                {
                    //Console.WriteLine($"Location Confidence: {entity.ConfidenceScore}");
                    date = entity.Text;
                }
            }            
            // Get the day for the specified date
            string dayResponse = GetDay(date);
            Console.WriteLine(dayResponse);
            break;
        case "GetDate":
            var day = DateTime.Today.DayOfWeek.ToString();
            // Check for entities            
            // Check for a Weekday entity
            foreach (dynamic entity in conversationPrediction.Entities)
            {
                if (entity.Category == "Weekday")
                {
                    //Console.WriteLine($"Location Confidence: {entity.ConfidenceScore}");
                    day = entity.Text;
                }
            }          
            // Get the date for the specified day
            string dateResponse = GetDate(day);
            Console.WriteLine(dateResponse);
            break;
        default:
            // Some other intent (for example, "None") was predicted
            Console.WriteLine("Try asking me for the time, the day, or the date.");
            break;
    }
    ```

    **Python**: clock-client.py

    ```python
    # Apply the appropriate action
    if top_intent == 'GetTime':
        location = 'local'
        # Check for entities
        if len(entities) > 0:
            # Check for a location entity
            for entity in entities:
                if 'Location' == entity["category"]:
                    # ML entities are strings, get the first one
                    location = entity["text"]
        # Get the time for the specified location
        print(GetTime(location))

    elif top_intent == 'GetDay':
        date_string = date.today().strftime("%m/%d/%Y")
        # Check for entities
        if len(entities) > 0:
            # Check for a Date entity
            for entity in entities:
                if 'Date' == entity["category"]:
                    # Regex entities are strings, get the first one
                    date_string = entity["text"]
        # Get the day for the specified date
        print(GetDay(date_string))

    elif top_intent == 'GetDate':
        day = 'today'
        # Check for entities
        if len(entities) > 0:
            # Check for a Weekday entity
            for entity in entities:
                if 'Weekday' == entity["category"]:
                # List entities are lists
                    day = entity["text"]
        # Get the date for the specified day
        print(GetDate(day))

    else:
        # Some other intent (for example, "None") was predicted
        print('Try asking me for the time, the day, or the date.')
    ```

1. 変更を保存し、**clock-client** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    - **C#** : `dotnet run`
    - **Python**: `python clock-client.py`

    > **ヒント**: [ターミナル] ツールバーの **最大化パネル サイズ** (**^**) アイコンを使用すると、コンソール テキストをさらに表示できます。

1. プロンプトが表示されたら、発話を入力してアプリケーションをテストします。 たとえば、次の操作を試してください。

    *Hello*

    *What time is it?*

    *What's the time in London?* \(ロンドンの時刻は何時ですか?\)

    *What's the date?* \(何日ですか?\)

    *What date is Sunday?* \(日曜日は何日ですか?\)

    *What day is it?* \(何曜日ですか?\)

    *What day is 01/01/2025?* \(2025 年 1 月 1 日は何曜日ですか?\)

    > **注**: アプリケーションのロジックは意図的に単純であり、いくつかの制限があります。 たとえば、時間を取得する場合、制限された都市のセットのみがサポートされ、夏時間は無視されます。 目標は、アプリケーションが次のことを行う必要がある言語サービスを使用するための一般的なパターンの例を確認することです。
    >   1. 予測エンドポイントに接続します。
    >   2. 予測を得るために発話を送信します。
    >   3. 予測された意図とエンティティに適切に応答するロジックを実装します。

1. テストが終了したら、「*quit*」と入力します。

## リソースをクリーンアップする

Azure AI Language サービスの探索が終了したら、この演習で作成したリソースを削除できます。 方法は以下のとおりです。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
2. このラボで作成した Azure AI Language リソースを参照します。
3. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細情報

Azure AI Language における会話言語理解の詳細については、「[Azure AI Language のドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/overview)」をご覧ください。

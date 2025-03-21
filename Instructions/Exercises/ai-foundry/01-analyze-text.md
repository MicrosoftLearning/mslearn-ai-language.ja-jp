---
lab:
  title: テキストを分析する
  module: Module 3 - Develop natural language processing solutions
---

# テキストの分析

**Azure Language** は、言語検出、感情分析、キー フレーズ抽出、エンティティ認識など、テキストの分析をサポートします。

たとえば、旅行代理店が会社の Web サイトに送信されたホテルのレビューを処理したいとします。 Azure AI Language を使用すると、各レビューが書かれている言語、レビューの感情 (ポジティブ、ニュートラル、ネガティブ)、レビューで議論されている主なトピックを示す可能性のあるキー フレーズ、場所、ランドマーク、またはレビューで言及された人などの名前付きエンティティなどを特定できます。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションに **Azure AI Language サービス** リソースがまだない場合は、Azure サブスクリプションでプロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. **[リソースの作成]** を選択します。
1. 検索フィールドで、**言語サービス**を検索します。 次に、結果で、**[言語サービス]** の下の **[作成]** を選択します。
1. **[リソースの作成を続行する]** を選択します。
1. 次の設定を使用してリソースをプロビジョニングします。
    - **[サブスクリプション]**: *お使いの Azure サブスクリプション*。
    - **リソース グループ**: *リソース グループを選択または作成します*。
    - **[リージョン]**: *使用できるリージョンを選択します*。
    - **[名前]**: *一意の名前を入力します*。
    - **価格レベル**: **F0** (*無料*)、または F が利用できない場合は **S** (*標準*) を選択します。
    - **責任ある AI 通知**: 同意。
1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[リソース管理]** セクションで、**[キーとエンドポイント]** ページを表示します。 このページの情報は、演習の後半で必要になります。

## Visual Studio Code でアプリを開発する準備をする

Visual Studio Code を使用してテキスト分析アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

> **ヒント**: mslearn-ai-language** リポジトリを**既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
2. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
3. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。

    > **注**:Visual Studio Code に、開いているコードを信頼するかどうかを求めるポップアップ メッセージが表示された場合は、ポップアップの **[はい、作成者を信頼します]** オプションをクリックします。

4. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるプロンプトが表示された場合は、**[今はしない]** を選択します。

## アプリケーションを構成する

C# と Python の両方のアプリケーションと、要約のテストに使用するサンプル テキスト ファイルが提供されています。 どちらのアプリにも同じ機能があります。 まず、アプリケーションの主要な部分をいくつか完成させて、アプリケーションで Azure AI Language リソースを使用できるようにします。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/01-analyze-text** フォルダーを参照し、言語の設定に応じて **CSharp** または **Python** フォルダー、およびそれに含まれる **text-analysis** フォルダーを展開します。 各フォルダーには、Azure AI Language の Text Analytics 機能を統合するアプリの言語固有のファイルが含まれています。
2. コード ファイルが含まれている **text-analysis** フォルダーを右クリックし、統合ターミナルを開きます。 次に、言語設定に適合するコマンドを実行して、Azure AI Language の Text Analytics SDK パッケージをインストールします。 Python 演習では、`dotenv` パッケージもインストールします。

    **C#**:

    ```
    dotnet add package Azure.AI.TextAnalytics --version 5.3.0
    ```

    **Python**:

    ```
    pip install azure-ai-textanalytics==5.3.0
    pip install python-dotenv
    ```

3. **[エクスプローラー]** ペインの **text-analysis** フォルダーで、優先する言語の構成ファイルを開きます

    - **C#**: appsettings.json
    - **Python**: .env
    
4. 作成した Azure 言語リソースの**エンドポイント**と**キー**を含むように構成値を更新します (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで利用可能)。
5. 構成ファイルを保存します。

6. **text-analysis** フォルダーには、クライアント アプリケーションのコード ファイルが含まれていることにご注意ください。

    - **C#**: Program.cs
    - **Python**: text-analysis.py

    コード ファイルを開き、上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Text Analytics SDK を使用するために必要な名前空間インポートします。

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.TextAnalytics;
    ```

    **Python**: text-analysis.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

7. **Main** 関数で、構成ファイルから Azure AI Language サービスのエンドポイントとキーを読み込むためのコードが既に提供されていることに注意してください。 次に、**「エンドポイントとキーを使用してクライアントを作成する」** というコメントを見つけ、次のコードを追加して、Text Analysis API のクライアントを作成します。

    **C#**: Programs.cs

    ```C#
    // Create client using endpoint and key
    AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
    Uri endpoint = new Uri(aiSvcEndpoint);
    TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);
    ```

    **Python**: text-analysis.py

    ```Python
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

8. 変更を保存して、**text-analysis** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    - **C#**: `dotnet run`
    - **Python**: `python text-analysis.py`

    > **ヒント**: ターミナル ツールバーの **最大化パネル サイズ** (**^**) アイコンを使用すると、コンソール テキストをさらに表示できます。

9. コードがエラーなしで実行され、**reviews** フォルダー内の各レビュー テキストファイルの内容が表示されるので、出力を確認します。 アプリケーションは Text Analytics API のクライアントを正常に作成しますが、それを利用しません。 次の手順で修正します。

## 言語を検出するコードを追加する

API のクライアントを作成したので、それを使用して、各レビューが書かれている言語を検出します。

1. プログラムの **Main** 関数で、コメント **Get language** を見つけます。 次に、このコメントの下に、各レビュー ドキュメントで言語を検出するために必要なコードを追加します。

    **C#**: Programs.cs

    ```csharp
    // Get language
    DetectedLanguage detectedLanguage = aiClient.DetectLanguage(text);
    Console.WriteLine($"\nLanguage: {detectedLanguage.Name}");
    ```

    **Python**: text-analysis.py

    ```python
    # Get language
    detectedLanguage = ai_client.detect_language(documents=[text])[0]
    print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
    ```

     > **注**: *この例では、各レビューが個別に分析され、ファイルごとにサービスが個別に呼び出されます。別の方法として、ドキュメントのコレクションを作成し、1 回の呼び出しでサービスに渡す方法があります。どちらの方法でも、サービスからの応答はドキュメントのコレクションで構成されます。これは、上記の Python コードでは、応答 ([0]) 内の最初の (そして唯一の) ドキュメントのインデックスが指定されている理由です。*

1. 変更を保存します。 次に、**read-text** フォルダーの統合ターミナルに戻り、プログラムを再実行します。
1. 出力を観察します。今回は、各レビューの言語が識別されていることに注意してください。

## センチメントを評価するコードを追加する

"*感情分析*" は、テキストを "*ポジティブ*" または "*ネガティブ*" ("*ニュートラル*" または "*混合*" の場合もある) として分類するために一般的に使用される手法です。 ソーシャル メディアの投稿、製品レビュー、およびテキストの感情が有用な洞察を提供する可能性があるその他のアイテムを分析するために一般的に使用されます。

1. プログラムの **Main** 関数で、コメント **Get sentiment** を見つけます。 次に、このコメントの下に、各レビュードキュメントの感情を検出するために必要なコードを追加します。

    **C#**: Program.cs

    ```csharp
    // Get sentiment
    DocumentSentiment sentimentAnalysis = aiClient.AnalyzeSentiment(text);
    Console.WriteLine($"\nSentiment: {sentimentAnalysis.Sentiment}");
    ```

    **Python**: text-analysis.py

    ```python
    # Get sentiment
    sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
    print("\nSentiment: {}".format(sentimentAnalysis.sentiment))
    ```

1. 変更を保存します。 次に、**read-text** フォルダーの統合ターミナルに戻り、プログラムを再実行します。
1. 出力を観察し、レビューの感情が検出されたことに注意します。

## キー フレーズを識別するコードを追加する

テキストの本文でキー フレーズを特定すると、説明する主なトピックを特定するのに役立ちます。

1. プログラムの **Main** 関数で、コメント **Get key phrases** を見つけます。 次に、このコメントの下に、各レビュー ドキュメントのキー フレーズを検出するために必要なコードを追加します。

    **C#**: Program.cs

    ```csharp
    // Get key phrases
    KeyPhraseCollection phrases = aiClient.ExtractKeyPhrases(text);
    if (phrases.Count > 0)
    {
        Console.WriteLine("\nKey Phrases:");
        foreach(string phrase in phrases)
        {
            Console.WriteLine($"\t{phrase}");
        }
    }
    ```

    **Python**: text-analysis.py

    ```python
    # Get key phrases
    phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
    if len(phrases) > 0:
        print("\nKey Phrases:")
        for phrase in phrases:
            print('\t{}'.format(phrase))
    ```

1. 変更を保存します。 次に、**read-text** フォルダーの統合ターミナルに戻り、プログラムを再実行します。
1. 各ドキュメントにキー フレーズが含まれていることに注意して、出力を確認します。それはレビューが何であるかについてのいくつかの洞察を与えます。

## データを抽出するエンティティを追加する

多くの場合、ドキュメントまたはその他のテキスト本体は、人、場所、期間、またはその他のエンティティについて言及しています。 Text Analytics API は、テキスト内のエンティティの複数のカテゴリ (およびサブカテゴリ) を検出できます。

1. プログラムの **Main**関数で、コメント **Get entities** を見つけます。 次に、このコメントの下に、各レビューで言及されているエンティティを識別するために必要なコードを追加します。

    **C#**: Program.cs

    ```csharp
    // Get entities
    CategorizedEntityCollection entities = aiClient.RecognizeEntities(text);
    if (entities.Count > 0)
    {
        Console.WriteLine("\nEntities:");
        foreach(CategorizedEntity entity in entities)
        {
            Console.WriteLine($"\t{entity.Text} ({entity.Category})");
        }
    }
    ```

    **Python**: text-analysis.py

    ```python
    # Get entities
    entities = ai_client.recognize_entities(documents=[text])[0].entities
    if len(entities) > 0:
        print("\nEntities")
        for entity in entities:
            print('\t{} ({})'.format(entity.text, entity.category))
    ```

1. 変更を保存します。 次に、**read-text** フォルダーの統合ターミナルに戻り、プログラムを再実行します。
1. 出力を確認します。テキストで検出されたエンティティに注意してください。

## リンクされたエンティティを抽出するコードを追加する

分類されたエンティティに加えて、Text Analytics API は、Wikipedia などのデータソースへの既知のリンクがあるエンティティを検出できます。

1. プログラムの **Main** 関数で、コメント **Get linked entities** を見つけます。 次に、このコメントの下に、各レビューで言及されているリンクされたエンティティを識別するために必要なコードを追加します。

    **C#**: Program.cs

    ```csharp
    // Get linked entities
    LinkedEntityCollection linkedEntities = aiClient.RecognizeLinkedEntities(text);
    if (linkedEntities.Count > 0)
    {
        Console.WriteLine("\nLinks:");
        foreach(LinkedEntity linkedEntity in linkedEntities)
        {
            Console.WriteLine($"\t{linkedEntity.Name} ({linkedEntity.Url})");
        }
    }
    ```

    **Python**: text-analysis.py

    ```python
    # Get linked entities
    entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
    if len(entities) > 0:
        print("\nLinks")
        for linked_entity in entities:
            print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
    ```

1. 変更を保存します。 次に、**read-text** フォルダーの統合ターミナルに戻り、プログラムを再実行します。
1. 出力を確認します。識別されたリンクされたエンティティに注意してください。

## リソースをクリーンアップする

Azure AI Language サービス の調査が完了した場合は、この演習で作成したリソースを削除してください。 方法は以下のとおりです。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。

2. このラボで作成した Azure AI Language リソースを参照します。

3. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細

**Azure AI Language** の詳細については、「[ドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/)」を参照してください。

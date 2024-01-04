---
lab:
  title: カスタム エンティティを抽出する
  module: Module 3 - Getting Started with Natural Language Processing
---

# カスタム エンティティを抽出する

Azure AI Language サービスでは、他の自然言語処理機能に加えて、カスタム エンティティを定義してテキストからインスタンスを抽出できます。

カスタム エンティティ抽出をテストするため、モデルを作成し、Azure AI Language Studio を使用してトレーニングしてから、コマンド ライン アプリケーションを使用してテストします。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションにまだリソースがない場合は、**Azure AI Language サービス** リソースをプロビジョニングする必要があります。 さらに、カスタム テキスト分類を使用して、**カスタム テキスト分類および抽出**機能を有効にする必要があります。

1. ブラウザーで Azure portal (`https://portal.azure.com`) を開き、Microsoft アカウントを使用してサインインします。
1. **[リソースの作成]** ボタンを選択し、*Language* を検索して、**Azure AI Language サービス**のリソースを作成します。 *その他の機能*について質問されたら、**[カスタム テキスト分類および抽出]** を選択します。 次の設定を使用してリソースを作成します。
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **リソース グループ**: *リソース グループを選択または作成します*
    - **[リージョン]**: 使用できるリージョンを選択します**
    - **[名前]**: *一意の名前を入力します*
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **ストレージ アカウント**: 新しいストレージ アカウント
      - **ストレージ アカウント名**: "*一意の名前を入力します*"。
      - **ストレージ アカウントの種類**: 標準 LRS
    - **[責任ある AI に関する注意]**: オン。

1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## サンプル広告のアップロード

Azure AI Language サービスとストレージ アカウントを作成したら、後でモデルをトレーニングするためにサンプル広告をアップロードする必要があります。

1. 新しいブラウザー タブで、分類された広告のサンプルを `https://aka.ms/entity-extraction-ads` からダウンロードし、選択したフォルダーにファイルを抽出します。

2. Azure portal で、作成したストレージ アカウントに移動して選択します。

3. ストレージ アカウントで、**[設定]** の下にある **[構成]** を選択し、画面で **[BLOB 匿名アクセスを許可する]** オプションを有効にし、**[保存]** を選択します。

4. **[データ ストレージ]** の下にある、左側のメニューの **[コンテナー]** を選択します。 表示された画面で、**[+ コンテナー]** を選択します。 コンテナーに `classifieds` という名前を付け、**[匿名アクセス レベル]** を **[コンテナー (コンテナーと BLOB の匿名読み取りアクセス)]** に設定します。

    > **メモ**: 実際のソリューション用にストレージ アカウントを構成する場合は、適切なアクセス レベルを割り当てるように注意してください。 各アクセス レベルの詳細については、「[Azure Storage に関するドキュメント](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure)」をご覧ください。

5. コンテナーを作成したら、それを選択し、**[アップロード]** ボタンをクリックして、ダウンロードしたサンプル広告をアップロードします。

## カスタム固有表現認識プロジェクトを作成する

これで、カスタム固有表現認識プロジェクトを作成する準備ができました。 このプロジェクトによって、モデルのビルド、トレーニング、デプロイを行うための作業場所が提供されます。

> **メモ**: REST API を使用してモデルを作成、ビルド、トレーニング、デプロイすることもできます。

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

1. ポータルの上部にある **[新規作成]** メニューで、*[カスタム固有表現認識]** を選択します。

1. 次の設定で新しいプロジェクトを作成します。
    - **ストレージに接続する**: *この値は既に入力されている可能性があります。入力されていない場合は、値を「storage account」に変更します*
    - **基本情報**
    - **名前**: `CustomEntityLab`
        - **[Text primary language](テキストのプライマリ言語)**: 英語 (米国)
        - **データセットに同じ言語ではないドキュメントが含まれていますか?** : *いいえ*
        - **説明**: `Custom entities in classified ads`
    - **コンテナー**:
        - **BLOB ストア コンテナー**: 分類
        - **[Are your files labeled with classes?] (ファイルにはクラスでラベルが付いていますか?)**: [No, I need to label my files as part of this project] (いいえ、このプロジェクトの一部としてファイルにラベルを付ける必要があります)

## データにラベルを付ける

プロジェクトが作成されたので、テキストの識別方法をモデルにトレーニングするためにデータにラベルを付ける必要があります。

1. **[データのラベル付け]** ページがまだ開いていない場合は、左側のペインで **[データのラベル付け]** を選択します。 ストレージ アカウントにアップロードしたファイルの一覧が表示されます。
1. 右側にある **[アクティビティ]** ペインで、**[エンティティの追加]** を選択し、`ItemForSale` という名前を付けた新しいエンティティを追加します。
1.  前の手順を繰り返して、以下のエンティティを作成します。
    - `Price`
    - `Location`
1. 3 つのエンティティを作成したら、**Ad 1.txt** を選択して読むことができます。
1. *Ad 1.txt* 内で 
    1. *face cord of firewood* というテキストを強調表示し、**ItemForSale** エンティティを選択します。
    1. *Denver, CO* というテキストを強調表示し、**場所**エンティティを選択します。
    1. *$90* というテキストを強調表示し、**価格**エンティティを選択します。
1. **[アクティビティ]** ペインで、モデルをトレーニングするためにこのドキュメントがデータセットに追加されることに注意してください。
1. **[次のドキュメント]** ボタンをクリックして次のドキュメントに移動し、一連のドキュメント全体の適切なエンティティにテキストを割り当て続け、それらすべてをトレーニング データセットに追加します。
1. 最後のドキュメント (*Ad 9.txt*) にラベルを付けたら、ラベルを保存します。

## モデルをトレーニングする

データにラベルを付けた後、モデルをトレーニングする必要があります。

1. 左側のペインで、**[トレーニング ジョブ]** を選択します。
2. **[トレーニング ジョブの開始]** を選択します。
3. `ExtractAds` という名前が付いた新しいモデルをトレーニングするオプションを選択します
4. **[テスト セットをトレーニング データから自動的に分割する]** を選択します

    > **ヒント**: 独自の抽出プロジェクトでは、データに最適なテスト分割を使用します。 データの一貫性を高め、データセットを大きくするために、Azure AI Languag サービスはテスト セットをパーセンテージで自動的に分割します。 データセットが小さい場合は、適切な種類の入力ドキュメントを使用してトレーニングすることが重要です。

5. **[トレーニング]** をクリックします

    > **重要**: モデルのトレーニングには、数分かかる場合があります。 完了すると、通知が表示されます。

## モデルを評価する

テキスト分類の実際のアプリケーションでは、モデルを評価して改善し、想定どおりに機能していることを確認することが重要です。 左側の 2 つのページには、トレーニング済みのモデルの詳細と、失敗したテストが表示されます。

左側メニューの **[モデル パフォーマンス]** を選択し、ご利用の `ExtractAds` モデルを選択します。 モデルのスコア、パフォーマンス メトリクス、トレーニングされた日時を確認できます。 どのテスト ドキュメントでエラーが生じたのかを確認できます。これらのエラーは、改善すべき場所を理解するのに役立ちます。

## モデルをデプロイする

モデルのトレーニングに問題がなければ、デプロイします。これにより、API を使用してテキストの分類を開始できます。

1. 左側のパネルで、**[モデルのデプロイ]** を選択します。
2. **[デプロイの追加]** を選択し、名前「`AdEntities`」を入力し、**ExtractAds** モデルを選択します。
3. **[デプロイ]** をクリックしてモデルをデプロイします。

## Visual Studio Code でアプリの開発準備をする

Azure AI Language サービスのカスタム エンティティ抽出機能をテストするには、Visual Studio Code で簡単なコンソール アプリケーションを開発します。

> **ヒント**: **mslearn-ai-language** リポジトリを既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
2. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
3. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。
4. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるダイアログが表示された場合は、 **[今はしない]** を選択します。

## アプリケーションの構成

C# と Python の両方のアプリケーションと、要約のテストに使用するサンプル テキスト ファイルが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI Language リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/05-custom-entity-recognition** フォルダーを参照し、言語の設定とそこに含まれている **custom-entities** フォルダーに応じて **C-Sharp** または **Python** フォルダーを展開します。 各フォルダーには、Azure AI Language テキスト分類機能を統合するアプリの言語固有のファイルが含まれています。
1. コード ファイルを含む **custom-entities** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適したコマンドを実行して、Azure AI Language Text Analytics SDK パッケージをインストールします。

    **C#:**

    ```
    dotnet add package Azure.AI.TextAnalytics --version 5.3.0
    ```

    **Python**:

    ```
    pip install azure-ai-textanalytics==5.3.0
    ```

1. **[エクスプローラー]** ペインの **custom-entities** フォルダーで、優先する言語の構成ファイルを開きます。

    - **C#** : appsettings.json
    - **Python**: .env
    
1. 構成値を更新して、作成した Azure Language リソースの**エンドポイント**と**キー**を含めます (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで使用できます)。 ファイルには、カスタム エンティティ抽出モデルのプロジェクト名とデプロイ名が既に含まれている必要があります。
1. 構成ファイルを保存します。

## エンティティを抽出するコードを追加する

これで、Azure AI Language サービスを使用してテキストからカスタム エンティティを抽出する準備ができました。

1. **custom-entities** フォルダー内の **ads** フォルダーを展開して、アプリケーションで分析する案内広告を表示します。
1. **custom-entities** フォルダーで、クライアント アプリケーションのコード ファイルを開きます。

    - **C#** : Program.cs
    - **Python**: custom-entities.py

1. 「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Text Analytics SDK を使用するために必要な名前空間インポートします。

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.TextAnalytics;
    ```

    **Python**: custom-entities.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. **Main** 関数で、構成ファイルから Azure AI Language サービスのエンドポイントとキーおよびプロジェクト名とデプロイ名を読み込むためのコードが既に提供されていることに注意してください。 次に、**エンドポイントとキーを使用してクライアントを作成する**というコメントを見つけ、次のコードを追加して、Text Analysis API のクライアントを作成します。

    **C#**: Programs.cs

    ```csharp
    // Create client using endpoint and key
    AzureKeyCredential credentials = new(aiSvcKey);
    Uri endpoint = new(aiSvcEndpoint);
    TextAnalyticsClient aiClient = new(endpoint, credentials);
    ```

    **Python**: custom-entities.py

    ```Python
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. **Main** 関数で、既存のコードが **articles** フォルダー内のすべてのファイルを読み取り、その内容を含むリストを作成することに注意してください。 C# コードの場合、**TextDocumentInput** オブジェクトの一覧を使用して、ファイル名を ID と言語として含めます。 Python では、テキスト コンテンツの単純なリストが使用されます。
1. 「**Extract entities**」というコメントを見つけて、次のコードを追加します。

    **C#** : Program.cs

    ```csharp
    // Extract entities
    RecognizeCustomEntitiesOperation operation = await aiClient.RecognizeCustomEntitiesAsync(WaitUntil.Completed, batchedDocuments, projectName, deploymentName);

    await foreach (RecognizeCustomEntitiesResultCollection documentsInPage in operation.Value)
    {
        foreach (RecognizeEntitiesResult documentResult in documentsInPage)
        {
            Console.WriteLine($"Result for \"{documentResult.Id}\":");

            if (documentResult.HasError)
            {
                Console.WriteLine($"  Error!");
                Console.WriteLine($"  Document error code: {documentResult.Error.ErrorCode}");
                Console.WriteLine($"  Message: {documentResult.Error.Message}");
                Console.WriteLine();
                continue;
            }

            Console.WriteLine($"  Recognized {documentResult.Entities.Count} entities:");

            foreach (CategorizedEntity entity in documentResult.Entities)
            {
                Console.WriteLine($"  Entity: {entity.Text}");
                Console.WriteLine($"  Category: {entity.Category}");
                Console.WriteLine($"  Offset: {entity.Offset}");
                Console.WriteLine($"  Length: {entity.Length}");
                Console.WriteLine($"  ConfidenceScore: {entity.ConfidenceScore}");
                Console.WriteLine($"  SubCategory: {entity.SubCategory}");
                Console.WriteLine();
            }

            Console.WriteLine();
        }
    }
    ```

    **Python**: custom-entities.py

    ```Python
    # Extract entities
    operation = ai_client.begin_recognize_custom_entities(
        batchedDocuments,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = operation.result()

    for doc, custom_entities_result in zip(files, document_results):
        print(doc)
        if custom_entities_result.kind == "CustomEntityRecognition":
            for entity in custom_entities_result.entities:
                print(
                    "\tEntity '{}' has category '{}' with confidence score of '{}'".format(
                        entity.text, entity.category, entity.confidence_score
                    )
                )
        elif custom_entities_result.is_error is True:
            print("\tError with code '{}' and message '{}'".format(
                custom_entities_result.error.code, custom_entities_result.error.message
                )
            )
    ```

1. 変更内容をコード ファイルに保存します。

## アプリケーションのテスト

これでアプリケーションをテストする準備ができました。

1. **classify-text** フォルダーの統合ターミナルで、次のコマンドを入力してプログラムを実行します。

    - **C#** : `dotnet run`
    - **Python**: `python custom-entities.py`

    > **ヒント**: [ターミナル] ツールバーの **最大化パネル サイズ** (**^**) アイコンを使用すると、コンソール テキストをさらに表示できます。

1. 出力を確認します。 アプリケーションでは、各テキスト ファイルで見つかったエンティティの詳細を一覧表示する必要があります。

## クリーンアップ

プロジェクトが必要なくなったら、Language Studio の **[プロジェクト]** ページから削除できます。 [Azure portal](https://portal.azure.com) でも、Azure AI Language サービスと関連付けられたストレージ アカウントを削除できます。

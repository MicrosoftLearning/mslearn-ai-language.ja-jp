---
lab:
  title: カスタム テキスト分類
  module: Module 3 - Getting Started with Natural Language Processing
---

# カスタム テキスト分類

Azure AI Language には、キー フレーズ特定、テキスト要約、感情分析など、いくつかの NLP 機能があります。 この Language サービスには、カスタムの質問応答やカスタム テキスト分類などのカスタム機能も用意されています。

Azure AI Language サービスのカスタム テキスト分類をテストするために、ここでは Language Studio を使ってモデルを構成した後、Cloud Shell で実行される小さなコマンドライン アプリケーションを使ってそれをテストします。 ここで使用するものと同じパターンと機能を実際のアプリケーションでも使用できます。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションにまだリソースがない場合は、**Azure AI Language サービス** リソースをプロビジョニングする必要があります。 さらに、カスタム テキスト分類を使用して、**カスタム テキスト分類と抽出**機能を有効にする必要があります。

1. ブラウザーで Azure portal (`https://portal.azure.com`) を開き、Microsoft アカウントを使用してサインインします。
1. ポータルの上部にある検索フィールドを選び、`Azure AI services` を検索し、**言語サービス** リソースを作成します。
1. **[カスタム テキスト分類]** を含むボックスを選びます。 **[リソースの作成を続行する]** を選びます。
1. 次の設定を使ってリソースを作成します。
    - **[サブスクリプション]**: *お使いの Azure サブスクリプション*。
    - **リソース グループ**: *リソース グループを選択または作成します*。
    - **リージョン**: *次のいずれかのリージョンから選択します。*\*
        - オーストラリア東部
        - インド中部
        - 米国東部
        - 米国東部 2
        - 北ヨーロッパ
        - 米国中南部
        - スイス北部
        - 英国南部
        - 西ヨーロッパ
        - 米国西部 2
        - 米国西部 3
    - **[名前]**: *一意の名前を入力します*。
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **ストレージ アカウント**: 新しいストレージ アカウント
      - **ストレージ アカウント名**: "*一意の名前を入力します*"。
      - **[ストレージ アカウントの種類]**: 標準 LRS
    - **[責任ある AI に関する注意]**: オン。

1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## ユーザーのロール
> **注**: この手順をスキップした場合、カスタム プロジェクトに接続しようとすると 403 エラーが発生します。 自分がストレージ アカウントの所有者であっても、現在のユーザーがストレージ アカウント BLOB データにアクセスするためにこのロールを持っていることが重要です。**

1. Azure portal でストレージ アカウントのページに移動します。
2. 左側のナビゲーション メニューで **[アクセス制御 (IAM)]** を選択します。
3. **[追加]** を選択してロールの割り当てを追加し、ストレージ アカウントに対して**ストレージ BLOB データ共同作成者**ロールを選択します。
4. **[アクセスの割り当て先]** 内で、**[ユーザー、グループ、またはサービス プリンシパル]** を選択します。
5. **[メンバーの選択]** を選びます。
6. ユーザーを選択します。 **[選択]** フィールドでユーザー名を検索できます。

## サンプル記事をアップロードする

Azure AI Language サービスとストレージ アカウントを作成したら、後でモデルをトレーニングするためのサンプル記事をアップロードする必要があります。

1. 新しいブラウザー タブで、`https://aka.ms/classification-articles` からサンプル記事をダウンロードし、選択したフォルダーにファイルを抽出します。

1. Azure portal で、作成したストレージ アカウントに移動して選択します。

1. ストレージ アカウントで、**[設定]** の下にある **[構成]** を選択します。 [構成] 画面で、**[BLOB 匿名アクセスを許可する]** オプションを有効にし、**[保存]** を選択します。

1. **[データ ストレージ]** の下にある、左側のメニューの **[コンテナー]** を選択します。 表示された画面で、**[+ コンテナー]** を選択します。 コンテナーに `articles` という名前を付け、**[匿名アクセス レベル]** を **[コンテナー (コンテナーと BLOB の匿名読み取りアクセス)]** に設定します。

    > **注**: 実際のソリューション用にストレージ アカウントを構成する場合は、適切なアクセス レベルを割り当てるように注意してください。 各アクセス レベルの詳細については、「[Azure Storage に関するドキュメント](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure)」をご覧ください。

1. コンテナーを作成したら、それを選び、**[アップロード]** ボタンを選びます。 **[ファイルの参照]** を選んで、ダウンロードしたサンプル記事を参照します。 **[アップロード]** を選択します。

## カスタム テキスト分類プロジェクトを作成する

構成が完了したら、カスタム テキスト分類プロジェクトを作成します。 このプロジェクトによって、モデルのビルド、トレーニング、デプロイを行うための作業場所が提供されます。

> **注**: このラボでは、**Language Studio** を使用しますが、REST API を使用してモデルの作成、ビルド、トレーニング、デプロイを行うこともできます。

1. 新しいブラウザー タブで Azure AI Language ポータル (`https://language.cognitive.azure.com/`) を開き、お使いの Azure サブスクリプションに関連付けられている Microsoft アカウントを使ってサインインします。
1. 言語リソースの選択を求めるメッセージが表示されたら、次の設定を選択します。

    - **Azure ディレクトリ**: ご利用のサブスクリプションを含む Azure ディレクトリ
    - **Azure サブスクリプション**: ご利用の Azure サブスクリプション
    - **リソースの種類**: 言語。
    - **言語リソース**: 以前に作成した Azure AI Language リソース。

    言語リソースの選択を求めるメッセージが表示<u>されない</u>場合、原因として、お使いのサブスクリプションに複数の言語リソースが存在していることが考えられます。その場合は、次の操作を行います。

    1. ページの上部にあるバーで、**[設定] (&#9881;)** ボタンを選択します。
    2. **[設定]** ページで、**[リソース]** タブを表示します。
    3. 作成したばかりの言語リソースを選択し、**[リソースの切り替え]** をクリックします。
    4. ページの上部で、**[Language Studio]** をクリックして、Language Studio のホーム ページに戻ります。

1. ポータルの上部にある **[新規作成]** メニューで、**[カスタム テキスト分類]** を選択します。
1. **[記憶域への接続]** ページが表示されます。 すべての値は既に入力されています。 そのため、**[次へ]** を選びます。
1. **[プロジェクト タイプの選択]** ページで、**[単一ラベル分類]** を選びます。 **[次へ]** を選択します。
1. **[基本情報の入力]** ペインで以下を設定します。
    - **名前**: `ClassifyLab`  
    - **テキストのプライマリ言語**: 英語 (米国)
    - **説明**: `Custom text lab`

1. [**次へ**] を選択します。
1. **[コンテナーの選択]** ページで、**[BLOB ストレージ コンテナー]** ドロップダウンをお使いの*記事*コンテナーに設定します。
1. **[No, I need to label my files as part of this project] (いいえ、このプロジェクトの一部としてファイルにラベルを付ける必要があります)** オプションを選びます。 **[次へ]** を選択します。
1. **[プロジェクトの作成]** を選択します。

> **ヒント**: "この操作を実行する権限がありません" というエラー メッセージを受信した場合は、ロールの割り当てを追加する必要があります。 このエラーを修正するために、ラボを実行しているユーザーのストレージ アカウントに "ストレージ Blob データ共同作成者" ロールを追加します。 詳細については、[こちらのドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)を参照してください。

## データにラベルを付ける

プロジェクトが作成されたので、テキストの分類方法をモデルにトレーニングするためにデータにラベル (タグ) を付ける必要があります。

1. 左側にある **[データのラベル付け]** をまだ選んでいない場合は選びます。 ストレージ アカウントにアップロードしたファイルの一覧が表示されます。
1. 右側にある **[アクティビティ]** ペインで **[+ クラスの追加]** を選びます。  このラボの記事は、4 つのクラスに分類されるため、`Classifieds`、`Sports`、`News`、`Entertainment` を作成する必要があります。

    ![タグ データ ページとクラスの追加ボタンを示すスクリーンショット。](../media/tag-data-add-class-new.png#lightbox)

1. 4 つのクラスを作成したら、**[Article 1] (記事 1)** を選んで開始します。 ここでは、この記事を読み、このファイルがどのクラスであるか、そしてどのデータセット (トレーニングまたはテスト) に割り当てるかを定義できます。
1. 右側にある **[アクティビティ]** ペインを使って、各記事に適切なクラスとデータセット (トレーニングまたはテスト) を割り当てます。  右側にあるラベルの一覧からラベルを選び、[アクティビティ] ペインの下部にあるオプションを使って、各記事を**トレーニング**または**テスト**に設定できます。 **[次のドキュメント]** を選んで次のドキュメントに移動します。 このラボの目的として、モデルのトレーニングとモデルのテストのどちらに使うかを定義します。

    | [アーティクル]  | クラス  | データセット  |
    |---------|---------|---------|
    | Article 1 | スポーツ | トレーニング |
    | Article 10 | News | トレーニング |
    | Article 11 | エンターテイメント | テスト |
    | Article 12 | News | テスト |
    | Article 13 | スポーツ | テスト |
    | Article 2 | スポーツ | トレーニング |
    | Article 3 | 案内広告 | トレーニング |
    | Article 4 | 案内広告 | トレーニング |
    | Article 5 | エンターテイメント | トレーニング |
    | Article 6 | エンターテイメント | トレーニング |
    | Article 7 | News | トレーニング |
    | Article 8 | News | トレーニング |
    | Article 9 | エンターテイメント | トレーニング |

    > **注** Language Studio ではファイルがアルファベット順に表示されるため、上記の一覧は順番に並んでいません。 記事にラベルを付けるときは、必ずドキュメントの両方のページにアクセスしてください。

1. **[ラベルの保存]** を選んでラベルを保存します。

## モデルをトレーニングする

データにラベルを付けた後、モデルをトレーニングする必要があります。

1. 左側のメニューで **[トレーニング ジョブ]** を選びます。
1. **[トレーニング ジョブの開始]** を選択します。
1. `ClassifyArticles` という名前の新しいモデルをトレーニングします。
1. **[トレーニングおよびテスト データの手動分割を使用する]** を選びます。

    > **ヒント** 独自の分類プロジェクトでは、Azure AI Language サービスは、テスト用セットを大規模なデータセットで有用なパーセンテージで自動的に分割します。 小規模なデータセットでは、適切なクラス分布でトレーニングすることが重要です。

1. [**トレーニング**] を選択します。

> **重要** モデルのトレーニングには、数分かかる場合があります。 完了すると、通知が表示されます。

## モデルを評価する

テキスト分類の実際のアプリケーションでは、モデルを評価して改善し、想定どおりに機能していることを確認することが重要です。

1. **[モデルのパフォーマンス]** を選んで、**ClassifyArticles** モデルを選びます。 モデルのスコア、パフォーマンス メトリクス、トレーニングされた日時を確認できます。 モデルのスコアリングが 100% ではない場合、テストに使われたドキュメントのいずれかが、ラベル付けされたとおりに評価されなかったことを意味します。 これらのエラーは、改善すべき点を理解するのに役立ちます。
1. **[テスト セットの詳細]** タブを選びます。エラーがある場合、このタブで、テスト対象として指定した記事と、モデルによってどのように予測されたか、それがテスト ラベルと矛盾するかどうかを確認できます。 既定値では、このタブには正しくない予測のみが表示されます。 **[不一致のみを表示する]** オプションを切り替えると、テスト対象として指定したすべての記事と、それぞれがどのように予測されたかを確認できます。

## モデルをデプロイする

モデルのトレーニングに問題がなければ、デプロイします。これにより、API を使用してテキストの分類を開始できます。

1. 左側のパネルで、**[Deploying model] (モデルのデプロイ)** を選びます。
1. **[デプロイの追加]** を選択し、**[新しいデプロイ名の作成]** フィールドに「`articles`」と入力し、**[モデル]** フィールドで **[ClassifyArticles]** を選択します。
1. **[デプロイ]** を選んでモデルをデプロイします。
1. モデルがデプロイされたら、そのページを開いたままにします。 次の手順で、このプロジェクトとデプロイの名前が必要になります。

## Visual Studio Code でアプリの開発準備をする

Azure AI Language サービスのカスタム テキスト分類機能をテストするには、Visual Studio Code で簡単なコンソール アプリケーションを開発します。

> **ヒント**: **mslearn-ai-language** リポジトリを既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
2. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
3. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。

    > **注**:Visual Studio Code に、開いているコードを信頼するかどうかを求めるポップアップ メッセージが表示された場合は、ポップアップの **[はい、作成者を信頼します]** オプションをクリックします。

4. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるプロンプトが表示された場合は、**[今はしない]** を選択します。

## アプリケーションを構成する

C# と Python の両方のアプリケーションと、要約のテストに使用するサンプル テキスト ファイルが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI Language リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/04-text-classification** フォルダーを参照し、言語の設定に応じて **C-Sharp** または **Python** フォルダーと、そこに含まれている **classify-text** フォルダーを展開します。 各フォルダーには、Azure AI Language テキスト分類機能を統合するアプリの言語固有のファイルが含まれています。
1. コード ファイルを含む **classify-text** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適合するコマンドを実行して、Azure AI Language Text Analytics SDK パッケージをインストールします。

    **C#**:

    ```
    dotnet add package Azure.AI.TextAnalytics --version 5.3.0
    ```

    **Python**:

    ```
    pip install azure-ai-textanalytics==5.3.0
    ```

1. **[エクスプローラー]** ペインの **classify-text** フォルダーで、優先する言語の構成ファイルを開きます

    - **C#**: appsettings.json
    - **Python**: .env
    
1. 構成値を更新して、作成した Azure Language リソースの**エンドポイント**と**キー**を含めます (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで使用できます)。 ファイルには、テキスト分類モデルのプロジェクト名とデプロイ名が既に含まれている必要があります。
1. 構成ファイルを保存します。

## ドキュメントを分類するコードを追加する

これで、Azure AI Language サービスを使用してドキュメントを分類する準備ができました。

1. **classify-text** フォルダー内の **articles** フォルダーを展開して、アプリケーションで分類するテキスト記事を表示します。
1. **classify-text** フォルダーで、クライアント アプリケーションのコード ファイルを開きます。

    - **C#** : Program.cs
    - **Python**: classify-text.py

1. 「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Text Analytics SDK を使用するために必要な名前空間インポートします。

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.TextAnalytics;
    ```

    **Python**: classify-text.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. **Main** 関数で、構成ファイルから Azure AI Language サービスのエンドポイントとキーおよびプロジェクト名とデプロイ名を読み込むためのコードが既に提供されていることに注意してください。 次に、**「エンドポイントとキーを使用してクライアントを作成する」** というコメントを見つけ、次のコードを追加して、Text Analysis API のクライアントを作成します。

    **C#**: Programs.cs

    ```csharp
    // Create client using endpoint and key
    AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
    Uri endpoint = new Uri(aiSvcEndpoint);
    TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);
    ```

    **Python**: classify-text.py

    ```Python
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. **Main** 関数で、既存のコードが **articles** フォルダー内のすべてのファイルを読み取り、その内容を含むリストを作成することに注意してください。 次に、「**Get Classifications**」というコメントを見つけて、次のコードを追加します。

    **C#** : Program.cs

    ```csharp
    // Get Classifications
    ClassifyDocumentOperation operation = await aiClient.SingleLabelClassifyAsync(WaitUntil.Completed, batchedDocuments, projectName, deploymentName);

    int fileNo = 0;
    await foreach (ClassifyDocumentResultCollection documentsInPage in operation.Value)
    {
        
        foreach (ClassifyDocumentResult documentResult in documentsInPage)
        {
            Console.WriteLine(files[fileNo].Name);
            if (documentResult.HasError)
            {
                Console.WriteLine($"  Error!");
                Console.WriteLine($"  Document error code: {documentResult.Error.ErrorCode}");
                Console.WriteLine($"  Message: {documentResult.Error.Message}");
                continue;
            }

            Console.WriteLine($"  Predicted the following class:");
            Console.WriteLine();

            foreach (ClassificationCategory classification in documentResult.ClassificationCategories)
            {
                Console.WriteLine($"  Category: {classification.Category}");
                Console.WriteLine($"  Confidence score: {classification.ConfidenceScore}");
                Console.WriteLine();
            }
            fileNo++;
        }
    }
    ```
    
    **Python**: classify-text.py

    ```Python
    # Get Classifications
    operation = ai_client.begin_single_label_classify(
        batchedDocuments,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = operation.result()

    for doc, classification_result in zip(files, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("{} was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score)
            )
        elif classification_result.is_error is True:
            print("{} has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message)
            )
    ```

1. 変更内容をコード ファイルに保存します。

## アプリケーションのテスト

これで、アプリケーションをテストする準備が整いました。

1. **read-text** フォルダーの統合ターミナルで、次のコマンドを入力してプログラムを実行します。

    - **C#**: `dotnet run`
    - **Python**: `python classify-text.py`

    > **ヒント**: ターミナル ツールバーの**パネル サイズの最大化** (**^**) アイコンを使用すると、コンソール テキストをさらに表示できます。

1. 出力を確認します。 アプリケーションは、各テキスト ファイルの分類と信頼度スコアを一覧表示します。


## クリーンアップ

プロジェクトが必要なくなったら、Language Studio の **[プロジェクト]** ページから削除できます。 [Azure portal](https://portal.azure.com) でも、Azure AI Language サービスと関連付けられたストレージ アカウントを削除できます。

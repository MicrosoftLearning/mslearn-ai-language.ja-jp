---
lab:
  title: カスタム エンティティを抽出する
  description: Azure AI Language を使用してテキスト入力からカスタマイズされたエンティティを抽出するモデルをトレーニングします。
---

# カスタム エンティティを抽出する

Azure AI Language サービスでは、他の自然言語処理機能に加えて、カスタム エンティティを定義し、テキストからそのインスタンスを抽出できます。

カスタム エンティティ抽出をテストするため、モデルを作成し、Azure AI Language スタジオを使用してトレーニングしてから、Python アプリケーションを使用してテストします。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用してテキスト分類アプリケーションを開発できます。

- [Python 用 Azure AI Text Analytics クライアント ライブラリ](https://pypi.org/project/azure-ai-textanalytics/)
- [.NET 用 Azure AI Text Analytics クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.TextAnalytics)
- [JavaScript 用 Azure AI Text Analytics クライアント ライブラリ](https://www.npmjs.com/package/@azure/ai-text-analytics)

この演習は約 **35** 分かかります。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションにまだリソースがない場合は、**Azure AI Language サービス** リソースをプロビジョニングする必要があります。 さらに、カスタム テキスト分類を使用して、**カスタム テキスト分類と抽出**機能を有効にする必要があります。

1. ブラウザーで Azure portal (`https://portal.azure.com`) を開き、Microsoft アカウントを使用してサインインします。
1. **[リソースの作成]** ボタンを選択し、*Language* を検索して、**[Language サービス]** のリソースを作成します。 *[追加機能の選択]* ページで、**カスタム固有表現認識**が含まれるカスタム機能を選択します。 次の設定を使用してリソースを作成します。
    - **[サブスクリプション]**: *ご自身の Azure サブスクリプション*
    - **[リソース グループ]**: *リソース グループを選択または作成します*
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
    - **[名前]**: *一意の名前を入力します*
    - **[価格レベル]**: **F0** (*Free*) を選択します。F が使用できない場合は **S** (*Standard*) を選択します。
    - **[ストレージ アカウント]**: 新しいストレージ アカウント:
      - **[ストレージ アカウント名]**: *一意の名前を入力します*。
      - **[ストレージ アカウントの種類]**: 標準 LRS
    - **[責任ある AI に関する注意]**: オン。

1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## ユーザーのロールベースのアクセスを構成する

> **注**: この手順をスキップした場合、カスタム プロジェクトに接続しようとすると 403 エラーが発生します。 自分がストレージ アカウントの所有者であっても、現在のユーザーがストレージ アカウント BLOB データにアクセスするためにこのロールを持っていることが重要です。

1. Azure portal でストレージ アカウントのページに移動します。
2. 左側のナビゲーション メニューで **[アクセス制御 (IAM)]** を選択します。
3. **[追加]** を選択してロールの割り当てを追加し、ストレージ アカウントに対して**ストレージ BLOB データ共同作成者**ロールを選択します。
4. **[アクセスの割り当て先]** 内で、**[ユーザー、グループ、またはサービス プリンシパル]** を選択します。
5. **[メンバーの選択]** を選択します。
6. ユーザーを選択します。 **[選択]** フィールドでユーザー名を検索できます。

## サンプル広告のアップロード

Azure AI Language サービスとストレージ アカウントを作成したら、後でモデルをトレーニングするためにサンプル広告をアップロードする必要があります。

1. 新しいブラウザー タブで、分類された広告のサンプルを `https://aka.ms/entity-extraction-ads` からダウンロードし、選択したフォルダーにファイルを抽出します。

2. Azure portal で、作成したストレージ アカウントに移動して選択します。

3. ストレージ アカウントで、**[設定]** の下にある **[構成]** を選択し、画面で **[BLOB 匿名アクセスを許可する]** オプションを有効にし、**[保存]** を選択します。

4. 左側のメニューの **[データ ストレージ]** の下にある **[コンテナー]** を選択します。 表示された画面で、**[+ コンテナー]** を選択します。 コンテナーに `classifieds` という名前を付け、**[匿名アクセス レベル]** を **[コンテナー (コンテナーと BLOB の匿名読み取りアクセス)]** に設定します。

    > **注**: 実際のソリューション用にストレージ アカウントを構成する場合は、適切なアクセス レベルを割り当てるように注意してください。 各アクセス レベルの詳細については、[Azure Storage のドキュメント](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure)を参照してください。

5. コンテナーを作成したら、それを選択し、**[アップロード]** ボタンをクリックして、ダウンロードしたサンプル広告をアップロードします。

## カスタム固有表現認識プロジェクトを作成する

これでカスタム固有表現認識プロジェクトを作成する準備ができました。 このプロジェクトによって、モデルのビルド、トレーニング、デプロイを行うための作業場所が提供されます。

> **注**: REST API を使用してモデルを作成、ビルド、トレーニング、デプロイすることもできます。

1. 新しいブラウザー タブで Azure AI Language Studio ポータル (`https://language.cognitive.azure.com/`) を開き、お使いの Azure サブスクリプションに関連付けられている Microsoft アカウントを使ってサインインします。
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

1. ポータルの上部にある **[新規作成]** メニューで、**[カスタム固有表現認識]** を選択します。

1. 次の設定で新しいプロジェクトを作成します。
    - **ストレージに接続する**: *この値は既に入力されている可能性があります。入力されていない場合は、ストレージ アカウントに変更します*
    - **基本情報**
    - **名前**: `CustomEntityLab`
        - **テキストのプライマリ言語**: 英語 (米国)
        - **データセットに同じ言語ではないドキュメントが含まれていますか?** : *いいえ*
        - **説明**: `Custom entities in classified ads`
    - **コンテナー**:
        - **BLOB ストア コンテナー**: 分類
        - **ファイルにはクラスでラベルが付いていますか?**: いいえ、このプロジェクトの一部としてファイルにラベルを付ける必要があります

> **ヒント**: "この操作を実行する権限がありません" というエラー メッセージを受信した場合は、ロールの割り当てを追加する必要があります。 このエラーを修正するために、ラボを実行しているユーザーのストレージ アカウントに "ストレージ Blob データ共同作成者" ロールを追加します。 詳細については、[こちらのドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)を参照してください。

## データにラベルを付ける

プロジェクトが作成されたので、テキストの識別方法をモデルにトレーニングするためにデータにラベルを付ける必要があります。

1. **[データのラベル付け]** ページがまだ開いていない場合は、左側のウィンドウで **[データのラベル付け]** を選択します。 ストレージ アカウントにアップロードしたファイルの一覧が表示されます。
1. 右側にある **[アクティビティ]** ウィンドウで、**[エンティティの追加]** を選択し、`ItemForSale` という名前の新しいエンティティを追加します。
1.  前の手順を繰り返して、以下のエンティティを作成します。
    - `Price`
    - `Location`
1. 3 つのエンティティを作成したら、**Ad 1.txt** を選択して読むことができます。
1. *Ad 1.txt* の場合: 
    1. *face cord of firewood* というテキストを強調表示し、**ItemForSale** エンティティを選択します。
    1. *Denver, CO* というテキストを強調表示し、**Location** エンティティを選択します。
    1. テキスト *$90* を強調表示し、**Price** エンティティを選択します。
1. **[アクティビティ]** ペインで、このドキュメントがモデルのトレーニング用のデータセットに追加されることに注意してください。
1. **[次のドキュメント]** ボタンを使用して次のドキュメントに移動し、ドキュメントのセット全体で適切なエンティティにテキストを割り当て続け、それらをすべてトレーニング データセットに追加します。
1. 最後のドキュメント (*Ad 9.txt)* にラベルを付けたら、ラベルを保存します。

## モデルをトレーニングする

データにラベルを付けた後、モデルをトレーニングする必要があります。

1. 左側のウィンドウで **[トレーニング ジョブ]** を選択します。
2. **[トレーニング ジョブの開始]** を選択します
3. `ExtractAds` という名前の新しいモデルをトレーニングする 
4. **[テスト セットをトレーニング データから自動的に分割する]** を選択します

    > **ヒント**: 独自の抽出プロジェクトでは、データに最適なテスト分割を使用します。 データの一貫性を高め、データセットを大きくするために、Azure AI Languag サービスはテスト セットをパーセンテージで自動的に分割します。 データセットが小さい場合は、適切な種類の入力ドキュメントを使用してトレーニングすることが重要です。

5. **[トレーニング]** をクリックします

    > **重要**: モデルのトレーニングには、数分かかる場合があります。 完了すると、通知が表示されます。

## モデルを評価する

テキスト分類の実際のアプリケーションでは、モデルを評価して改善し、想定どおりに機能していることを確認することが重要です。 左側の 2 つのページには、トレーニング済みのモデルの詳細と、失敗したテストが表示されます。

左側メニューの **[モデル パフォーマンス]** を選択し、ご利用の `ExtractAds` モデルを選択します。 モデルのスコア、パフォーマンス メトリクス、トレーニングされた日時を確認できます。 どのテスト ドキュメントでエラーが生じたのかを確認できます。これらのエラーは、改善すべき場所を理解するのに役立ちます。

## モデルをデプロイする

モデルのトレーニングに問題がなければ、デプロイします。これにより、API を使用してテキストの分類を開始できます。

1. 左側のウィンドウで、**[モデルのデプロイ]** を選択します。
2. **[デプロイの追加]** を選択し、名前 `AdEntities` を入力し、**ExtractAds** モデルを選択します
3. **[デプロイ]** をクリックしてモデルをデプロイします。

## Cloud Shell でアプリを開発する準備をする

Azure AI Language サービスのカスタム エンティティ抽出機能をテストするため、Azure Cloud Shell で簡単なコンソール アプリケーションを開発します。

1. Azure portal で、ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal に新しい Cloud Shell を作成し、***PowerShell*** 環境を選択します。 Azure portal の下部にあるペインに、Cloud Shell のコマンド ライン インターフェイスが表示されます。

    > **注**: *Bash* 環境を使用するクラウド シェルを以前に作成した場合は、それを ***PowerShell*** に切り替えます。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

    **<font color="red">続行する前に、クラシック バージョンの Cloud Shell に切り替えたことを確認します。</font>**

1. PowerShell ペインで、次のコマンドを入力して、この演習用の GitHub リポジトリを複製します。

    ```
   rm -r mslearn-ai-language -f
   git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **ヒント**: Cloudshell にコマンドを貼り付けると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。
    ```

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
    cd mslearn-ai-language/Labfiles/05-custom-entity-recognition/Python/custom-entities
    ```

## Configure your application

1. In the command line pane, run the following command to view the code files in the **custom-entities** folder:

    ```
   ls -a -l
    ```

    The files include a configuration file (**.env**) and a code file (**custom-entities.py**). The text your application will analyze is in the **ads** subfolder.

1. Create a Python virtual environment and install the Azure AI Language Text Analytics SDK package and other required packages by running the following command:

    ```
   python -m venv labenv ./labenv/bin/Activate.ps1 pip install -r requirements.txt azure-ai-textanalytics==5.3.0
    ```

1. Enter the following command to edit the application configuration file:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. Update the configuration values to include the  **endpoint** and a **key** from the Azure Language resource you created (available on the **Keys and Endpoint** page for your Azure AI Language resource in the Azure portal).The file should already contain the project and deployment names for your custom entity extraction model.
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

## Add code to extract entities

1. Enter the following command to edit the application code file:

    ```
    code custom-entities.py
    ```

1. Review the existing code. You will add code to work with the AI Language Text Analytics SDK.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need to use the Text Analytics SDK:

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. **main** 関数では、Azure AI Language サービスのエンドポイントとキー、およびプロジェクト名とデプロイ名を構成ファイルから読み込むコードが既に提供されていることに注目してください。 次に、**Create client using endpoint and key (エンドポイントとキーを使用してクライアントを作成する)** というコメントを検索し、次のコードを追加して、テキスト分析クライアントを作成します。

    ```Python
   # Create client using endpoint and key
   credential = AzureKeyCredential(ai_key)
   ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. 既存のコードが **ads** フォルダー内のすべてのファイルを読み取り、その内容を含む一覧を作成することにご注意ください。 **Extract entities (エンティティを抽出する)** というコメントを検索し、次のコードを追加します。

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

1. 変更を保存し (Ctrl + S)、次のコマンドを入力してプログラムを実行します (コマンド ライン ペインのテキストをより多く表示するには、[Cloud Shell] ペインを最大化し、パネルをサイズ変更します)。

    ```
   python custom-entities.py
    ```

1. 出力を確認します。 アプリケーションでは、各テキスト ファイルで見つかったエンティティの詳細を一覧表示する必要があります。

## クリーンアップ

プロジェクトが必要なくなったら、Language Studio の **[プロジェクト]** ページから削除できます。 [Azure portal](https://portal.azure.com) でも、Azure AI Language サービスと関連付けられたストレージ アカウントを削除できます。

---
lab:
  title: テキストを分析する
  description: Azure AI Language を使用して、言語検出、感情分析、キー フレーズ抽出、エンティティ認識などのテキスト分析を行います。
---

# テキストの分析

**Azure AI Language** は、言語検出、感情分析、キー フレーズ抽出、エンティティ認識などのテキスト分析をサポートしています。

たとえば、旅行代理店が会社の Web サイトに送信されたホテルのレビューを処理したいとします。 Azure AI Language を使用すると、各レビューが書かれている言語、レビューの感情 (ポジティブ、ニュートラル、ネガティブ)、レビューで議論されている主なトピックを示す可能性のあるキー フレーズ、場所、ランドマーク、またはレビューで言及された人などの名前付きエンティティなどを特定できます。 この演習では、テキスト分析に Azure AI Language Python SDK を使用して、この例に基づいて簡単なホテル レビュー アプリケーションを実装します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用してテキスト分析アプリケーションを開発できます。

- [Python 用 Azure AI Text Analytics クライアント ライブラリ](https://pypi.org/project/azure-ai-textanalytics/)
- [.NET 用 Azure AI Text Analytics クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.TextAnalytics)
- [JavaScript 用 Azure AI Text Analytics クライアント ライブラリ](https://www.npmjs.com/package/@azure/ai-text-analytics)

この演習は約 **30** 分かかります。

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

## このコースのリポジトリを複製する

Azure portal から Cloud Shell を使用してコード開発を行います。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

1. Azure portal で、ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal に新しい Cloud Shell を作成し、***PowerShell*** 環境を選択します。 Azure portal の下部にあるペインに、Cloud Shell のコマンド ライン インターフェイスが表示されます。

    > **注**: *Bash* 環境を使用するクラウド シェルを以前に作成した場合は、それを ***PowerShell*** に切り替えます。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

    **<font color="red">続行する前に、クラシック バージョンの Cloud Shell に切り替えたことを確認します。</font>**

1. PowerShell ペインで、次のコマンドを入力して、この演習用の GitHub リポジトリを複製します。

    ```
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **ヒント**: Cloudshell にコマンドを入力すると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。

1. リポジトリが複製されたら、アプリケーション コード ファイルを含むフォルダーに移動します。  

    ```
    cd mslearn-ai-language/Labfiles/01-analyze-text/Python/text-analysis
    ```

## アプリケーションを構成する

1. コマンド ライン ペインで次のコマンドを実行して、**text-analysis** フォルダー内のコード ファイルを表示します。

    ```
   ls -a -l
    ```

    これらのファイルとしては、構成ファイル (**.env**) とコード ファイル (**text-analysis.py**) があります。 アプリケーションで分析するテキストは、**reviews** サブフォルダーにあります。

1. 次のコマンドを実行して、Python 仮想環境を作成し、Azure AI Language Text Analytics SDK パッケージとその他の必要なパッケージをインストールします。

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-textanalytics==5.3.0
    ```

1. 次のコマンドを入力して、アプリケーション構成ファイルを編集します。

    ```
   code .env
    ```

    このファイルをコード エディターで開きます。

1. 作成した Azure 言語リソースの**エンドポイント**と**キー**を含むように構成値を更新します (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで利用可能)。
1. プレースホルダーを置き換えたら、コード エディター内で、**Ctrl + S** コマンドを使用するか、**右クリックして保存**で変更を保存してから、**Ctrl + Q** コマンドを使用するか、**右クリックして終了**で、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

## Azure AI Language リソースに接続するコードを追加する

1. 次のコマンドを入力して、アプリケーション コード ファイルを編集します。

    ```
    code text-analysis.py
    ```

1. 既存のコードを確認します。 AI Language Text Analytics SDK を操作するコードを追加します。

    > **ヒント**: コード ファイルにコードを追加する際は、必ず正しいインデントを維持してください。

1. コード ファイルの上部にある既存の名前空間参照の下で、**Import namespaces (名前空間をインポートする)** というコメントを検索し、Text Analytics SDK を使用するために必要な名前空間をインポートする次のコードを追加します。

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. **main** 関数で、構成ファイルから Azure AI Language サービス エンドポイントとキーを読み込むためのコードが既に提供されていることに注目してください。 次に、**「エンドポイントとキーを使用してクライアントを作成する」** というコメントを見つけ、次のコードを追加して、Text Analysis API のクライアントを作成します。

    ```Python
   # Create client using endpoint and key
   credential = AzureKeyCredential(ai_key)
   ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. 変更を保存し (Ctrl + S)、次のコマンドを入力してプログラムを実行します (コマンド ライン ペインのテキストをより多く表示するには、[Cloud Shell] ペインを最大化し、パネルをサイズ変更します)。

    ```
   python text-analysis.py
    ```

1. コードがエラーなしで実行され、**reviews** フォルダー内の各レビュー テキストファイルの内容が表示されるので、出力を確認します。 アプリケーションは Text Analytics API のクライアントを正常に作成しますが、それを利用しません。 次のセクションでこれを修正します。

## 言語を検出するコードを追加する

API のクライアントを作成したので、それを使用して、各レビューが書かれている言語を検出します。

1. コード エディターで、**Get language (言語を取得する)** というコメントを検索します。 次に、各レビュー ドキュメントで言語を検出するために必要なコードを追加します。

    ```python
   # Get language
   detectedLanguage = ai_client.detect_language(documents=[text])[0]
   print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
    ```

     > **注**: *この例では、各レビューが個別に分析され、ファイルごとにサービスが個別に呼び出されます。別の方法として、ドキュメントのコレクションを作成し、1 回の呼び出しでサービスに渡す方法があります。どちらの方法でも、サービスからの応答はドキュメントのコレクションで構成されます。これは、上記の Python コードでは、応答 ([0]) 内の最初の (そして唯一の) ドキュメントのインデックスが指定されている理由です。*

1. 変更を保存。 次に、プログラムを再実行します。
1. 出力を観察します。今回は、各レビューの言語が識別されていることに注意してください。

## センチメントを評価するコードを追加する

"*感情分析*" は、テキストを "*ポジティブ*" または "*ネガティブ*" ("*ニュートラル*" または "*混合*" の場合もある) として分類するために一般的に使用される手法です。 ソーシャル メディアの投稿、製品レビュー、およびテキストの感情が有用な洞察を提供する可能性があるその他のアイテムを分析するために一般的に使用されます。

1. コード エディターで、**Get sentiment (センチメントを取得する)** というコメントを検索します。 次に、各レビュードキュメントの感情を検出するために必要なコードを追加します。

    ```python
   # Get sentiment
   sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
   print("\nSentiment: {}".format(sentimentAnalysis.sentiment))
    ```

1. 変更を保存。 次に、コード エディターを閉じて、プログラムを再実行します。
1. 出力を観察し、レビューの感情が検出されたことに注意します。

## キー フレーズを識別するコードを追加する

テキストの本文でキー フレーズを特定すると、説明する主なトピックを特定するのに役立ちます。

1. コード エディターで、**Get key phrases (キー フレーズを取得する)** というコメントを検索します。 次に、各レビュー ドキュメントでキー フレーズを検出するために必要なコードを追加します。

    ```python
   # Get key phrases
   phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
   if len(phrases) > 0:
        print("\nKey Phrases:")
        for phrase in phrases:
            print('\t{}'.format(phrase))
    ```

1. 変更を保存し、プログラムを再実行します。
1. 各ドキュメントにキー フレーズが含まれていることに注意して、出力を確認します。それはレビューが何であるかについてのいくつかの洞察を与えます。

## データを抽出するエンティティを追加する

多くの場合、ドキュメントまたはその他のテキスト本体は、人、場所、期間、またはその他のエンティティについて言及しています。 Text Analytics API は、テキスト内のエンティティの複数のカテゴリ (およびサブカテゴリ) を検出できます。

1. コード エディターで、**Get entities (エンティティを取得する)** というコメントを検索します。 次に、各レビューで言及されているエンティティを識別するために必要なコードを追加します。

    ```python
   # Get entities
   entities = ai_client.recognize_entities(documents=[text])[0].entities
   if len(entities) > 0:
        print("\nEntities")
        for entity in entities:
            print('\t{} ({})'.format(entity.text, entity.category))
    ```

1. 変更を保存し、プログラムを再実行します。
1. 出力を確認します。テキストで検出されたエンティティに注意してください。

## リンクされたエンティティを抽出するコードを追加する

分類されたエンティティに加えて、Text Analytics API は、Wikipedia などのデータソースへの既知のリンクがあるエンティティを検出できます。

1. コード エディターで、**Get linked entities (リンクされているエンティティを取得する)** というコメントを検索します。 次に、各レビューで言及されている、リンクされているエンティティを識別するために必要なコードを追加します。

    ```python
   # Get linked entities
   entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
   if len(entities) > 0:
        print("\nLinks")
        for linked_entity in entities:
            print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
    ```

1. 変更を保存し、プログラムを再実行します。
1. 出力を確認します。識別されたリンクされたエンティティに注意してください。

## リソースをクリーンアップする

Azure AI Language サービス の調査が完了した場合は、この演習で作成したリソースを削除してください。 方法は以下のとおりです。

1. [Azure Cloud Shell] ペインを閉じます
1. Azure portal で、このラボで作成した Azure AI Language リソースを参照します。
1. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細

**Azure AI Language** の詳細については、「[ドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/)」を参照してください。

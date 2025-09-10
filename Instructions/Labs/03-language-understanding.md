---
lab:
  title: Azure AI Language サービスで言語理解モデルを作成する
  description: 入力の解釈、意図の予測、エンティティの識別を行うカスタム言語理解モデルを作成します。
---

# 言語サービスで言語理解モデルを作成する

Azure AI Language サービスを使うと、*会話言語理解*モデルを定義することができます。これをアプリケーションから使って、ユーザーからの自然言語*発話* (テキストまたは音声入力) を解釈し、ユーザーの*意図* (達成したいこと) を予測し、その意図を適用する必要がある*エンティティ*を特定することができます。

たとえば、時計アプリケーション用の会話言語モデルは、次のような入力を処理することが期待される場合があります。

*What's the time in London?* (ロンドンの時刻は何時ですか?)

この種の入力は、*発話* (ユーザーが言うまたは入力する可能性のあるもの) の例です。*意図* は、特定の場所 (*エンティティ*) (この場合はロンドン) の時刻を得ることです。

> **メモ** 会話言語モデルのタスクは、ユーザーの意図を予測し、意図が適用されるエンティティを特定することです。 意図を満たすために必要なアクションを実際に実行することは、会話言語モデルの仕事では<u>ありません</u>。 たとえば、時計アプリケーションは会話言語モデルを使用して、ユーザーがロンドンの時刻を知りたいことを識別できます。ただし、クライアント アプリケーション自体は、正しい時刻を決定してユーザーに提示するロジックを実装する必要があります。

この演習では、Azure AI Language サービスを使用して会話言語理解モデルを作成し、Python SDK を使用してそれを使用するクライアント アプリを実装します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用して会話理解アプリケーションを開発できます。

- [Python 用 Azure AI Conversations クライアント ライブラリ](https://pypi.org/project/azure-ai-language-conversations/)
- [.NET 用 Azure AI Conversations クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.Language.Conversations)
- [JavaScript 用 Azure AI Conversations クライアント ライブラリ](https://www.npmjs.com/package/@azure/ai-language-conversations)

この演習は約 **35** 分かかります。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションに **Azure AI Language サービス** リソースがまだない場合は、Azure サブスクリプションでプロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. **[リソースの作成]** を選択します。
1. 検索フィールドで、**言語サービス**を検索します。 次に、結果で、**[言語サービス]** の下の **[作成]** を選択します。
1. 次の設定を使用してリソースをプロビジョニングします。
    - **[サブスクリプション]**: *お使いの Azure サブスクリプション*。
    - **リソース グループ**: *リソース グループを選択または作成します*。
    - **リージョン**: *次のいずれかのリージョンから選択します。*\*
        - オーストラリア東部
        - インド中部
        - 中国東部 2
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
    - **価格レベル**: **F0** (*無料*)、または F が利用できない場合は **S** (*標準*) を選択します。
    - **責任ある AI 通知**: 同意。
1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
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

    1. ページの上部にあるバーで、**[設定] (&#9881;)** ボタンを選択します。
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

    > **注:** 新しい発話を追加するには、意図の横にあるテキスト ボックスに発話を入力し、Enter キーを押します。 

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

1. **[トレーニング ジョブの開始]** ダイアログで、新しいモデルをトレーニングするオプションを選び、名前を `Clock` にします。 **標準トレーニング** モードと既定の **[データ分割]** オプションを選択します。

1. モデルのトレーニング プロセスを開始するには、**[トレーニングする]** をクリックします。

1. トレーニングが完了した場合 (数分かかることがあります)、ジョブの **[状態]** が " **トレーニング成功**" に変わります。

1. **[モデルのパフォーマンス]** ページを選択して、 **[Clock]** モデルを選択します。 全体と意図ごとの評価メトリック ( *"精度"* 、 *"再現率"* 、 *"F1 スコア"* ) と、トレーニング時に行った評価で生成された *"混同行列"* を確認します (サンプル発話数が少ないため、すべての意図が結果に含まれていない可能性がある点に注意してください)。

    > **メモ** 評価メトリックの詳細については、「[ドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/concepts/evaluation-metrics)」をご覧ください。

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

    > **注:** 新しいリストのフィールドに入力するには、テキスト フィールドに値 `Sunday` を挿入したあと、"値を入力して Enter キーを押してください" と表示されているフィールドをクリックし、シノニムを入力して Enter キーを押します。

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
1. 事前構築済みエンティティを追加したら、**[データのラベル付け]** ページに戻ります
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

### Cloud Shell でアプリを開発する準備をする

Azure portal で Cloud Shell を使用して、言語理解アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

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

1. リポジトリが複製されたら、アプリケーション コード ファイルを含むフォルダーに移動します。  

    ```
   cd mslearn-ai-language/Labfiles/03-language/Python/clock-client
    ```

### アプリケーションを構成する

1. コマンド ラインで次のコマンドを実行して、**clock-client** フォルダー内のコード ファイルを表示します。

    ```
   ls -a -l
    ```

    これらのファイルとしては、構成ファイル (**.env**) とコード ファイル (**clock-client.py**) があります。

1. 次のコマンドを実行して、Python 仮想環境を作成し、Azure AI Language Conversations SDK パッケージとその他の必要なパッケージをインストールします。

    ```
   python -m venv labenv
    ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-language-conversations==1.1.0
    ```
1. 次のコマンドを入力して、構成ファイルを編集します。

    ```
   code .env
    ```

    このファイルをコード エディターで開きます。

1. 構成値を更新して、作成した Azure Language リソースの**エンドポイント**と**キー**を含めます (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで使用できます)。
1. プレースホルダーを置き換えたら、コード エディター内で、**Ctrl + S** コマンドを使用するか、**右クリックして保存**で変更を保存してから、**Ctrl + Q** コマンドを使用するか、**右クリックして終了**で、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

### アプリケーションにコードを追加する

1. 次のコマンドを入力して、アプリケーション コード ファイルを編集します。

    ```
   code clock-client.py
    ```

1. 既存のコードを確認します。 AI Language Conversations SDK を操作するコードを追加します。

    > **ヒント**: コード ファイルにコードを追加する際は、必ず正しいインデントを維持してください。

1. コード ファイルの上部にある既存の名前空間参照の下で、**Import namespaces (名前空間をインポートする)** というコメントを検索し、AI Language Conversations SDK を使用するために必要な名前空間をインポートする次のコードを追加します。

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.language.conversations import ConversationAnalysisClient
    ```

1. **main** 関数では、構成ファイルから予測エンドポイント、およびキーを読み込むためのコードが既に提供されていることに注目してください。 次に、**Create a client for the Language service model (Language サービス モデルのクライアントを作成する)** というコメントを検索し、次のコードを追加して、AI Language サービスの会話分析予測クライアントを作成します。

    ```python
   # Create a client for the Language service model
   client = ConversationAnalysisClient(
        ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))
    ```

1. ユーザーが "quit" と入力するまで、**main** 関数のコードはユーザーによる入力を求めるプロンプトを表示することにご注意ください。 このループ内で、コメント "**Call the Language service model to get intent and entities**" を見つけて、次のコードを追加します。

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

    会話理解サービス モデルを呼び出すと、予測または結果が返されます。これには、入力発話で検出されたエンティティだけでなく、最上位の (最も可能性の高い) 意図も含まれます。 クライアント アプリケーションは、その予測を使用して適切なアクションを決定および実行する必要があります。

1. コメント **Apply the appropriate action** を見つけ、次のコードを追加します。このコードは、アプリケーションでサポートされている意図 (**GetTime**、**GetDate**、および **GetDay**) をチェックします。また、適切な応答を生成するために既存の関数を呼び出す前に、関連するエンティティが検出されたかどうかを判断します。

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

1. 変更を保存し (Ctrl + S)、次のコマンドを入力してプログラムを実行します (コマンド ライン ペインのテキストをより多く表示するには、[Cloud Shell] ペインを最大化し、パネルをサイズ変更します)。

    ```
   python clock-client.py
    ```

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

Azure AI Language サービス の調査が完了した場合は、この演習で作成したリソースを削除してください。 方法は以下のとおりです。

1. [Azure Cloud Shell] ペインを閉じます
1. Azure portal で、このラボで作成した Azure AI Language リソースを参照します。
1. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細情報

Azure AI Language における会話言語理解の詳細については、「[Azure AI Language のドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/overview)」をご覧ください。

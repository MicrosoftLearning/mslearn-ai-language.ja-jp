---
lab:
  title: 質問応答ソリューションを作成する
  description: Azure AI Language を使用して、カスタムの質問応答ソリューションを作成します。
---

# 質問応答ソリューションを作成する

最も一般的な会話シナリオの 1 つは、よくある質問 (FAQ) のナレッジ ベースを通じてサポートを提供することです。 多くの組織は、FAQ をドキュメントまたは Web ページとして公開しています。これは、質問と回答のペアの小さなセットに適していますが、大きなドキュメントは検索が難しく、時間がかかる場合があります。

**Azure AI Language** には、*質問応答*機能が含まれており、これを使用すると、自然言語入力で問い合わせることができる、質問と回答のペアで構成されるナレッジ ベースを作成できます。また、この機能は、ユーザーから送信された質問への回答を検索するためにボットが使用できるリソースとして最も一般的に使用されています。 この演習では、テキスト分析に Azure AI Language Python SDK を使用して、この例に基づいて簡単な質問応答アプリケーションを実装します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用して質問応答アプリケーションを開発できます。

- [Python 用 Azure AI Language Service Question Answering クライアント ライブラリ](https://pypi.org/project/azure-ai-language-questionanswering/)
- [.NET 用 Azure AI Language Service Question Answering クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.Language.QuestionAnswering)

この演習は約 **20** 分かかります。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションにまだリソースがない場合は、**Azure AI Language サービス** リソースをプロビジョニングする必要があります。 さらに、質問応答用のナレッジ ベースを作成してホストするには、**質問応答**機能を有効にする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. **[リソースの作成]** を選択します。
1. 検索フィールドで、**言語サービス**を検索します。 次に、結果で、**[言語サービス]** の下の **[作成]** を選択します。
1. **カスタム質問応答**ブロックを選択します。 **[リソースの作成を続行する]** を選びます。 次の設定を入力する必要があります。

    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **[リソース グループ]**: *リソース グループを作成または選択します*。
    - **[リージョン]** : *利用可能な場所を選択する*
    - **[名前]**: *一意の名前を入力します*
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **Azure Search のリージョン**: *言語リソースと同じグローバル リージョン内の場所を選択します*
    - **Azure Search の価格レベル**：無料 (F) ("*このレベルが利用できない場合は、[基本 (B)] を選択してください*")
    - **責任ある AI 通知**: "同意"**

1. **[作成と確認]** を選択し、次に **[作成]** を選択します。

    > **メモ** カスタム質問応答では、Azure Search を使用して、質問と回答のナレッジ ベースにインデックスを付けてクエリを実行します。

1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[リソース管理]** セクションで、**[キーとエンドポイント]** ページを表示します。 このページの情報は、演習の後半で必要になります。

## 質問応答プロジェクトを作成する

Azure AI Language リソースで質問応答のナレッジ ベースを作成するには、Language Studio ポータルを使用して質問応答プロジェクトを作成します。 この場合、[Microsoft Learn](https://docs.microsoft.com/learn) に関する質問と答えを含むナレッジ ベースを作成します。

1. 新しいブラウザー タブで Language Studio ポータル ([https://language.cognitive.azure.com/](https://language.cognitive.azure.com/)) に移動し、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使ってサインインします。
1. 言語リソースの選択を求めるメッセージが表示されたら、次の設定を選択します。
    - **Azure ディレクトリ**: ご利用のサブスクリプションを含む Azure ディレクトリ
    - **Azure サブスクリプション**: ご利用の Azure サブスクリプション
    - **リソースの種類**: 言語
    - **リソース名**: 先ほど作成した Azure AI Language リソース。

    言語リソースの選択を求めるメッセージが表示<u>されない</u>場合、原因として、お使いのサブスクリプションに複数の言語リソースが存在していることが考えられます。その場合は、次の操作を行います。

    1. ページの上部にあるバーで、**[設定] (&#9881;)** ボタンを選択します。
    2. **[設定]** ページで、**[リソース]** タブを表示します。
    3. 作成したばかりの言語リソースを選択し、**[リソースの切り替え]** をクリックします。
    4. ページの上部で、**[Language Studio]** をクリックして、Language Studio のホーム ページに戻ります。

1. ポータルの上部にある **[Create new]** メニューで、 **[Custom question answering]** (カスタム質問と回答) を選択します。
1. ***[プロジェクトの作成]** ウィザードの **[言語設定の選択]** ページで、**[すべてのプロジェクトの言語を選択する]** オプションを選択し、言語として**英語**を選択します。 **[次へ]** を選択します。
1. **[基本情報の入力]** ページで、次の詳細を入力します。
    - **名前**`LearnFAQ`
    - **説明**: `FAQ for Microsoft Learn`
    - **回答が返されない場合の既定の回答**: `Sorry, I don't understand the question`
1. [**次へ**] を選択します。
1. **[確認と終了]** ページで、**[プロジェクトの作成]** を選択します。

## ナレッジ ベースにソースを追加する

ナレッジ ベースは最初から作成できますが、既存の FAQ ページまたはドキュメントから質問と回答をインポートすることから始めるのが一般的です。 この場合、Microsoft Learn の既存の FAQ Web ページからデータをインポートし、一般的な会話のやり取りをサポートするために、あらかじめ定義された "おしゃべり" の質問と回答もインポートします。

1. 質問応答プロジェクトの **[ソースの管理]** ページにある **[&#9547; ソースの追加]** の一覧で、 **[URL]** を選択します。 次に、**[URL の追加]** ダイアログ ボックスで **[╋ URL の追加]** を選択し、次の名前と URL を設定してから、**[すべて追加]** を選択してナレッジ ベースに追加します。
    - **名前**: `Learn FAQ Page`
    - **URL**: `https://docs.microsoft.com/en-us/learn/support/faq`
1. 質問応答プロジェクトの **[ソースの管理]** ページで、 **[&#9547; ソースの追加]** の一覧にある **[Chitchat](おしゃべり)** を選択します。 次に、**[おしゃべりの追加]** ダイアログ ボックスで、**[フレンドリ]** を選択し、**[おしゃべりの追加]** をクリックします。

## ナレッジ ベースを編集する

ナレッジ ベースには、Microsoft Learn FAQ の質問と回答のペアが入力されており、会話型 *chit-chat* の質問と回答のペアが追加されています。 質問と回答のペアを追加することで、ナレッジ ベースを拡張できます。

1. Language Studio の **LearnFAQ** プロジェクトで、**[ナレッジ ベースの編集]** ページを選択して既存の質問と回答のペアを表示します (複数のヒントが表示されている場合は、それを読み、**[了解]** を選択して閉じるか、**[すべてスキップ]** を選択します)
1. ナレッジ ベースの **[質問と回答のペア]** タブで、**[＋]** を選択し、次の設定で新しい質問と回答のペアを作成します。
    - **ソース**: `https://docs.microsoft.com/en-us/learn/support/faq`
    - **質問**: `What are Microsoft credentials?`
    - **回答**: `Microsoft credentials enable you to validate and prove your skills with Microsoft technologies.`
1. **完了** を選択します。
1. 作成された「**Microsoft 認定資格とは?**」という質問のページで、**[代わりの質問]** を展開してください。 次に、代わりの質問 `How can I demonstrate my Microsoft technology skills?` を追加します。

    場合によっては、ユーザーが回答をフォローアップして、*マルチターン*会話を作成できるようにすることが理にかなっています。ユーザーは、質問を繰り返し絞り込んで、必要な回答にたどり着きます。

1. 認定資格についての質問に対して入力した答えで **[フォローアップ プロンプト]** を展開し、次のフォローアップ プロンプトを追加します。
    - **ユーザーへのプロンプトに表示されるテキスト**: `Learn more about credentials`。
    - **[新しいペアへのリンクの作成]** を選択し、「`You can learn more about credentials on the [Microsoft credentials page](https://docs.microsoft.com/learn/credentials/).`」のテキストを入力します。
    - **[コンテキスト フローでのみ表示]** を選択します。 このオプションにより、元の認定質問からのフォローアップ質問のコンテキストでのみ回答が返されるようになります。
1. **[プロンプトの追加]** を選択します。

## ナレッジ ベースのトレーニングとテスト

ナレッジベースができたので、Language Studio でテストできます。

1. 左側の **[質問と回答のペア]** タブで **[保存]** ボタンを選択して、変更内容をナレッジ ベースに保存します。
1. 変更が保存されたら、**[テスト]** を選択して、テスト ペインを開きます。
1. テスト ペインの上部にある **[短い回答を含める]** の選択を解除します (まだ選択解除されていない場合)。 次に、下部に「`Hello`」というメッセージを入力します。 適切な応答が返される必要があります。
1. テスト ペインの下部に「`What is Microsoft Learn?`」というメッセージを入力します。 FAQ から適切な応答が返されるはずです。
1. 「`Thanks!`」というメッセージを入力します。適切なおしゃべりの応答が返されます。
1. 「`Tell me about Microsoft credentials`」というメッセージを入力します。 作成した回答が、フォローアップ プロンプト ボタンとともに返されます。
1. **[資格情報の詳細]** フォローアップ リンクを選択します。 認定ページへのリンクを含むフォローアップ回答を返送する必要があります。
1. ナレッジ ベースのテストが完了したら、テスト ペインを閉じます。

## ナレッジ ベースをデプロイする

ナレッジ ベースは、クライアント アプリケーションが質問に回答するために使用できるバックエンド サービスを提供します。 これで、ナレッジ ベースを公開し、クライアントからその REST インターフェイスにアクセスする準備が整いました。

1. Language Studio の **LearnFAQ** プロジェクトで、左側のナビゲーション メニューから **[ナレッジ ベースのデプロイ]** ページを選択します。
1. ページの上部で、**[デプロイ]** を選択します。 次に、**[デプロイ]** を選択して、ナレッジ ベースをデプロイすることを確認します。
1. デプロイが完了したら、**[予測 URL の取得]** を選択してナレッジ ベースの REST エンドポイントを表示し、サンプル要求に次のパラメーターが含まれていることに注意します。
    - **projectName**: プロジェクトの名前 (*LearnFAQ* にする必要があります)
    - **deploymentName**: デプロイの名前 (*実稼働*にする必要があります)
1. 予測 URL ダイアログ ボックスを閉じます。

## Cloud Shell でアプリを開発する準備をする

Azure portal で Cloud Shell を使用して、質問応答アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

1. Azure portal で、ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal に新しい Cloud Shell を作成し、***PowerShell*** 環境を選択します。 Azure portal の下部にあるペインに、Cloud Shell のコマンド ライン インターフェイスが表示されます。

    > **注**: *Bash* 環境を使用するクラウド シェルを以前に作成した場合は、それを ***PowerShell*** に切り替えます。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

    **<font color="red">続行する前に、クラシック バージョンの Cloud Shell に切り替えたことを確認します。</font>**

1. PowerShell ペインで、次のコマンドを入力して、この演習用の GitHub リポジトリを複製します。

    ```
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **ヒント**: Cloud Shell にコマンドを入力すると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。

1. リポジトリが複製されたら、アプリケーション コード ファイルを含むフォルダーに移動します。  

    ```
    cd mslearn-ai-language/Labfiles/02-qna/Python/qna-app
    ```

## アプリケーションを構成する

1. コマンド ライン ペインで次のコマンドを実行して、**qna-app** フォルダー内のコード ファイルを表示します。

    ```
   ls -a -l
    ```

    これらのファイルとしては、構成ファイル (**.env**) とコード ファイル (**qna-app.py**) があります。

1. 次のコマンドを実行して、Python 仮想環境を作成し、Azure AI Language Question Answering SDK パッケージとその他の必要なパッケージをインストールします。

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-language-questionanswering
    ```

1. 次のコマンドを入力して、構成ファイルを編集します。

    ```
    code .env
    ```

    このファイルをコード エディターで開きます。

1. コード ファイルに含まれる構成値を、作成した Azure AI Language リソースの**エンドポイント**と認証**キー**を反映するように更新します (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで確認できます)。 このファイルには、デプロイされたナレッジ ベースのプロジェクト名とデプロイ名も含まれている必要があります。
1. プレースホルダーを置き換えたら、コード エディター内で、**Ctrl + S** コマンドを使用するか、**右クリックして保存**で変更を保存してから、**Ctrl + Q** コマンドを使用するか、**右クリックして終了**で、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

## ナレッジ ベース使用するためのコードを追加する

1. 次のコマンドを入力して、アプリケーション コード ファイルを編集します。

    ```
    code qna-app.py
    ```

1. 既存のコードを確認します。 ナレッジ ベースを操作するコードを追加します。

    > **ヒント**: コード ファイルにコードを追加する際は、必ず正しいインデントを維持してください。

1. コード ファイルで、**Import namespaces (名前空間をインポートする)** というコメントを検索します。 次に、このコメントの下に、次の言語固有のコードを追加して、Question Answering SDK を使用するために必要な名前空間をインポートします。

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.language.questionanswering import QuestionAnsweringClient
    ```

1. **main** 関数で、構成ファイルから Azure AI Language サービス エンドポイントとキーを読み込むためのコードが既に提供されていることに注目してください。 次に、**Create client using endpoint and key (エンドポイントとキーを使用してクライアントを作成する)** というコメントを検索し、次のコードを追加して、質問応答クライアントを作成します。

    ```Python
   # Create client using endpoint and key
   credential = AzureKeyCredential(ai_key)
   ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
    ```

1. コード ファイルで、**Submit a question and display the answer (質問を送信して答えを表示する)** というコメントを検索し、コマンド ラインから質問を繰り返し読み取り、サービスに送信して、回答の詳細を表示する次のコードを追加します。

    ```Python
   # Submit a question and display the answer
   user_question = ''
   while True:
        user_question = input('\nQuestion:\n')
        if user_question.lower() == "quit":                
            break
        response = ai_client.get_answers(question=user_question,
                                        project_name=ai_project_name,
                                        deployment_name=ai_deployment_name)
        for candidate in response.answers:
            print(candidate.answer)
            print("Confidence: {}".format(candidate.confidence))
            print("Source: {}".format(candidate.source))
    ```

1. 変更を保存し (Ctrl + S)、次のコマンドを入力してプログラムを実行します (コマンド ライン ペインのテキストをより多く表示するには、[Cloud Shell] ペインを最大化し、パネルをサイズ変更します)。

    ```
   python qna-app.py
    ```

1. メッセージが表示されたら、質問応答プロジェクトに送信する質問を入力します。例: `What is a learning path?`。
1. 返された回答を確認します。
1. 他の質問をします。 完了したら、「`quit`」と入力します。

## リソースをクリーンアップする

Azure AI Language サービス の調査が完了した場合は、この演習で作成したリソースを削除してください。 方法は以下のとおりです。

1. [Azure Cloud Shell] ペインを閉じます
1. Azure portal で、このラボで作成した Azure AI Language リソースを参照します。
1. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細情報

Azure AI Language における質問応答の詳細については、「[Azure AI Language のドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/question-answering/overview)」をご覧ください。

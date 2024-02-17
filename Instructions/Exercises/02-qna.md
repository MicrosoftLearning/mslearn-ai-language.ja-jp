---
lab:
  title: 質問応答ソリューションを作成する
  module: Module 6 - Create question answering solutions with Azure AI Language
---

# 質問応答ソリューションを作成する

最も一般的な会話シナリオの 1 つは、よくある質問 (FAQ) のナレッジ ベースを通じてサポートを提供することです。 多くの組織は、FAQ をドキュメントまたは Web ページとして公開しています。これは、質問と回答のペアの小さなセットに適していますが、大きなドキュメントは検索が難しく、時間がかかる場合があります。

**Azure AI Language** には、*質問応答*機能が含まれており、これを使用すると、自然言語入力で問い合わせることができる、質問と回答のペアで構成されるナレッジ ベースを作成できます。また、この機能は、ユーザーから送信された質問への回答を検索するためにボットが使用できるリソースとして最も一般的に使用されています。

## *Azure AI Language* リソースをプロビジョニングする

サブスクリプションにまだリソースがない場合は、**Azure AI Language サービス** リソースをプロビジョニングする必要があります。 さらに、質問応答用のナレッジ ベースを作成してホストするには、**質問応答**機能を有効にする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部の検索フィールドに「**Azure AI サービス**」と入力し、**Enter** キーを押します。
1. 結果の**言語サービス** リソースの下で **[作成]** を選択します。
1. **カスタム質問応答**ブロックを**選択**します。 **[リソースの作成を続行する]** を選びます。 次の設定を入力する必要があります。

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
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

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
1. ***[プロジェクトの作成]** ウィザードの **[言語設定の選択]** ページで、**[このリソースのすべてのプロジェクトの言語を設定する]** オプションを選択し、言語として**英語**を選択します。 **[次へ]** を選択します。
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

1. Language Studio で、**LearnFAQ** プロジェクトの **[ナレッジ ベースのデプロイ]** ページを選択します。
1. ページの上部で、**[デプロイ]** を選択します。 次に、**[デプロイ]** を選択して、ナレッジ ベースをデプロイすることを確認します。
1. デプロイが完了したら、**[予測 URL の取得]** を選択してナレッジ ベースの REST エンドポイントを表示し、サンプル要求に次のパラメーターが含まれていることに注意します。
    - **projectName**: プロジェクトの名前 (*LearnFAQ* にする必要があります)
    - **deploymentName**: デプロイの名前 (*実稼働*にする必要があります)
1. 予測 URL ダイアログ ボックスを閉じます。

## Visual Studio Code でアプリの開発準備をする

Visual Studio Code を使用して、質問応答アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

> **ヒント**: mslearn-ai-language** リポジトリを**既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
2. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
3. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。
4. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるプロンプトが表示された場合は、**[今はしない]** を選択します。

## アプリケーションを構成する

C# と Python の両方のアプリケーションと、要約のテストに使用するサンプル テキスト ファイルが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI Language リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/02-qna** フォルダーを参照し、言語の設定とそこに含まれている **qna-app** フォルダーに応じて **CSharp** または **Python** フォルダーを展開します。 各フォルダーには、Azure AI Language の質問に回答する機能を統合するアプリの言語固有のファイルが含まれています。
2. コード ファイルを含んだ **qna-app** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適したコマンドを実行して、Azure AI Language 質問応答 SDK パッケージをインストールします。

    **C#:**

    ```
    dotnet add package Azure.AI.Language.QuestionAnswering
    ```

    **Python**:

    ```
    pip install azure-ai-language-questionanswering
    ```

3. **[エクスプローラー]** ペインの **qna-app** フォルダーで、優先する言語の構成ファイルを開きます

    - **C#**: appsettings.json
    - **Python**: .env
    
4. 構成値を更新して、作成した Azure Language リソースの**エンドポイント**と**キー**を含めます (Azure portal の Azure AI Language リソースの **[キーとエンドポイント]** ページで使用できます)。 このファイルには、デプロイされたナレッジ ベースのプロジェクト名とデプロイ名も含まれている必要があります。
5. 構成ファイルを保存します。

## アプリケーションにコードを追加する

これで、必要な SDK ライブラリをインポートするために必要なコードを追加し、デプロイされたプロジェクトへの認証済み接続を確立し、質問を送信する準備ができました。

1. **qna-app** フォルダーには、クライアント アプリケーションのコード ファイルが含まれていることに注意してください。

    - **C#**: Program.cs
    - **Python**: qna-app.py

    コード ファイルを開き、上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Text Analytics SDK を使用するために必要な名前空間インポートします。

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.Language.QuestionAnswering;
    ```

    **Python**: qna-app.py

    ```python
    # import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.questionanswering import QuestionAnsweringClient
    ```

1. **Main** 関数で、構成ファイルから Azure AI Language サービスのエンドポイントとキーを読み込むためのコードが既に提供されていることに注意してください。 次に、**「エンドポイントとキーを使用してクライアントを作成する」** というコメントを見つけ、次のコードを追加して、Text Analysis API のクライアントを作成します。

    **C#**: Programs.cs

    ```C#
    // Create client using endpoint and key
    AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
    Uri endpoint = new Uri(aiSvcEndpoint);
    QuestionAnsweringClient aiClient = new QuestionAnsweringClient(endpoint, credentials);
    ```

    **Python**: qna-app.py

    ```Python
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
    ```

1. **Main** 関数で、「**Submit a question and display the answer**」というコメントを見つけ、コマンド ラインから質問を繰り返し読み取り、サービスに送信して、回答の詳細を表示する次のコードを追加します。

    **C#**: Programs.cs

    ```C#
    // Submit a question and display the answer
    string user_question = "";
    while (user_question.ToLower() != "quit")
        {
            Console.Write("Question: ");
            user_question = Console.ReadLine();
            QuestionAnsweringProject project = new QuestionAnsweringProject(projectName, deploymentName);
            Response<AnswersResult> response = aiClient.GetAnswers(user_question, project);
            foreach (KnowledgeBaseAnswer answer in response.Value.Answers)
            {
                Console.WriteLine(answer.Answer);
                Console.WriteLine($"Confidence: {answer.Confidence:P2}");
                Console.WriteLine($"Source: {answer.Source}");
                Console.WriteLine();
            }
        }
    ```

    **Python**: qna-app.py

    ```Python
    # Submit a question and display the answer
    user_question = ''
    while user_question.lower() != 'quit':
        user_question = input('\nQuestion:\n')
        response = ai_client.get_answers(question=user_question,
                                        project_name=ai_project_name,
                                        deployment_name=ai_deployment_name)
        for candidate in response.answers:
            print(candidate.answer)
            print("Confidence: {}".format(candidate.confidence))
            print("Source: {}".format(candidate.source))
    ```

1. 変更を保存して **qna-app** フォルダーの統合ターミナルに戻り、次のコマンドを入力してプログラムを実行します。

    - **C#** : `dotnet run`
    - **Python**: `python qna-app.py`

    > **ヒント**: [ターミナル] ツールバーの **最大化パネル サイズ** (**^**) アイコンを使用すると、コンソール テキストをさらに表示できます。

1. メッセージが表示されたら、質問応答プロジェクトに送信する質問を入力します。例: `What is a learning path?`。
1. 返された回答を確認します。
1. 他の質問をします。 完了したら、「`quit`」と入力します。

## リソースをクリーンアップする

Azure AI Language サービス の調査が完了した場合は、この演習で作成したリソースを削除してください。 方法は以下のとおりです。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
2. このラボで作成した Azure AI Language リソースを参照します。
3. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細情報

Azure AI Language における質問応答の詳細については、「[Azure AI Language のドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/question-answering/overview)」をご覧ください。

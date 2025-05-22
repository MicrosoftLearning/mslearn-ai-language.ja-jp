---
lab:
  title: 音声対応チャット アプリを開発する
  description: Azure AI Foundry を使用して、音声入力をサポートする生成 AI アプリを構築する方法について説明します。
---

# 音声対応チャット アプリを開発する

この演習では、*Phi-4-multimodal-instruct* 生成 AI モデルを使用して、音声ファイルを含むプロンプトに対する応答を生成します。 Azure AI Foundry と Azure AI モデル推論サービスを使用して、顧客が残した音声メッセージを要約することで、農産物サプライヤー会社に AI 支援を提供するアプリを開発します。

この演習は約 **30** 分かかります。

## Azure AI Foundry プロジェクトを作成する

まず、Azure AI Foundry プロジェクトを作成します。

1. Web ブラウザーで [Azure AI Foundry ポータル](https://ai.azure.com) (`https://ai.azure.com`) を開き、Azure 資格情報を使用してサインインします。 初めてサインインするときに開いたヒントまたはクイック スタート ウィンドウを閉じます。また、必要に応じて左上にある **Azure AI Foundry** ロゴを使用してホーム ページに移動します。それは次の画像のようになります。

    ![Azure AI Foundry ポータルのスクリーンショット。](../media/ai-foundry-home.png)

1. ホーム ページで、**[+ 作成]** を選択します。
1. **[プロジェクトの作成]** ウィザードで、プロジェクトの有効な名前を入力し、既存のハブが推奨される場合は、新しいハブを作成するオプションを選択します。 次に、ハブとプロジェクトをサポートするために自動的に作成される Azure リソースを確認します。
1. **[カスタマイズ]** を選択し、ハブに次の設定を指定します。
    - **ハブ名**: *ハブの有効な名前*
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **リソース グループ**: *リソース グループを作成または選択します。*
    - **場所**: 次のいずれかのリージョンを選択します\*:
        - 米国東部
        - 米国東部 2
        - 米国中北部
        - 米国中南部
        - スウェーデン中部
        - 米国西部
        - 米国西部 3
    - **Azure AI サービスまたは Azure OpenAI への接続**: *新しい AI サービス リソースを作成します*
    - **Azure AI 検索への接続**:接続をスキップする

    > \* 執筆時点で、この演習で使用する Microsoft *Phi-4-multimodal-instruct* モデルは、これらのリージョンで使用できます。 [Azure AI Foundry のドキュメント](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless-availability#region-availability)で、特定のモデルの最新のリージョン別の使用可能性を確認できます。 演習の後半でクォータ制限に達した場合は、別のリージョンに別のリソースを作成する必要が生じる可能性があります。

1. **[次へ]** を選択し、構成を確認します。 **[作成]** を選択し、プロセスが完了するまで待ちます。
1. プロジェクトが作成されたら、表示されているヒントをすべて閉じて、Azure AI Foundry ポータルのプロジェクト ページを確認します。これは次の画像のようになっているはずです。

    ![Azure AI Foundry ポータルの Azure AI プロジェクトの詳細のスクリーンショット。](../media/ai-foundry-project.png)

## マルチモーダル モデルをデプロイする

これで、音声ベースの入力をサポートできるマルチモーダル モデルをデプロイする準備ができました。 OpenAI *gpt-4o* モデルなど、選択できるモデルは複数あります。 この演習では、*Phi-4-multimodal-instruct* モデルを使用します。

1. Azure AI Foundry プロジェクト ページの右上にあるツール バーで、**[プレビュー機能]** (**&#9215**) アイコンを使用して、**[Azure AI モデル推論サービスにモデルをデプロイする]** 機能を有効にします。 この機能により、アプリケーション コードで使用する Azure AI 推論サービスでモデル デプロイを使用できるようになります。
1. プロジェクトの左側のウィンドウの **[マイ アセット]** セクションで、**[モデル + エンドポイント]** ページを選択します。
1. **[モデル + エンドポイント]** ページの **[モデル デプロイ]** タブの **[+ モデルのデプロイ]** メニューで、**[基本モデルのデプロイ]** を選択します。
1. 一覧で **Phi-4-multimodal-instruct** モデルを検索してから、それを選択して確認します。
1. メッセージに応じて使用許諾契約書に同意したあと、デプロイの詳細で **[カスタマイズ]** を選択して、以下の設定でモデルをデプロイします。
    - **デプロイ名**: *モデル デプロイの有効な名前*
    - **デプロイの種類**: グローバル標準
    - **デプロイの詳細**: *既定の設定を使用します*
1. デプロイのプロビジョニングの状態が**完了**になるまで待ちます。

## クライアント アプリケーションを作成する

モデルをデプロイしたので、クライアント アプリケーションでデプロイを使用できます。

> **ヒント**: Python または Microsoft C# を使用してソリューションを開発することを選択できます。 選択した言語の適切なセクションの指示に従います。

### アプリケーション構成を準備する

1. Azure AI Foundry ポータルで、プロジェクトの **[概要]** ページを表示します。
1. **[プロジェクトの詳細]** エリアで、**[プロジェクト接続文字列]** の内容を書き留めます。 この接続文字列を使用して、クライアント アプリケーションでプロジェクトに接続します。
1. 新しいブラウザー タブを開きます (既存のタブで Azure AI Foundry ポータルを開いたままにします)。 新しいブラウザー タブで [Azure portal](https://portal.azure.com) (`https://portal.azure.com`) を開き、メッセージに応じて Azure 資格情報を使用してサインインします。

    ウェルカム通知を閉じて、Azure portal のホーム ページを表示します。

1. ページ上部の検索バーの右側にある **[\>_]** ボタンを使用して、Azure portal に新しい Cloud Shell を作成し、サブスクリプションにストレージがない ***PowerShell*** 環境を選択します。

    Azure portal の下部にあるペインに Cloud Shell のコマンド ライン インターフェイスが表示されます。 作業しやすくするために、このウィンドウのサイズを変更したり最大化したりすることができます。

    > **注**: *Bash* 環境を使用するクラウド シェルを以前に作成した場合は、それを ***PowerShell*** に切り替えます。

1. Cloud Shell ツール バーの **[設定]** メニューで、**[クラシック バージョンに移動]** を選択します (これはコード エディターを使用するのに必要です)。

    **<font color="red">続行する前に、クラシック バージョンの Cloud Shell に切り替えたことを確認します。</font>**

1. Cloud Shell 画面で、次のコマンドを入力して、この演習のコード ファイルを含む GitHub リポジトリをクローンします (コマンドを入力するか、クリップボードにコピーしてから、コマンド ラインで右クリックし、プレーンテキストとして貼り付けます)。


    ```
    rm -r mslearn-ai-audio -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-language mslearn-ai-audio
    ```

    > **ヒント**: Cloudshell にコマンドを貼り付けると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。

1. リポジトリが複製されたら、アプリケーション コード ファイルを含むフォルダーに移動します。  

    **Python**

    ```
    cd mslearn-ai-audio/Labfiles/09-audio-chat/Python
    ```

    **C#**

    ```
    cd mslearn-ai-audio/Labfiles/09-audio-chat/C-sharp
    ```

1. Cloud Shell コマンド ライン ペインで、次のコマンドを入力して、これから使用するライブラリをインストールします。

    **Python**

    ```
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-identity azure-ai-projects azure-ai-inference
    ```

    **C#**

    ```
    dotnet add package Azure.Identity
    dotnet add package Azure.AI.Inference --version 1.0.0-beta.3
    dotnet add package Azure.AI.Projects --version 1.0.0-beta.3
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

    ファイルがコード エディターで開きます。

1. コード ファイルで、**your_project_connection_string** プレースホルダーをプロジェクトの接続文字列 (Azure AI Foundry ポータルでプロジェクトの **[概要]** ページからコピーしたもの) に置き換え、**your_model_deployment** プレースホルダーを Phi-4-multimodal-instruct モデル デプロイに割り当てた名前に置き換えます。

1. プレースホルダーを置き換えたら、コード エディターで、**Ctrl + S** コマンドまたは**右クリック メニューの [保存]** を使用して変更を保存したあと、**Ctrl + Q** コマンドまたは**右クリック メニューの [終了]** を使用して、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

### プロジェクトに接続してモデルのためにチャット クライアントを取得するためのコードを記述する

> **ヒント**: コードを追加する際は、必ず正しいインデントを維持してください。

1. 次のコマンドを入力して、提供されているコード ファイルを編集します。

    **Python**

    ```
    code audio-chat.py
    ```

    **C#**

    ```
    code Program.cs
    ```

1. コード ファイルで、ファイルの先頭に追加された既存のステートメントを書き留めて、必要な SDK 名前空間をインポートします。 次に、コメント**参照の追加**を探して、次のコードを追加し、前にインストールしたライブラリの名前空間を参照します。

    **Python**

    ```python
    # Add references
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.inference.models import (
        SystemMessage,
        UserMessage,
        TextContentItem,
    )
    ```

    **C#**

    ```csharp
    // Add references
    using Azure.Identity;
    using Azure.AI.Projects;
    using Azure.AI.Inference;
    ```

1. **main** 関数のコメント**構成設定の取得**で、構成ファイルで定義したプロジェクト接続文字列とモデル デプロイ名の値がコードで読み込まれることに注意してください。

1. コメント**プロジェクト クライアントの初期化**を探して、次のコードを追加し、現在のサインインに使用した Azure 資格情報で Azure AI Foundry プロジェクトに接続します。

    **Python**

    ```python
    # Initialize the project client
    project_client = AIProjectClient.from_connection_string(
        conn_str=project_connection,
        credential=DefaultAzureCredential())
    ```

    **C#**

    ```csharp
    // Initialize the project client
    var projectClient = new AIProjectClient(project_connection,
                        new DefaultAzureCredential());
    ```

1. コメント **"Get a chat client"** を見つけ、次のコードを追加して、モデルとチャットするためのクライアント オブジェクトを作成します。

    **Python**

    ```python
    # Get a chat client
    chat_client = project_client.inference.get_chat_completions_client(model=model_deployment)
    ```

    **C#**

    ```csharp
    // Get a chat client
    ChatCompletionsClient chat = projectClient.GetChatCompletionsClient();
    ```
    

### URL ベースの音声プロンプトを送信するためのコードを記述する

1. コード エディターで、**audio-chat.py** ファイルのループ セクションの **Get a response to audio input** (音声入力への応答を取得する) というコメントの下に次のコードを追加して、次の音声を含むプロンプトを送信するようにします。

    <video controls src="../media/avocados.mp4" title="アボカドの要求" width="150"></video>

    **Python**

    ```python
    # Get a response to audio input
    file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
    response = chat_client.complete(
        messages=[
            SystemMessage(system_message),
            UserMessage(
                [
                    TextContentItem(text=prompt),
                    {
                        "type": "audio_url",
                        "audio_url": {"url": file_path}
                    }
                ]
            )
        ]
    )
    print(response.choices[0].message.content)
    ```

    **C#**

    ```csharp
    // Get a response to audio input
    string audioUrl = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3";
    var requestOptions = new ChatCompletionsOptions()
    {
        Messages =
        {
            new ChatRequestSystemMessage(system_message),
            new ChatRequestUserMessage(
                new ChatMessageTextContentItem(prompt),
                new ChatMessageAudioContentItem(new Uri(audioUrl))),
        },
        Model = model_deployment
    };
    var response = chat.Complete(requestOptions);
    Console.WriteLine(response.Value.Content);
    ```

1. **CTRL + S** コマンドを使用して、変更をコード ファイルに保存します。 必要に応じて、コード エディターを閉じる (**CTRL + Q**) こともできます。

1. コード エディターの下の Cloud Shell コマンド ライン ペインで、次のコマンドを入力してアプリを実行します。

    **Python**

    ```
    python audio-chat.py
    ```

    **C#**

    ```
    dotnet run
    ```

1. メッセージが表示されたら、プロンプトを入力します。 

    ```
    Can you summarize this customer's voice message?
    ```

1. 応答を確認します。

### 別のオーディオ ファイルを使用する

1. コード エディターで開いたアプリ コードで、前に **Get a response to audio input** (音声入力への応答を取得する) というコメントの下に追加したコードを見つけます。 次に、コードを次のように変更して、別のオーディオ ファイルを選択します。

    <video controls src="../media/fresas.mp4" title="イチゴの要求" width="150"></video>

    **Python**

    ```python
    # Get a response to audio input
    file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/fresas.mp3"
    response = chat_client.complete(
        messages=[
            SystemMessage(system_message),
            UserMessage(
                [
                    TextContentItem(text=prompt),
                    {
                        "type": "audio_url",
                        "audio_url": {"url": file_path}
                    }
                ]
            )
        ]
    )
    print(response.choices[0].message.content)
    ```

    **C#**

    ```csharp
    // Get a response to audio input
    string audioUrl = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/fresas.mp3";
    var requestOptions = new ChatCompletionsOptions()
    {
        Messages =
        {
            new ChatRequestSystemMessage(system_message),
            new ChatRequestUserMessage(
                new ChatMessageTextContentItem(prompt),
                new ChatMessageAudioContentItem(new Uri(audioUrl))),
        },
        Model = model_deployment
    };
    var response = chat.Complete(requestOptions);
    Console.WriteLine(response.Value.Content);
    ```

1. **CTRL + S** コマンドを使用して、変更をコード ファイルに保存します。 必要に応じて、コード エディターを閉じる (**CTRL + Q**) こともできます。

1. コード エディターの下の Cloud Shell コマンド ライン ペインで、次のコマンドを入力してアプリを実行します。

    **Python**

    ```
    python audio-chat.py
    ```

    **C#**

    ```
    dotnet run
    ```

1. メッセージが表示されたら、次のプロンプトを入力します。 
    
    ```
    Can you summarize this customer's voice message? Is it time-sensitive?
    ```

1. 応答を確認します。 次に、「`quit`」と入力してプログラムを終了します。

    > **注**: このシンプルなアプリには、会話履歴を保持するためのロジックが含まれていないので、モデルは、各プロンプトを前のプロンプトのコンテキストを持たない新しいリクエストとして処理します。

1. 引き続きアプリを実行し、さまざまなプロンプトの種類を選択して、異なるプロンプトを試すことができます。 終了したら、`quit` を入力してプログラムを終了します。

    時間があれば、別のシステム プロンプトと、インターネットからアクセスできる独自の音声ファイルを使用するようにコードを変更してもかまいません。

    > **注**: このシンプルなアプリには、会話履歴を保持するためのロジックが含まれていないので、モデルは、各プロンプトを前のプロンプトのコンテキストを持たない新しいリクエストとして処理します。

## まとめ

この演習では、Azure AI Foundry と Azure AI 推論 SDK を使用して、マルチモーダル モデルを使用して音声への応答を生成するクライアント アプリケーションを作成しました。

## クリーンアップ

Azure AI Foundry を確認し終わったら、不要な Azure コストが発生しないように、この演習で作成したリソースを削除する必要があります。

1. Azure portal が表示されているブラウザー タブに戻り (または、新しいブラウザー タブで `https://portal.azure.com` の [Azure portal](https://portal.azure.com) をもう一度開き)、この演習で使用したリソースがデプロイされているリソース グループの内容を表示します。
1. ツール バーの **[リソース グループの削除]** を選びます。
1. リソース グループ名を入力し、削除することを確認します。

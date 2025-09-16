---
lab:
  title: 音声対応チャット アプリを開発する
  description: Azure AI Foundry を使用して、音声入力をサポートする生成 AI アプリを構築する方法について説明します。
---

# 音声対応チャット アプリを開発する

この演習では、*Phi-4-multimodal-instruct* 生成 AI モデルを使用して、音声ファイルを含むプロンプトに対する応答を生成します。 顧客が残した音声メッセージを要約することで農産物サプライヤー会社に AI 支援を提供するアプリを、Azure AI Foundry と Python OpenAI SDK を使用して開発します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用して同様のアプリケーションを開発できます。

- [Python 向け Azure AI プロジェクト](https://pypi.org/project/azure-ai-projects)
- [Python 用 OpenAI ライブラリ](https://pypi.org/project/openai/)
- [Microsoft .NET 向け Azure AI プロジェクト](https://www.nuget.org/packages/Azure.AI.Projects)
- [Microsoft .NET 用 Azure OpenAI クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.OpenAI)
- [JavaScript 向け Azure AI プロジェクト](https://www.npmjs.com/package/@azure/ai-projects)
- [TypeScript 用 Azure OpenAI ライブラリ](https://www.npmjs.com/package/@azure/openai)

この演習は約 **30** 分かかります。

## Azure AI Foundry プロジェクトを作成する

まず、Azure AI Foundry プロジェクトにモデルをデプロイします。

1. Web ブラウザーで [Azure AI Foundry ポータル](https://ai.azure.com) (`https://ai.azure.com`) を開き、Azure 資格情報を使用してサインインします。 初めてサインインするときに開いたヒントまたはクイック スタート ウィンドウを閉じます。また、必要に応じて左上にある **Azure AI Foundry** ロゴを使用してホーム ページに移動します。それは次の画像のようになります。

    ![Azure AI Foundry ポータルのスクリーンショット。](../media/ai-foundry-home.png)

1. ホーム ページの **[モデルと機能を調査する]** セクションで、プロジェクトで使用する `Phi-4-multimodal-instruct` モデルを検索します。
1. 検索結果で **Phi-4-multimodal-instruct** モデルを選んで詳細を確認してから、モデルのページの上部にある **[このモデルを使用する]** を選択します。
1. プロジェクトの作成を求められたら、プロジェクトの有効な名前を入力し、**[詳細]** オプションを展開します。
1. **[カスタマイズ]** を選択し、ハブに次の設定を指定します。
    - **Azure AI Foundry リソース**: *Azure AI Foundry リソースの有効な名前*
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **リソース グループ**: *リソース グループを作成または選択します*
    - **リージョン**: **AI Foundry が推奨する**もの*の中から選択します\*

    > \* 一部の Azure AI リソースは、リージョンのモデル クォータによって制限されます。 演習の後半でクォータ制限を超えた場合は、別のリージョンに別のリソースを作成する必要が生じる可能性があります。 [Azure AI Foundry のドキュメント](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless-availability#region-availability)で、特定のモデルの、最新のリージョン別の使用可能性を確認できます

1. **[作成]** を選択して、プロジェクトが作成されるまで待ちます。

    この操作が完了するまで数分かかる場合があります。

1. **[同意して続行]** を選択してモデルの使用条件に同意し、**[デプロイ]** を選択して Phi モデルのデプロイを完了します。

1. プロジェクトが作成されると、モデルの詳細が自動的に開きます。 モデル デプロイの名前に注目します (**Phi-4-multimodal-instruct** となっているはずです)

1. 左側のナビゲーション ウィンドウで **[概要]** を選択すると、プロジェクトのメイン ページが表示されます。次のようになります。

    > **注**: *アクセス許可が不十分です** というエラーが表示された場合は、**[修正]** ボタンを使用してエラーを解決します。

    ![Azure AI Foundry プロジェクトの概要ページのスクリーンショット。](../media/ai-foundry-project.png)

## クライアント アプリケーションを作成する

これでモデルをデプロイしたので、Azure AI Foundry SDK と Azure AI モデル推論 SDK を使用して、モデルとチャットするアプリケーションを開発できます。

> **ヒント**: Python または Microsoft C# を使用してソリューションを開発することを選択できます。 選択した言語の適切なセクションの指示に従います。

### アプリケーション構成を準備する

1. Azure AI Foundry ポータルで、プロジェクトの **[概要]** ページを表示します。
1. **[プロジェクトの詳細]** エリアの **[Azure AI Foundry プロジェクト エンドポイント]** をメモします。 クライアント アプリケーションで、このエンドポイントを使用してプロジェクトに接続します。
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
   git clone https://github.com/MicrosoftLearning/mslearn-ai-language
    ```

    > **ヒント**: Cloudshell にコマンドを貼り付けると、出力が大量のスクリーン バッファーを占有する可能性があります。 `cls` コマンドを入力して、各タスクに集中しやすくすることで、スクリーンをクリアできます。

1. リポジトリが複製されたら、アプリケーション コード ファイルを含むフォルダーに移動します。  

    ```
   cd mslearn-ai-language/Labfiles/09-audio-chat/Python
    ````

1. Cloud Shell コマンド ライン ペインで、次のコマンドを入力して、これから使用するライブラリをインストールします。

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-identity azure-ai-projects openai
    ```

1. 次のコマンドを入力して、提供されている構成ファイルを編集します。

    ```
   code .env
    ```

    ファイルがコード エディターで開きます。

1. コード ファイルで、**your_project_endpoint** プレースホルダーをプロジェクトのエンドポイント (Azure AI Foundry ポータルでプロジェクトの **[概要]** ページからコピーしたもの) に置き換え、**your_model_deployment** プレースホルダーを Phi-4-multimodal-instruct モデル デプロイに割り当てた名前に置き換えます。

1. プレースホルダーを置き換えたら、コード エディターで、**Ctrl + S** コマンドまたは**右クリック メニューの [保存]** を使用して変更を保存したあと、**Ctrl + Q** コマンドまたは**右クリック メニューの [終了]** を使用して、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

### プロジェクトに接続してモデルのためにチャット クライアントを取得するためのコードを記述する

> **ヒント**: コードを追加する際は、必ず正しいインデントを維持してください。

1. 次のコマンドを入力して、コード ファイルを編集します。

    ```
   code audio-chat.py
    ```

1. コード ファイルで、ファイルの先頭に追加された既存のステートメントを書き留めて、必要な SDK 名前空間をインポートします。 次に、コメント**参照の追加**を探して、次のコードを追加し、前にインストールしたライブラリの名前空間を参照します。

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient
    ```

1. **main** 関数のコメント**構成設定の取得**で、構成ファイルで定義したプロジェクト接続文字列とモデル デプロイ名の値がコードで読み込まれることに注意してください。

1. コメント **Initialize the project client** を見つけて、次のコードを追加し、Azure AI Foundry プロジェクトに接続します。

    > **ヒント**: コードのインデント レベルを正しく維持するように注意してください。

    ```python
   # Initialize the project client
   project_client = AIProjectClient(            
       credential=DefaultAzureCredential(
           exclude_environment_credential=True,
           exclude_managed_identity_credential=True
       ),
       endpoint=project_endpoint,
   )
    ```

1. コメント **"Get a chat client"** を見つけ、次のコードを追加して、モデルとチャットするためのクライアント オブジェクトを作成します。

    ```python
   # Get a chat client
   openai_client = project_client.get_openai_client(api_version="2024-10-21")
    ```

### 音声ベースのプロンプトを送信するためのコードを書く

プロンプトを送信する前に、要求のオーディオ ファイルをエンコードする必要があります。 その後、LLM のプロンプトを使用して、ユーザーのメッセージにオーディオ データを添付できます。 コードには、ユーザーが「quit」と入力するまでプロンプトを入力できるようにするループが含まれていることに注意してください。 

1. **Encode the audio file** というコメントの下に次のコードを入力して、次のオーディオ ファイルを準備します。

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/avocados.mp4" title="アボカドの要求" width="150"></video>

    ```python
   # Encode the audio file
   file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
   response = requests.get(file_path)
   response.raise_for_status()
   audio_data = base64.b64encode(response.content).decode('utf-8')
    ```

1. **Get a response to audio input** というコメントの下に次のコードを追加して、プロンプトを送信します。

    ```python
   # Get a response to audio input
   response = openai_client.chat.completions.create(
       model=model_deployment,
       messages=[
           {"role": "system", "content": system_message},
           { "role": "user",
               "content": [
               { 
                   "type": "text",
                   "text": prompt
               },
               {
                   "type": "input_audio",
                   "input_audio": {
                       "data": audio_data,
                       "format": "mp3"
                   }
               }
           ] }
       ]
   )
   print(response.choices[0].message.content)
    ```

1. **CTRL + S** コマンドを使用して、変更をコード ファイルに保存します。 必要に応じて、コード エディターを閉じる (**CTRL + Q**) こともできます。

### Azure にサインインしてアプリを実行する

1. Cloud Shell コマンド ライン ペインで、次のコマンドを入力して Azure にサインインします。

    ```
   az login
    ```

    **<font color="red">Cloud Shell セッションが既に認証されている場合でも、Azure にサインインする必要があります。</font>**

    > **注**: ほとんどのシナリオでは、*az ログイン*を使用するだけで十分です。 ただし、複数のテナントにサブスクリプションがある場合は、*[--tenant]* パラメーターを使用してテナントを指定する必要があります。 詳細については、「[Azure CLI を使用して対話形式で Azure にサインインする](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)」を参照してください。
    
1. メッセージが表示されたら、指示に従って新しいタブでサインイン ページを開き、指定された認証コードと Azure 資格情報を入力します。 次に、コマンド ラインでサインイン プロセスを完了し、プロンプトが表示されたら、Azure AI Foundry ハブを含むサブスクリプションを選択します。

1. Cloud Shell コマンド ライン ペインで、次のコマンドを入力してアプリを実行します。

    ```
   python audio-chat.py
    ```

1. メッセージが表示されたら、プロンプトを入力します。 

    ```
   Can you summarize this customer's voice message?
    ```

1. 応答を確認します。

### 別のオーディオ ファイルを使用する

1. コード エディターで開いたアプリ コードで、先ほど **Encode the audio file** というコメントの下に追加したコードを見つけます。 次に、要求に別のオーディオ ファイルを使用するためにファイル パスの URL を以下のように変更します (ファイル パスの後の既存のコードはそのままにします)。

    ```python
   # Encode the audio file
   file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/fresas.mp3"
    ```

    新しいファイルは次のように聞こえます。

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/fresas.mp4" title="イチゴの要求" width="150"></video>

 1. **CTRL + S** コマンドを使用して、変更をコード ファイルに保存します。 必要に応じて、コード エディターを閉じる (**CTRL + Q**) こともできます。

1. コード エディターの下の Cloud Shell コマンド ライン ペインで、次のコマンドを入力してアプリを実行します。

    ```
   python audio-chat.py
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

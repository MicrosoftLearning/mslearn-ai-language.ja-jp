---
lab:
  title: テキストの翻訳
  description: Azure AI 翻訳を使用して、サポートされている言語間で提供されたテキストを翻訳します。
---

# テキストの翻訳

**Azure AI 翻訳**は、言語間でテキストを翻訳できるようにするサービスです。 この演習では、これを使用して、サポートされている任意の言語の入力を任意のターゲット言語に変換する単純なアプリを作成します。

この演習は Python に基づいていますが、次のような複数の言語固有の SDK を使用してテキスト翻訳アプリケーションを開発できます。

- [Python 用 Azure AI Translation クライアント ライブラリ](https://pypi.org/project/azure-ai-translation-text/)
- [.NET 用 Azure AI Translation クライアント ライブラリ](https://www.nuget.org/packages/Azure.AI.Translation.Text)
- [JavaScript 用 Azure AI Translation クライアント ライブラリ](https://www.npmjs.com/package/@azure-rest/ai-translation-text)

この演習は約 **30** 分かかります。

## *Azure AI 翻訳*リソースをプロビジョニングする

サブスクリプションに **Azure AI 翻訳**リソースがまだない場合は、プロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部の検索フィールドで、**Translators** を検索し、結果で **Translators** を選択します。
1. 次の設定を使ってリソースを作成します。
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **[リソース グループ]**: *リソース グループを作成または選択します*
    - **[リージョン]**: *使用できるリージョンを選択します*
    - **[名前]**: *一意の名前を入力します*
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## Cloud Shell でアプリを開発する準備をする

Azure AI 翻訳のテキスト翻訳機能をテストするため、Azure Cloud Shell で簡単なコンソール アプリケーションを開発します。

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
   cd mslearn-ai-language/Labfiles/06-translator-sdk/Python/translate-text
    ```

## アプリケーションを構成する

1. コマンド ライン ペインで次のコマンドを実行して、**translate-text** フォルダー内のコード ファイルを表示します。

    ```
   ls -a -l
    ```

    これらのファイルとしては、構成ファイル (**.env**) とコード ファイル (**translate.py**) があります。

1. 次のコマンドを実行して、Python 仮想環境を作成し、Azure AI Translation SDK パッケージとその他の必要なパッケージをインストールします。

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-translation-text==1.0.1
    ```

1. 次のコマンドを入力して、アプリケーション構成ファイルを編集します。

    ```
   code .env
    ```

    このファイルをコード エディターで開きます。

1. 作成した Azure AI 翻訳リソースの**リージョン**と**キー**を含むように構成値を更新します (Azure portal の Azure AI 翻訳リソースの「**キーとエンドポイント**」ページで使用できます)。

    > **注**: エンドポイントでは<u>なく</u>、必ずリソースの*リージョン*を追加してください。

1. プレースホルダーを置き換えたら、コード エディター内で、**Ctrl + S** コマンドを使用するか、**右クリックして保存**で変更を保存してから、**Ctrl + Q** コマンドを使用するか、**右クリックして終了**で、Cloud Shell コマンド ラインを開いたままコード エディターを閉じます。

## テキストを翻訳するコードを追加する

1. 次のコマンドを入力して、アプリケーション コード ファイルを編集します。

    ```
   code translate.py
    ```

1. 既存のコードを確認します。 Azure AI Translation SDK を操作するコードを追加します。

    > **ヒント**: コード ファイルにコードを追加する際は、必ず正しいインデントを維持してください。

1. コード ファイルの上部にある既存の名前空間参照の下で、**Import namespaces (名前空間をインポートする)** というコメントを検索し、Translation SDK を使用するために必要な名前空間をインポートする次のコードを追加します。

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.translation.text import *
   from azure.ai.translation.text.models import InputTextItem
    ```

1. **main** 関数で、既存のコードが構成設定を読み取ることに注目してください。
1. 「**Create client using endpoint and key**」というコメントを見つけ、次のコードを追加します。

    ```python
   # Create client using endpoint and key
   credential = AzureKeyCredential(translatorKey)
   client = TextTranslationClient(credential=credential, region=translatorRegion)
    ```

1. **Choose target language (ターゲット言語を選択する)** というコメントを検索し、次のコードを追加します。これにより、Text Translator サービスを使用して翻訳でサポートされている言語の一覧が返され、ターゲット言語の言語コードを選択するようにユーザーにダイアログが表示されます。

    ```python
   # Choose target language
   languagesResponse = client.get_supported_languages(scope="translation")
   print("{} languages supported.".format(len(languagesResponse.translation)))
   print("(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
   print("Enter a target language code for translation (for example, 'en'):")
   targetLanguage = "xx"
   supportedLanguage = False
   while supportedLanguage == False:
        targetLanguage = input()
        if  targetLanguage in languagesResponse.translation.keys():
            supportedLanguage = True
        else:
            print("{} is not a supported language.".format(targetLanguage))
    ```

1. **Translate text (テキストを翻訳する)** というコメントを検索し、次のコードを追加します。これにより、翻訳するテキストを入力し、Azure AI 翻訳サービスを使用してターゲット言語 (ソース言語は自動的に検出されます) に翻訳するように示すダイアログが繰り返し表示されます。ユーザーが *quit* と入力するまで結果が表示されます。

    ```python
   # Translate text
   inputText = ""
   while inputText.lower() != "quit":
        inputText = input("Enter text to translate ('quit' to exit):")
        if inputText != "quit":
            input_text_elements = [InputTextItem(text=inputText)]
            translationResponse = client.translate(body=input_text_elements, to_language=[targetLanguage])
            translation = translationResponse[0] if translationResponse else None
            if translation:
                sourceLanguage = translation.detected_language
                for translated_text in translation.translations:
                    print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")
    ```

1. 変更を保存し (Ctrl + S)、次のコマンドを入力してプログラムを実行します (コマンド ライン ペインのテキストをより多く表示するには、[Cloud Shell] ペインを最大化し、パネルをサイズ変更します)。

    ```
   python translate.py
    ```

1. メッセージが表示されたら、表示された一覧から有効なターゲット言語を入力します。
1. 翻訳する語句 (たとえば `This is a test` または `C'est un test`) を入力し、結果を表示します。結果は、ソース言語を検出し、テキストをターゲット言語に翻訳する必要があります。
1. 完了したら、「`quit`」と入力します。 アプリケーションをもう一度実行し、別のターゲット言語を選択できます。

## リソースをクリーンアップする

Azure AI 翻訳サービスを調べ終えたら、この演習で作成したリソースを削除できます。 方法は以下のとおりです。

1. [Azure Cloud Shell] ペインを閉じます
1. Azure portal で、このラボで作成した Azure AI 翻訳リソースを参照します。
1. [リソース] ページで **[削除]** を選択し、指示に従ってリソースを削除します。

## 詳細

**Azure AI 翻訳**の使用の詳細については、「[Azure AI 翻訳のドキュメント](https://learn.microsoft.com/azure/ai-services/translator/)」を参照してください。

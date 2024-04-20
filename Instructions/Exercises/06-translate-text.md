---
lab:
  title: テキストの翻訳
  module: Module 3 - Getting Started with Natural Language Processing
---

# テキストの翻訳

**Azure AI 翻訳**は、言語間でテキストを翻訳できるようにするサービスです。 この演習では、これを使用して、サポートされている任意の言語の入力を任意のターゲット言語に変換する単純なアプリを作成します。

## *Azure AI 翻訳*リソースをプロビジョニングする

サブスクリプションに **Azure AI 翻訳**リソースがまだない場合は、プロビジョニングする必要があります。

1. Azure portal (`https://portal.azure.com`) を開き、ご利用の Azure サブスクリプションに関連付けられている Microsoft アカウントを使用してサインインします。
1. 上部の [検索] フィールドで「**Azure AI サービス**」を検索して **Enter** キーを押し、結果から **[翻訳]** の下にある **[作成]** を選択します。
1. 次の設定を使ってリソースを作成します。
    - **[サブスクリプション]**:"*ご自身の Azure サブスクリプション*"
    - **[リソース グループ]**: *リソース グループを作成または選択します*
    - **[リージョン]**: *使用できるリージョンを選択します*
    - **[名前]**: *一意の名前を入力します*
    - **価格レベル**: F が利用できない場合、**F0** (*Free*) または **S** (*Standard*) を選択します。
    - **責任ある AI 通知**: 同意。
1. **[確認および作成]** を選び、**[作成]** を選んでリソースをプロビジョニングします。
1. デプロイが完了するまで待ち、デプロイされたリソースに移動します。
1. **[キーとエンドポイント]** ページが表示されます。 このページの情報は、演習の後半で必要になります。

## Visual Studio Code でアプリの開発準備をする

Visual Studio Code を使用してテキスト翻訳アプリを開発します。 アプリのコード ファイルは、GitHub リポジトリで提供されています。

> **ヒント**: mslearn-ai-language** リポジトリを**既に複製している場合は、Visual Studio Code で開きます。 それ以外の場合は、次の手順に従って開発環境に複製します。

1. Visual Studio Code を起動します。
2. パレットを開き (SHIFT+CTRL+P)、**Git:Clone** コマンドを実行して、`https://github.com/MicrosoftLearning/mslearn-ai-language` リポジトリをローカル フォルダーに複製します (どのフォルダーでも問題ありません)。
3. リポジトリを複製したら、Visual Studio Code でフォルダーを開きます。
4. リポジトリ内の C# コード プロジェクトをサポートするために追加のファイルがインストールされるまで待ちます。

    > **注**: ビルドとデバッグに必要なアセットを追加するように求めるプロンプトが表示された場合は、**[今はしない]** を選択します。

## アプリケーションを構成する

C# と Python の両方のアプリケーションが提供されています。 どちらのアプリにも同じ機能があります。 まず、Azure AI 翻訳リソースの使用を有効にするために、アプリケーションのいくつかの重要な部分を完成します。

1. Visual Studio Code の **[エクスプローラー]** ペインで、**Labfiles/06b-translator-sdk** フォルダーを参照し、言語の設定とそこに含まれている **translate-text** フォルダーに応じて **CSharp** または **Python** フォルダーを展開します。 各フォルダーには、Azure AI 翻訳機能を統合するアプリの言語固有のコード ファイルが含まれています。
2. コード ファイルを含んだ **translate-text** フォルダーを右クリックして、統合ターミナルを開きます。 次に、言語設定に適したコマンドを実行して、Azure AI 翻訳 SDK パッケージをインストールします。

    **C#:**

    ```
    dotnet add package Azure.AI.Translation.Text --version 1.0.0-beta.1
    ```

    **Python**:

    ```
    pip install azure-ai-translation-text==1.0.0b1
    ```

3. **[エクスプローラー]** ペインの **translate-text** フォルダーで、優先する言語の構成ファイルを開きます

    - **C#**: appsettings.json
    - **Python**: .env
    
4. 作成した Azure AI 翻訳リソースの**リージョン**と**キー**を含むように構成値を更新します (Azure portal の Azure AI 翻訳リソースの「**キーとエンドポイント**」ページで使用できます)。

    > **注**: エンドポイントでは<u>なく</u>、必ずリソースの*リージョン*を追加してください。

5. 構成ファイルを保存します。

## テキストを翻訳するコードを追加する

これで、Azure AI 翻訳を使用してテキストを翻訳する準備ができました。

1. **translate-text** フォルダーには、クライアント アプリケーションのコード ファイルが含まれていることに注意してください。

    - **C#**: Program.cs
    - **Python**: translate.py

    コード ファイルを開き、上部の既存の名前空間参照の下で、「**Import namespaces**」というコメントを見つけます。 次に、このコメントの下に、次の言語固有のコードを追加して、Text Analytics SDK を使用するために必要な名前空間インポートします。

    **C#**: Programs.cs

    ```csharp
    // import namespaces
    using Azure;
    using Azure.AI.Translation.Text;
    ```

    **Python**: translate.py

    ```python
    # import namespaces
    from azure.ai.translation.text import *
    from azure.ai.translation.text.models import InputTextItem
    ```

1. **Main** 関数で、既存のコードが構成設定を読み取ることに注意してください。
1. 「**Create client using endpoint and key**」というコメントを見つけ、次のコードを追加します。

    **C#**: Programs.cs

    ```csharp
    // Create client using endpoint and key
    AzureKeyCredential credential = new(translatorKey);
    TextTranslationClient client = new(credential, translatorRegion);
    ```

    **Python**: translate.py

    ```python
    # Create client using endpoint and key
    credential = TranslatorCredential(translatorKey, translatorRegion)
    client = TextTranslationClient(credential)
    ```

1. 「**Choose target language**」というコメントを見つけて、次のコードを追加します。このコードは、テキスト翻訳サービスを使用して翻訳でサポートされている言語の一覧を返し、ターゲット言語の言語コードを選択するようにユーザーに求めます。

    **C#**: Programs.cs

    ```csharp
    // Choose target language
    Response<GetLanguagesResult> languagesResponse = await client.GetLanguagesAsync(scope:"translation").ConfigureAwait(false);
    GetLanguagesResult languages = languagesResponse.Value;
    Console.WriteLine($"{languages.Translation.Count} languages available.\n(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)");
    Console.WriteLine("Enter a target language code for translation (for example, 'en'):");
    string targetLanguage = "xx";
    bool languageSupported = false;
    while (!languageSupported)
    {
        targetLanguage = Console.ReadLine();
        if (languages.Translation.ContainsKey(targetLanguage))
        {
            languageSupported = true;
        }
        else
        {
            Console.WriteLine($"{targetLanguage} is not a supported language.");
        }

    }
    ```

    **Python**: translate.py

    ```python
    # Choose target language
    languagesResponse = client.get_languages(scope="translation")
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

1. 「**Translate text**」というコメントを見つけて、次のコードを追加します。このコードは、ユーザーにテキストの翻訳を繰り返し求め、Azure AI 翻訳 サービスを使用してターゲット言語に翻訳し (ソース言語を自動的に検出)、ユーザーが「*quit*」と入力するまで結果を表示します。

    **C#**: Programs.cs

    ```csharp
    // Translate text
    string inputText = "";
    while (inputText.ToLower() != "quit")
    {
        Console.WriteLine("Enter text to translate ('quit' to exit)");
        inputText = Console.ReadLine();
        if (inputText.ToLower() != "quit")
        {
            Response<IReadOnlyList<TranslatedTextItem>> translationResponse = await client.TranslateAsync(targetLanguage, inputText).ConfigureAwait(false);
            IReadOnlyList<TranslatedTextItem> translations = translationResponse.Value;
            TranslatedTextItem translation = translations[0];
            string sourceLanguage = translation?.DetectedLanguage?.Language;
            Console.WriteLine($"'{inputText}' translated from {sourceLanguage} to {translation?.Translations[0].To} as '{translation?.Translations?[0]?.Text}'.");
        }
    } 
    ```

    **Python**: translate.py

    ```python
    # Translate text
    inputText = ""
    while inputText.lower() != "quit":
        inputText = input("Enter text to translate ('quit' to exit):")
        if inputText != "quit":
            input_text_elements = [InputTextItem(text=inputText)]
            translationResponse = client.translate(content=input_text_elements, to=[targetLanguage])
            translation = translationResponse[0] if translationResponse else None
            if translation:
                sourceLanguage = translation.detected_language
                for translated_text in translation.translations:
                    print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")
    ```

1. 変更内容をコード ファイルに保存します。

## アプリケーションのテスト

これでアプリケーションをテストする準備ができました。

1. **Translate text** フォルダーの統合ターミナルで、次のコマンドを入力してプログラムを実行します。

    - **C#**: `dotnet run`
    - **Python**: `python translate.py`

    > **ヒント**: [ターミナル] ツールバーの **最大化パネル サイズ** (**^**) アイコンを使用すると、コンソール テキストをさらに表示できます。

1. メッセージが表示されたら、表示された一覧から有効なターゲット言語を入力します。
1. 翻訳する語句 (たとえば `This is a test` または `C'est un test`) を入力し、結果を表示します。結果は、ソース言語を検出し、テキストをターゲット言語に翻訳する必要があります。
1. 完了したら、「`quit`」と入力します。 アプリケーションをもう一度実行し、別のターゲット言語を選択できます。

## クリーンアップ

プロジェクトが不要になったら、[Azure portal](https://portal.azure.com) で Azure AI 翻訳リソースを削除できます。

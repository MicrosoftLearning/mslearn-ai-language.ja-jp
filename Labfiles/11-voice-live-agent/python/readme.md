# 必要条件

## Cloud Shell で実行する

* OpenAI アクセス権を持つ Azure サブスクリプション
* Azure Cloud Shell で実行している場合、Bash シェルを選択します。 Azure CLI と Azure Developer CLI は Cloud Shell に含まれています。

## ローカルで実行する

* デプロイ スクリプトを実行した後、Web アプリをローカルで実行できます。
    * [Azure Developer CLI (azd)](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)
    * [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
    * OpenAI アクセス権を持つ Azure サブスクリプション


## 環境変数

`.env` ファイルは、*azdeploy.sh* スクリプトによって作成されます。 AI モデル エンドポイント、API キー、モデル名は、リソースのデプロイ時に追加されます。

## Azure リソースのデプロイ

提供されている `azdeploy.sh` により、Azure に必要なリソースが作成されます。

* スクリプトの先頭にある 2 つの変数をニーズに合わせて変更し、他には何も変更しないでください。
* スクリプト:
    * AZD を使用して *gpt-4o* モデルをデプロイします。
    * Azure Container Registry サービスを作成する
    * ACR タスクを使用して Dockerfile イメージをビルドし、ACR にデプロイする
    * App Service プランを作成する
    * App Service Web アプリを作成する
    * ACR のコンテナー イメージ用に Web アプリを構成する
    * Web アプリの環境変数を構成する
    * このスクリプトにより、App Service エンドポイントが提供されます

このスクリプトには、次の 2 つのデプロイ オプションが用意されています。1.  完全なデプロイ。2.  イメージのみを再デプロイ。 オプション 2 は、アプリケーションの変更を試す場合にデプロイ後にのみ使用します。 

> 注:`bash azdeploy.sh` コマンドを使用して、PowerShell または Bash でスクリプトを実行できます。このコマンドを使用すると、スクリプトを実行可能ファイルに変換することなく Bash で実行することもできます。

## ローカル開発

### AI モデルを Azure にプロビジョニングする

プロジェクトをローカルで実行し、次の手順に従って AI モデルのみをプロビジョニングできます。

1. **環境を初期化します** (わかりやすい名前を選択します)。

   ```bash
   azd env new gpt-realtime-lab --confirm
   # or: azd env new your-name-gpt-experiment --confirm
   ```
   
   **重要**: この名前は、Azure リソース名の一部になります。  
   `--confirm` フラグは、プロンプトを表示せずに、これを既定の環境として設定します。

1. **リソース グループを設定します**。

   ```bash
   azd env set AZURE_RESOURCE_GROUP "rg-your-name-gpt"
   ```

1. **AI リソースにログインしてプロビジョニングします**。

   ```bash
   az login
   azd provision
   ```

    > **重要**: `azd deploy` を実行しないでください。アプリは AZD テンプレートで構成されていません。

`azd provision` メソッドを使用してモデルのみをプロビジョニングした場合は、次のエントリを含む `.env` ファイルをディレクトリのルートに作成する必要があります。

```
AZURE_VOICE_LIVE_ENDPOINT=""
AZURE_VOICE_LIVE_API_KEY=""
VOICE_LIVE_MODEL=""
VOICE_LIVE_VOICE="en-US-JennyNeural"
VOICE_LIVE_INSTRUCTIONS="You are a helpful AI assistant with a focus on world history. Respond naturally and conversationally. Keep your responses concise but engaging."
VOICE_LIVE_VERBOSE="" #Suppresses excessive logging to the terminal if running locally
```

注:

1. エンドポイントはモデルのエンドポイントであり、`https://<proj-name>.cognitiveservices.azure.com` のみを含める必要があります。
1. API キーはモデルのキーです。
1. モデルは、デプロイ時に使用されるモデル名です。
1. これらの値は、AI Foundry ポータルから取得できます。

### ローカルでのプロジェクトの実行

プロジェクトは、**uv**を使用して作成され、管理されていますが、実行する必要はありません。 

**uv** がインストールされている場合:

* `uv venv` を実行して環境を作成します
* `uv sync` を実行してパッケージを追加します
* Web アプリ用に作成されたエイリアス: `flask_app.py` スクリプトを開始する `uv run web`。
* `uv pip compile pyproject.toml -o requirements.txt` で作成された requirements.txt ファイル

**uv** がインストールされていない場合:

* 環境を作成します: `python -m venv .venv`
* 環境をアクティブにします: `.\.venv\Scripts\Activate.ps1`
* 依存関係をインストールします: `pip install -r requirements.txt`
* (プロジェクト ルートから) アプリケーションを実行します: `python .\src\real_time_voice\flask_app.py`

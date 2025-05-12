---
title: Azure AI Language の演習
permalink: index.html
layout: home
---

# Azure AI Language の演習

次の演習は、Azure で自然言語ソリューションを構築するときに開発者が行う一般的なタスクについて調べる、実践的な学習エクスペリエンスを提供するように設計されています。 

> **注**: これらの演習を完了するには、Azure サブスクリプションが必要です。 まだお持ちでない場合は、[Azure アカウント](https://azure.microsoft.com/free)にサインアップできます。 新規ユーザーには、最初の 30 日間のクレジットが付属する無料試用版オプションがあります。

## 演習

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %} {% for activity in labs  %}
<hr>
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

{% endfor %}

<hr>

> **注**: これらの演習は単独でも完了できますが、[Microsoft Learn](https://learn.microsoft.com/training/paths/develop-language-solutions-azure-ai/) のモジュールを補完するように設計されています。このモジュールでは、これらの演習の基になる概念の一部について詳しく説明しています。 

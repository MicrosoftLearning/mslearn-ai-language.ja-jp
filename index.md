---
title: Azure で AI Language と Speech のソリューションを開発する
permalink: index.html
layout: home
---

このページには、[Microsoft Learn](https://learn.microsoft.com/training/paths/develop-language-solutions-azure-ai/) の Microsoft スキルアップ コンテンツに関連付けられている演習が記載されています

> **注**: これらの演習を完了するには、Azure サブスクリプションが必要です。 まだお持ちでない場合は、[Azure アカウント](https://azure.microsoft.com/free)にサインアップできます。 新規ユーザーには、最初の 30 日間のクレジットが付属する無料試用版オプションがあります。

## 演習

<hr>

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %}
{% for activity in labs  %}
{% if activity.lab.title %}

### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{% if activity.lab.level %}**レベル**: {{activity.lab.level}} \| {% endif %}{% if activity.lab.duration %}**期間**: {{activity.lab.duration}} 分{% endif %}

{% if activity.lab.description %}
*{{activity.lab.description}}*
{% endif %}
<hr>
{% endif %}
{% endfor %}

---
title: Azure Language の演習
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

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %} {% for activity in labs  %} {% if activity.lab.title %}

{% if activity.lab.description %}
*{{activity.lab.description}}*
{% endif %}
<hr>
{% endif %}
{% endfor %}

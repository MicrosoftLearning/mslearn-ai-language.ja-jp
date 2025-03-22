---
title: Azure AI Language の演習
permalink: index.html
layout: home
---

# Azure AI Language の演習

次の演習は、Microsoft Learn の[自然言語ソリューションの開発](https://learn.microsoft.com/training/paths/develop-language-solutions-azure-ai/)のためのモジュールをサポートするように設計されています。


{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %} {% for activity in labs  %} {% unless activity.url contains 'ai-foundry' %}
- [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }}) {% endunless %} {% endfor %}

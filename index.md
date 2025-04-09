---
title: 星树浩
layout: layout.njk
---

设计师、开发者，以及一个希望在互联网上留下些痕迹的人。  
目前在学习 AI 和产品，用技术表达自己。

这个博客收录了我写过的大部分文章，有些有趣，有些无聊。随便看看。

---

{% for post in collections.posts reversed %}
- {{ post.date | date: "%y.%m.%d" }} [{{ post.data.title }}]({{ post.url }})
{% endfor %}

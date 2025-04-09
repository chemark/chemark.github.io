---

title: 星树浩
layout: layout.njk

---

<p>设计师、开发者，以及一个希望在互联网上留下些痕迹的人。<br />
目前在学习 AI 和产品，用技术表达自己。</p>

<p>这个博客收录了我写过的大部分文章，有些有趣，有些无聊。随便看看。</p>

<hr />

<ul>
{% for post in collections.posts | reverse %}
  <li>
    {{ post.date | date: "yy.MM.dd" }} <a href="{{ post.url }}">{{ post.data.title }}</a>
  </li>
{% endfor %}
</ul>

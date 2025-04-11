module.exports = function(eleventyConfig) {
  // 注册文章集合
  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("posts/*.md");
  });

  // 添加日期过滤器
  eleventyConfig.addFilter("date", function(date, format) {
    if (!date) return "";
    const year = date.getFullYear().toString().slice(-2);
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    return `${year}.${month}.${day}`;
  });

  // 添加全局数据
  eleventyConfig.addGlobalData("isHome", false);

  // 告诉 Eleventy 拷贝 img 文件夹
  eleventyConfig.addPassthroughCopy("img");

  return {
    dir: {
      input: ".",
      includes: "_includes",
      data: "_data",
      output: "_site"
    }
  };
};

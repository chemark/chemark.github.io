module.exports = function(eleventyConfig) {
  // 注册文章集合
  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("posts/*.md");
  });

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
  
module.exports = {
  output: {
    // expose to global namespace exported variable from index.js
    library: "app",
    // ecma version compatibility
    environment: {
      // compatible for older browsers
      arrowFunction: false,
    },
  },
  externals: {
    // require("jquery") is external and available on the global var jQuery
    jquery: "jQuery",
  },
  devtool: false,
  target: "web",
};

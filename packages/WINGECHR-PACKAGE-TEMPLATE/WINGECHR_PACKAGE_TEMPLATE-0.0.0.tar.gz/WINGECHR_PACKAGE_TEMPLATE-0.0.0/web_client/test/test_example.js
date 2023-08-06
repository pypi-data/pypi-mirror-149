"use strict";

/*
 *  test with node_modules/.bin/mocha
 */

const chai = require("chai");
chai.use(require("chai-almost")());

let main = require('../src/js/__main__.js');

describe('main', function() {
  it("examplePlusOne", function() {
    chai.expect(main.examplePlusOne(1)).to.be.almost.equals(2);
  });
});

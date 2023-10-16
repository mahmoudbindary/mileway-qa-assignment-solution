# Mileway Qa Assignment Solution
[![Testing web and api](https://github.com/mahmoudbindary/mileway-qa-assignment-solution/actions/workflows/testing.yml/badge.svg)](https://github.com/mahmoudbindary/mileway-qa-assignment-solution/actions/workflows/testing.yml)
___

I'm proudly presenting this repo as my solution to Mileway's QA assignment. Test Cases Design file contains web based test cases for website [Ui Playghround](http://uitestingplayground.com/) and API tests for endpoints with base url [petstore.swagger.io/v2](https://petstore.swagger.io/#/). The rest of the repo is a Test Automation Framework built from scratch to provide test automation for the test cases inside Test Cases Design files.

## Framework Tools

* **Python 3.11:**
    * Main language used to build the framework as it's very powerful language, easy to read and write and perfect for scenarios where it's needed to cover both Web and API tests.
* **Packages:**
    * *selenium:* used for controlling web browsers and performing browser automation.
    * *webdriver-manager:* used for webdrivers versions and installation.
    * *requests:* used for handling API requests through HTTP.
    * *pytest:* used for running, organizing and controlling test cases.
    * *pytest-html:* used for generating HTML reports for pytest test runs.
    * *pytest-xdist:* used for executing parallel testing for pytest runs.
    * *jsonschema:* used for validating JSON schema for API responses.
    * *faker:* used for generating random test data for API tests.

## Framework Features

* *Page Object Model design pattern:* achieved using `helpers` package to provide a level of abstraction to test cases and to make the framework modular and easy to maintain.
* *Data-driven testing approach:* achieved using `utilitiez` package to read and provide data from json files as well as config and env files to avoid hard coding secure data.
* *Test cases parametrization:* to run the same test case with different set of test data.
* *Reporting and logging:* as for each test run a new HTML with test execution results and automation logs file should be generated and added to `src/results` folder.
* *Screenshot-on-failure:* for web test cases implemented inside `conftest.py` module to generate a .png screenshot whenever web testcase fails with the testcase name, add it to `src/results` folder and attach it to HTML report.
* *Cross-browser web test execution:* achieved by adding argument `--browser {bowser name}` inside test execution command where browser name is chrome, edge or firefox.
* *Headless web test execution:* achieved by adding argument `--headless` inside test execution command
* *Test grouping using pytest markers:* to run a specific set of test cases by adding argument `-m {test group name}` where test group name is `regression` for all testcases, `web` for Web testcases and `api` for API test cases.
* *Parallel test execution:* using pytest-xdist package by adding argument `-n {number}` or `-n auto`.
* *CI/CD integration with Github actions:* to run all test cases and save generated HTML report on push or pull requests as well as on demand, pipeline implementation is specified inside `.github/workflows/testing.yml` file.

## Test Running

### Prerequisite

* Make a clone of this repo.
* Run command `pip install -r requirements.txt` to install all required packages.

### Running the test

* To run all test cases simply execute `pytest` commands on the project root folder.
* To specify a path for the generated HTML execute `pytest --html={path}.html`
* By default, web testcases will be run on chrome browser, to run on another browser ex: edge, execute command `pytest --browser edge`
* To achieve other test run specification like running specific test group, parallel test execution or running tests in headless mode, please refer to Test Features section.

## Author ##

* **Mahmoud Bindary**  (https://github.com/mahmoudbindary)

_I really enjoyed solving this assignment and put maximum effort in it, hope you'll enjoy reviewing it as well!_

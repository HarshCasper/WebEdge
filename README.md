![WebEdge](https://socialify.git.ci/HarshCasper/WebEdge/image?description=1&descriptionEditable=Bringing%20Edge%20to%20your%20Web%20Performance%20%F0%9F%94%A5%E2%9C%A8&forks=1&issues=1&language=1&pulls=1&stargazers=1&theme=Light)

<p align="center">
	We all have  inborn  talent and also  inborn  failings, <br>
	So often  scorn  a balance, chained to our own railings, <br>
	And our world misses a website that deserved to be a star, <br>
	But not  unfurled  in all its might, merely  cowering  from  afar, <br>
	Why not take your Van  Dyke, or Rembrandt seen by few, <br>
	And let us make it see the light, exposed to global view, <br>
	Don't hide them in shadows behind barriers of your mind, <br>
	Where pride and jealous arrows make them hard to find, <br>
	Instead turn to experts just  as good as  you would like to be, <br>
    Who you'll learn to trust, and who will set your website free. <br>
</p>
<p align="center">
Developed with <span style="color: #8b0000;">&hearts;</span> by your friends at <a href="https://github.com/MLH-Fellowship">MLH Fellowship</a> Team-1.
</p>
<p align="center">
    <img src="https://img.shields.io/badge/Version-1.0.2-brightgreen" alt="version 1.0.2"/>
    <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="license MIT"/>
    <img src="https://img.shields.io/badge/Author-MLH%20Fellowship%20Team--1-yellow" alt="MLH Fellowship Team 1"/>
    <img src="https://github.com/harshcasper/webedge/actions/workflows/ci.yml/badge.svg" alt="GitHub-Actions-Build"/>
	<img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Format: Black">
	<a href="https://img.shields.io/pypi/v/webedge"><img src="https://img.shields.io/pypi/v/webedge" alt="PyPI version" height="18"></a>
</p>

## 💥 Introduction

> Bringing Edge to your Web Performance

Rise of Web  has heralded the increasing ways in which we optimize Digital Performance. With SEO and Web Performance playing an important part, Developers feel lost around Performance needs. <b>WebEdge</b> aims to fix this 🌐

WebEdge have been introduced to suggest Web Optimizations for the App that can speed up operations and boost productivity ⚡

## 💡 Why did we build it?

As Frontend Developers, Performance plays an important part for Ranking and User Experience. The priority is such that it cannot be avoided any longer. WebEdge provides a Python Package for you to scrap you Website and auto-suggest improvements you can make to improve your Optimization Ranking ♾️

With this Package, we aim to have a unified tool to improve your SEO Ranking with real-time optimizations, that you can fix as a Developer. Sounds interesting? Well it is 🔥

## 🚀 Installation

To install WebEdge, we can use `pip`:

```sh
pip3 install webedge
```

The standard Python package will setup the CLI and you can use the same for local testing and analysis of your website and webpages.

```sh
 _       __     __    ______    __         
| |     / /__  / /_  / ____/___/ /___ ____ 
| | /| / / _ \/ __ \/ __/ / __  / __ `/ _ \
| |/ |/ /  __/ /_/ / /___/ /_/ / /_/ /  __/
|__/|__/\___/_.___/_____/\__,_/\__, /\___/ 
                              /____/       


usage: webedge [-h] -d DOMAIN [-s SITEMAP] [-p PAGE]
```

## 🛠️ Local development

That's pretty easy. To ensure that you are able to install everything properly, we would recommend you to have <b>Git</b>, <b>Python</b> and <b>pip</b> installed. You should ideally work with a Virtual Environment, such as `venv` or the `virtualenv` module, to get the best out of the package.

We will first start with setting up the Local Project Environment:

```sh
git clone https://github.com/HarshCasper/WebEdge.git
cd WebEdge
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 setup.py install
```

Once you run the Commands and get everything fine, we are all set to run the tool ✔️

Let's run the tool now:

```sh
webedge -d http://[DOMAIN_NAME]/
```

* For example if your domain is `https://fastcoder.netlify.app/` then your command should be (you can use `http` or `https` in the command according to your needs):

```sh
webedge -d https://fastcoder.netlify.app/
```

Pass your Website to the tool and you will get a generated JSON highlighting all the achievements you have made in SEO Optimization or the warnings being displayed by the same 🔑

To run the tests, simply push:

```sh
nosetests --with-coverage --cover-package=webedge tests.unit
```

To build with Docker, simply push:

```sh
docker build -t 'app:webedge' .
docker run app:webedge
```

## 🛑 External Tools

The Python Files have been linted using [flake8](https://flake8.pycqa.org/) which automatically suggests linting errors and issues with formatting and styling. You can run the `flake8` command with the given configuration in the Project 🍀

We are also making use of CodeQL Analysis, which can be viewed [here](.github/workflows/codeql-analysis.yml). This allows us to identify potential bugs and anti-patterns with each push to the repository, and potentially fix it 🐛

For setting up CI/CD, we are making use of [GitHub Actions](https://github.com/features/actions). With a simple configuration set-up, we were able to test each build for specific issues, which can be viewed [here](.github/workflows/ci.yml) 🌱

## 📜 LICENSE

[MIT License](https://github.com/HarshCasper/WebEdge/blob/main/LICENSE)

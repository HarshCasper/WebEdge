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
    <img src="https://img.shields.io/badge/Version-1.0.0-brightgreen" alt="version 1.0.0"/>
    <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="license MIT"/>
    <img src="https://img.shields.io/badge/Author-MLH%20Fellowship%20Team--1-yellow" alt="MLH Fellowship Team 1"/>
    <img src="https://travis-ci.org/HarshCasper/WebEdge.svg?branch=main" alt="Travis-Build"/>
</p>

## 💥 Introduction

> Bringing Edge to your Web Performance

Rise of Web  has heralded the increasing ways in which we optimize Digital Performance. With SEO and Web Performance playing an important part, Developers feel lost around Performance needs. <b>WebEdge</b> aims to fix this 🌐

WebEdge have been introduced to suggest Web Optimizations for the App that can speed up operations and boost productivity ⚡

## 💡 Why did we build it?

As Frontend Developers, Performance plays an important part for Ranking and User Experience. The priority is such that it cannot be avoided any longer. WebEdge provides a Python Package for you to scrap you Website and auto-suggest improvements you can make to improve your Optimization Ranking ♾️

With this Package, we aim to have a unified tool to improve your SEO Ranking with real-time optimizations, that you can fix as a Developer. Sounds interesting? Well it is 🔥

## 🛠️ Usage

That's pretty easy. To ensure that you are able to install everything properly, we would recommend you to have <b>Git</b>, <b>Python</b> and <b>pip</b> installed. You should ideally work with a Virtual Environment, such as `venv` or the `virtualenv` module, to get the best out of the package. 

We will first start with setting up the Local Project Environment:
```BASH
$ git clone https://github.com/HarshCasper/WebEdge.git
$ cd WebEdge
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
(venv) $ python3 setup.py install
```
Once you run the Commands and get everything fine, we are all set to run the tool ✔️

Let's run the tool now: 
```BASH
(venv) $ webedge -d http://[DOMAIN_NAME]/
```

* For example if your domain is ajitesh13.github.io then your command should be (you can use `http` or `https` in the command according to your needs): 

```BASH
(venv) $ webedge -d https://ajitesh13.github.io/
``` 
Pass your Website to the tool and you will get a generated JSON highlighting all the achievements you have made in SEO Optimization or the warnings being displayed by the same 🔑

**Building using docker**
```bash
$ docker build -t 'app:webedge' .
$ docker run app:webedge
```

## 🛑 External Tools

The Python Files have been linted using [flake8](https://flake8.pycqa.org/) which automatically suggests linting errors and issues with formatting and styling. You can run the `flake8` command with the given configuration in the Project 🍀

We are also making use of DeepSource Analysis, which can be viewed [here](http://deepsource.io/gh/HarshCasper/webEdge). This allows us to identify potential bugs and anti-patterns with each push to the repository, and potentially fix it 🐛

For setting up CI/CD, we are making use of [Travis CI](http://travis-ci.org/). With a simple configuration set-up, we were able to test each build for specific issues, which can be viewed [here](https://travis-ci.org/github/HarshCasper/WebEdge) 🌱

## 📜 LICENSE

[MIT License](https://github.com/HarshCasper/WebEdge/blob/main/LICENSE)

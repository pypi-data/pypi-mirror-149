# Automancy
A Web UI Automation framework for Python, designed to simplify the functionality and features of Selenium.

## Motivation
Raise your hand if you've ever thought to yourself "Man... I really don't like how Selenium code is written, it's so ugly and strangely difficult to work with..."

No, nevermind, don't raise your hand, you'll just look weird, and I won't be able to see you anyway.

We all know it, Selenium is cumbersome to write, abstract in the not-so-fun way, difficult to read (thus to maintain), and rather fragile most of the time.

Automancy is meant to resolve these annoyances, regardless of if your intent is to scrape web pages, automate actions on a web portal, or create automated UI tests for a web app.

The intent of Automancy is to add a greater degree of sophisticated control to web based automation while reducing the syntactic complexity of these operations and providing a design pattern meant to facilitate anti-fragility.

If you treat input as error, automating away as much menial work for the operator as possible without taking away meaningful control, fundamentally, you are automating automation.

Hence, Automancy, the animation of automation.

![Stay awhile and listen](docs/images/stay-awhile-and-listen.jpg)

## Pre-requisites
You'll need to have your favorite browser webdriver located in a directory that is a part of the Python path variables.

That's it, pretty simple.

_(If you don't know where to find a WebDriver, or if you don't know what I'm talking about, you might need to study up on some lesser arcane magic first)_

## Installation

    pip install automancy

_(What?  You thought there would be more?)_

## First Example
There are many ways Automancy can be used, various styles of implementation supported, it all depends on the needs of your context.

This first example is intended to show a bit of executable code and to illustrate Automancy's flexibility in implementation.

We are going to automate a few actions on Wikipedia.  We want to see if anyone has written a page for Automancy yet.

**Special Note 1**: You might notice the `driver` object is not passed to any further object in the scope.  This is not an error.  Automancy includes the ability to detect and reference WebDriver instances automatically.  This will be discussed in greater detail elsewhere.

**Special Note 2**: The current version of Automancy requires the manual instantiation of a Selenium WebDriver object.  This will change before v1.0.0 is released.

Here we go, This example will be broken up into three parts and illustrate two simple ways of doing the same thing.
1. Go to the Wikipedia main page searching for 
2. Type "Automancy" into the search bar
3. Click on the search button / press enter
4. Check for the existence of an element on the results page.

### Part 1 -> Setup
```python
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from automancy import Button, Label, Page, TextInput

# Instantiate a Chrome WebDriver
driver = webdriver.Chrome(options=webdriver.ChromeOptions(), desired_capabilities=DesiredCapabilities.CHROME)
```

### Part 2-a -> Generating a Page model programmatically using the `.add(...)` method
This is the first of the two alternative methods described here for constructing a web UI model with Automancy.
```python
# Instantiate a Page object with the wikipedia main url
wikipedia = Page(url='https://en.wikipedia.org/wiki/Main_Page')

# Add the necessary Elementals to the wikipedia page.
wikipedia.add(Button('//input[@id="searchButton"]', 'Search Button', 'search_button'))
wikipedia.add(TextInput('//input[@id="searchInput"]', 'Search Input', 'search_input'))
wikipedia.add(Label('//p[@class="mw-search-nonefound"]', 'Not Found Text', 'not_found_text'))
```

### Part 2-b -> Defining a UI Model as a persistent class
This is the second alternate method of constructing a web UI model; either will work.
```python
class Wikipedia(Page):
    def __init__(self, url='https://en.wikipedia.org/wiki/Main_Page'):
        self.search_button = Button('//input[@id="searchButton"]', 'Search Button', 'search_button')
        self.search_input = TextInput('//input[@id="searchInput"]', 'Search Input', 'search_input')
        self.not_found_text = Label('//p[@class="mw-search-nonefound"]', 'Not Found Text', 'not_found_text')

wikipedia = Wikipedia()
```

### Part 3 -> Perform the actions
```python
# Go to the wikipedia main page
wikipedia.visit()

# Input the search text
wikipedia.search_input.write('Automancy')

# Click the search button
wikipedia.search_button.click()

# Check to see if the "not found" text still exists
if wikipedia.not_found_text.exists:
    print('Forever alone...')
```

### Considerations
The great thing about these two methods is that you can perform the same kinds of actions with the same commands independent of how you build your models.

Sometimes it might be advantageous to build a page model on the fly if you're in a situation where you've got extremely dynamic pages.  If this is the case, you could technically create many "components" (a-la React, Polymer, etc), and mirror your automation scripts to the UI design, adding objects to page models only as needed.

It might also be advantageous to construct more statically defined Page models as a class to mirror components or features in a web app, able to stand on its own, able to be extended easily, able to be included in a library of models representing an entire web UI, and able to have custom functions defined within it to string together multiple Elemental actions in a single call.

## How to Think About Automancy
Ecosystems & Elementals.  These are the two key terms employed within Automancy which sum up the design philosophy.  Once you understand the meaning of these two terms, you'll understand Automancy.

Here is a brief overview for simplicity's sake.  Further discussion can be found in the `docs/` directory.

### Ecosystems
Think of the term "ecosystem" in the natural sciences.  What is an ecosystem?  It's a domain of life generally speaking, a domain of complex entities interacting with each other, usually with some sort of hierarchical relationship between everything within the domain.

This analogy is used here in Automancy.  A single web page can be thought of as an ecosystem.

Simple ecosystems might only contain some text, a picture, and a button to interact with, while complex ecosystem might have animations, triggered DOM changes, modals, toast messages, video playback, etc.

The practice of Automancy is the practice of defining what exists in an ecosystem as a "model" of reality (or at least as close to it as you need).

### Elementals
If a web page is a complex ecosystem as in nature, you can think of what lives on a web page, the unique constituents of a DOM, as complex organisms, molecular structures, and atomic elements, embedded within each other as complexity decreases.

"**Elemental**", in Automancy, is the general term used for everything from a simple `Button` to a complex `HTML5VideoPlayer` object.

That said, "Elementals" are intended to be considered hierarchical in nature.  A `Form` molecule will naturally contain any number of "`TextInput`" and `Button` atoms, for example.

[comment]: <> (For this reason, Automancy considers this hierarchical structure for its module and directory path conventions.)

There are three `Elemental` types

- Atoms
- Molecules
- Organisms

**Atoms**: The least complex `Elemental`.  Each represents a single web element DOM object; a `<button`, or an `<a>`, but also checkbox, radio selector, or a text input DOM objects.

**Molecules**: Meant to be used when constructing models of DOM structures such as `<form>`, a modal, a dialogbox; they tend to be made up of Atom objects which they contain.

**Organisms**: The most complex `Elemental`, usually constructed out of many custom class objects and unique controls and internal options.  Organisms contain the means of constructing xpath selectors for their children DOM elements automatically.

## Wrapping it Up
Now you've seen a simple example of how Selenium can be simplified for the greater good.

There is much more to be said, however I feel it wise to keep this initial README.md simple enough to consume and leave you, the reader, desiring more juicy details.

Juicy details ye shall receive.

Inside the `docs/` directory is where ongoing documentation will appear.

This further documentation will take the following forms.

- Tutorials: First steps for a learner, meant to introduce concepts, build confidence, inspire, not distract, etc.
- How-Tos: Answers to specific questions about how to accomplish something in or with Automancy.
- References: Technical specification details for each class, similar to API reference documentation (but not garbage, I hope...)
- Discussions: High level conveyance of ideas, philosophies, and explanations for design choices.

I hope you'll enjoy utilizing Automancy as much as I've enjoyed creating it so far.  Please feel free to submit issues here on GitHub when you find them, it's always appreciated.

If you'd like to contribute to Automancy in any way, I'm pretty easy to reach.  The more people working on Automancy the better for all.

Thank you!
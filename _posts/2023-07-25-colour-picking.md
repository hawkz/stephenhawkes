---
layout: post
title:  Building a Color Picker App for macOS
summary: Causing a rumpus with Python and Rumps
date:   2023-07-25
categories: python macOS rumps
---

Hello there! Today, I'll be sharing a fun project I've been working on - building a color picker app for macOS using Python and Rumps. Grab a cup of coffee, sit back, and let's get into it.

## Rumps, What's That?

Let's start with Rumps. If you're wondering, it stands for "Ridiculously Uncomplicated macOS Python Statusbar apps". As the name suggests, it's a Python library that makes it ridiculously easy to create applications that live in your menu bar. However, it's worth noting that Rumps is only available for macOS.

## The Birth of the Color Picker App

The journey started when a idea came rolling in - "Can you write a Rumps app that creates a drop-down menu that lists color names, and clicking one copies the color hex code to the clipboard?". Interesting, right? The need comes from some amazing work from Paul our Creative Director, he's injected some fun into the project by naming the key colours in the brand but I need a quick way to get the hex codes to use in the project.

Initially, we thought of having the color displayed next to the color name in the drop-down menu. I quickly realized, though, that Rumps didn't support custom icons or images in the drop-down menu items. Bummer! But hey, there's always a workaround. 

## Workaround, You Say?

One idea was to create separate menu items for each color and use an emoji or colored text in the menu item label to indicate the color. But that wouldn't give us the exact color representation. Plus, the color of the text or the icon in the menu item can't be changed in Rumps. So, we had to think of something else.

Our final solution was to add a Rumps notification that pops up when a color name is clicked. This notification would have a custom icon that represented the color. Here's what the code looked like:

```python
import rumps
import pyperclip

class MyApp(rumps.App):
    @rumps.clicked("Color")
    def color_clicked(self, sender):
        rumps.notification("Color", "Color Clicked", "Color: #FF0000", icon='/path/to/icon.png')
```

## Plot Twist: Dynamic PNG Creation

The plot thickened when we realized that it's not feasible to dynamically generate a PNG file for each color and use it as the icon in the notification with Rumps. We would need to have a preexisting PNG file for each color. 

## Clipboard Copying and Callback Functions

One important feature of our app was the ability to copy the hex code of a clicked color to the clipboard. For this, we used the `pyperclip` library, which is a cross-platform Python module for copy and paste clipboard functions. We built a callback function that got triggered each time a color was clicked, copying the hex code to the clipboard. 

## The End Result

The final result was a simple yet functional color picker app for macOS. It was a great exercise in exploring the capabilities and limitations of Rumps, and we're pretty proud of what we were able to achieve.  Building this tool was a great reminder of the power of Python and its vast ecosystem of libraries. Even with its limitations, Rumps proved to be a great library for quickly whipping up macOS menu bar applications.

It was a fun couple of hours and now I'll never need to worry about what colour "Clifford the Dog" Red was again :)

Until next time, happy coding!

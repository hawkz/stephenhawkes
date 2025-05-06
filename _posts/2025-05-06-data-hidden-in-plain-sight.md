---
published: true
date: 2025-05-06
title: Data Hidden in Plain Sight
summary: Making images that quietly carry meaning, and footers that serve double duty.
categories: blog
---
Sometimes, websites need to quietly tell machines (like Google, AI tools, or screen readers) what something _means_. Not just what it looks like. That’s what structured data is for — little bits of extra information that say, “Hey, this is an organisation,” or “This is a job listing,” or “This photo is licensed for reuse.”

Usually, that info lives in the website’s code. But what if you **can’t** change the code? I've recently been playing with the idea of ISO badges (inspired by our recent re-certification) and the process of adding those annual badges to the footer of our site.

I’ve built a small working demo to show how it can be done — by hiding data inside an image.

👉 [Check it out](https://codepen.io/hawkz/pen/WbbeYOp)

Here’s how it works, in plain terms:

*   You take a normal image (like a footer graphic).
    
*   You use a technique called **steganography** — a way of tucking secret messages into images — to hide some text inside the picture. In our case, it’s JSON-LD, which is a common format for structured data, from the form.
    
*   If I need the data, I can just grab that image, then pull out the data from the second form.
    

From a visitor’s perspective, nothing looks different. But a little script that’s scanning the site can now understand more about what’s on the page — thanks to information that’s hidden inside the pixels.

## Why is this useful?

*   You can keep meaningful data attached to an image, even when it’s reused across different sites.
    
*   You can work around platforms or CMSs that don’t let you add code.
    
*   You can embed machine-readable info without cluttering the visible layout.
    

It’s not magic. It’s not foolproof. But it’s a clever solution for niche cases — where clarity, portability, or platform restrictions make it hard to do things the normal way.

So yes, it’s just a footer.  
But now, it’s a footer with something to say — even if it never says it out loud.
---
layout: post
title: Breaking the Scroll Chain
summary: Building a Chrome Extension to Kick the YouTube Habit
date: 2023-07-24
categories: blog, productivity, programming
---

We've all been there. You open YouTube to watch that one video you've been meaning to catch up on, and suddenly, it's 2 am, and you're watching a documentary about the migratory patterns of African elephants. "How did I get here?", you wonder. Well, my friend, welcome to the world of YouTube scrolling addiction. A seemingly innocent pastime, but one that can turn into a pretty hefty personal challenge - just the way they engineered it! Today, I'll be turning the tables on this productivity zapper by building a Chrome extension that shuts down any tab that navigates to YouTube. Sounds fun? Let's dive right in!

## The Journey Begins

Our quest began with the basic structure of a Chrome extension, which includes two key files: `manifest.json` (the metadata for the extension) and `background.js` (where the JavaScript magic happens). With `manifest.json`, I declared the extension's name, version, description, and permissions. In `background.js`, I added a simple script to close the tab if the URL contains 'youtube.com'. 

I bet you're thinking, "That's it? We're done?" Well, not quite. While I was on the right track, I realized our extension was a tad overzealous. It was closing tabs not just when the domain was 'youtube.com', but even when 'youtube.com' was part of another hostname or elsewhere in the URL. I decided to use the URL API to parse the URL and specifically check the domain, a few tweaks to our `background.js`, and voila! Our extension was now only closing tabs where the domain was 'www.youtube.com'. All was well, or so I thought...

## The Devil is in the Details

Turns out, our extension was a bit of a loose cannon. It was closing tabs even if there was a YouTube video embedded in the page. That's when (after a lot of Googling) I realized I was using the `webNavigation.onCommitted` event, which fires when a navigation within the tab is committed, including the main frame navigation and sub-frame navigation. 

This was a real "aha!" moment. I needed to switch to the `tabs.onUpdated` event, which only triggers for the tab itself. This was the silver bullet. A few more tweaks to the code, and the extension was finally behaving just the way I wanted it to!

And just like that, I had built a Chrome extension that closes any tab that navigates to YouTube. It was a rollercoaster ride, with a fair share of twists and turns. But at the end of the day, I had a tool that could help me kick the YouTube scrolling addiction to the curb. It's like having a stern but loving friend who gently takes your phone away when you've had one too many. 

**manifest.json:**
```json
{
    "manifest_version": 3,
    "name": "YouTube Tab Closer",
    "version": "1.1",
    "description": "Closes any tab that navigates to YouTube",
    "permissions": ["tabs", "webNavigation"],
    "background": {
        "service_worker": "background.js"
    }
}
```

**background.js:**
```javascript
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.status === 'loading') {
    let url = new URL(tab.url);
    if(url.hostname === 'www.youtube.com') {
      chrome.tabs.remove(tabId);
    }
  }
});
```

So, the next time you find yourself spiraling down the YouTube rabbit hole, remember, there's an extension for that!
You can see on the [Chrome extension store](https://chrome.google.com/webstore/detail/youtube-tab-closer/bkmmkahjjgbmohlhefciefafnekeecoe?hl=en-GB&authuser=1) if you want just grab a copy for your Brave/Chrome browser.

---

### Interested in building your own Chrome extension or just curious about the code? Please do get in touch.
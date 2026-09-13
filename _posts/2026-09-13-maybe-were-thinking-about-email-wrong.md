---
published: true
date: 2026-09-12
title: Maybe we’re thinking about email wrong
summary: When the time to process email each takes up too many hours in the day....
categories: productivity
---
Email is getting harder to manage...

Not necessarily because we’re getting more email, although many of us are. It’s because everything around email is getting faster. More automated services, more notifications, more newsletters, more transactions, more people expecting quick responses... and now AI makes producing and sending things dramatically cheaper too, yikes! 😅 

Most approaches to email management focus on **triage**. Get to inbox zero. Read this. Archive that. Delete this. Move that. Unsubscribe. Repeat tomorrow. The problem is that triage is linear. If dealing with one email takes *t* seconds, dealing with *n* emails takes roughly *n × t* seconds. Get twice as much email and, broadly, you have twice as much work. Maybe we should think about email differently.

## Treat your inbox like a routing problem

**“How much of my email already knows where to go?”**

If 70% of the email arriving this month matches a rule that you've deliberately created, you have **70% coverage**. The remaining 30% is where your attention is useful. And instead of working through that 30% chronologically, you can find the biggest source of uncovered traffic. Perhaps `updates@example.com` accounts for 8% of everything arriving. Decide what should happen to it once, create a rule, and your coverage jumps from 70% to 78%. You haven't processed 100 emails faster. You've removed 100 emails from the problem.

## This matters as the world gets faster

The distinction becomes increasingly important as the volume of machine-generated communication increases. Triage scales with the **number of messages**. Routing scales much more closely with the **number of meaningful categories and exceptions** you have. Those are very different growth curves. If a service starts sending you ten times as many notifications, a manual workflow creates roughly ten times as much work.

A routing rule creates approximately **no additional work**. That's why increasing automation elsewhere should probably cause us to automate the *structure* of our inboxes too — rather than simply trying to become faster humans.

## So I've been playing with email coverage

I made a little Python script called **gmail-coverage** to experiment with this idea. It connects to Gmail and treats your existing filters as if they were test coverage for your inbox. It can analyse today, this week, this month, this quarter or this year and tell you what percentage of incoming mail has a sender or domain routing rule. More importantly, it finds the **highest-impact gap**. Something like:

```
Rule coverage · this month

███████████████████████████░░░░░  76.4%

✓ 981 messages covered
✗ 303 messages have no sender/domain rule

Highest-impact uncovered traffic

example-client.org     73 emails    +5.7%
github.com             61 emails    +4.8%

```

You can then create a rule for the sender or whole domain, apply one or more Gmail labels, optionally skip the inbox, and immediately move on to the next biggest opportunity. So instead of: **email → email → email,**  I'm trying for: **76% → 82% → 87% → 91% → 94%**

I want to stop managing messages and start improving the system that manages them. It may turn out that inbox zero was the wrong score all along. Maybe **coverage** is a better one.

### Trying it out

I've put the current version of `gmail_coverage.py` below. You'll need Python, a Google Cloud Desktop OAuth credential and access to the Gmail API. The script keeps its authentication and message cache locally, measures your existing routing coverage, and can help create new Gmail filters interactively.

It's an experiment rather than a polished product, but that's rather the point: I'm interested in what happens when we stop asking *“how quickly can I process my inbox?”* and start asking *“how little of my inbox should require processing at all?”*

*(Of course, when everything is sorted.. there still is work to do :facepalm:)*
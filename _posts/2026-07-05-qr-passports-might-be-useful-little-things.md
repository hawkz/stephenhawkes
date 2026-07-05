---
published: true
date: 2026-07-05
title: QR passports might be useful little things
summary: What if we don't use a giant centralised database
---
# Work in progress...

I've been playing with a small idea called a QR Passport. It is not really a passport. There is no back of an official database, no government bit, no platform account, no big infrastructure hiding behind it. It is just a way to make a small private support card, encrypt it and turn it into a QR code.

The idea is pretty simple. Someone designs a form. Someone else fills it in. They choose a passphrase. The answers get encrypted in browser and turned into a QR code. Later someone can scan QR, ask the original editor to enter a passphrase, and then they can read the encrypted content. But there is something in this pattern, I think, that is really interesting. Most access to services systems make you tell them the same stuff over and over. Sometimes it is boring stuff. Sometimes it is annoying stuff. Sometimes in the kind of projects we see in the sector it is difficult tiresome painful to explain again things: What can help when someone is overwhelmed. What not to do. Consent for things to be shared. The small bit of nuance contextual stuff that would make a service interaction go better, that lives in your head, a PDF, CRM, note, but almost never anywhere it would actually help. QR passport is a tiny wee tool for exactly this kind of stuff.

## What it does

It has three parts.
- First - the designer mode. Here you design a blank form - adding multiple choice, free text and default wording for the content to come.
- Second - the maker mode. This is the fillable, public form. You can alter the card title, wording used, fill in the free text elements, edit default fields as necessary and choose your own passphrase.
- Third - reader mode. This is used later to 'open' all of the 'stuff' above on the encrypted card. The QR code contains all of the encrypted card data. The passphrase entered during card creation is not stored. The card decryption takes place entirely in the browser. The entire site exists as a single entirely static webpage.

## Why I like it

I like tools that do not need too much machinery. This one runs as a static site. I've temporarily used GitHub Pages. No server database. No login. No admin area full of old personal data someone forgot existed. That certainly does not make it magically safe. Folks still need to use it carefully. Strong passphrases matter. HTTPS matters. Not putting unnecessary sensitive information into the the QR itself, just incase.

But there is something good about the shape of this. The information can be carried by a person. A service could read this, if given the permission. The form and what to use in this context can be adjusted. It is infrastuctural-ly boring. And Infrastructure-ly boring should be all you need to hear.

## Where it could be useful

I imagine versions for:

*   access needs at events, or in-person drop-in style places
*   Health or care preference
*   Communication passports
*   Volunteer's assistance, for example
*   Smart funder data on grantee performance and needs
*   Mutual aid setting
*   Community services that do not people want want another account

The point is not that one QR Passport should rule them all. The interesting bit is that the same pattern could work in lots of places: "design a tiny form, let someone complete it, encrypt the result, carry it as a QR code. That is the bit that I'm sure holds a solution to one of our partner's needs.

## The bit I’m interested in

Situations of over or under-building are rife in third sector organisations. We overbuild by creating platforms, portals, databases and case management systems for things that might only need a small portable artefact. We underbuild by leaving people to repeat the same information again and again because the "proper system" does not exist.

QR Passport sits somewhere in the middle. It is not a full system of record! It is not a replacement for safeguarding. It is not a replacement for a consent or 360-degree case management system, nor is it a replacement a good service design.

Instead it is more a like a bridge, rather than the whole system.. but something that could unlock more value in the system that exists. A way to move some structured information from one person to one interaction, without needing to create a new platform. 

## Where to next?

I am planning to experiment with some real templates. Not just generic ones; specific ones. A QR passport for event access, one for communication preferences and one for coping with overwhelmed feelings. Even a QR passport for a support worker handover. I want to see what issues arise. Is the QR code too dense? Is the passphrase model awkward to use? Do people understand what information is private and what is not? Does the wording make users feel in control? Does it actually help anyone avoid unnecessary repetition? That is the real test. But as a general concept, I believe there is potential here: the small form factor, encrypted card, QR code and absence of server storage. Often, effective digital infrastructure does not look like infrastructure at all.

Check it out: https://developersociety.github.io/qr-passport/

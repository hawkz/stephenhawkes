---
published: true
date: 2026-08-28
title: Tiny applications hiding in QR codes
summary: Putting a chess clock into a QR code
---
A QR code does not have to point to a website. It can contain one.

When you type a URL the `https:` part tells the browser to open a web page, browsers also understand `data:text/html` URLs, which means you can put HTML, CSS and JavaScript directly into a URL... and, if the application is small enough, that whole URL can then be encoded into a QR code.

So the QR is not really linking to the application. It is carrying it. This was something I was playing with this weekend. I tried to hold a tiny chess clock this way.

Scan the code and you get a full-screen red-versus-blue timer. Both players start with three minutes. Tap your side when you finish your turn and the other clock starts.

![image.png](/img/image.png)

There are pause and reset controls in the middle, sized to match the dots in the clock colon. The numbers scale to the screen. When one player reaches zero, a crown appears above the winner.  
Here's the URL that is inside the QR code:  
`data:text/html;charset=utf-8,%3C%21doctype%20html%3E%3Cmeta%20name%3D%22viewport%22%20content%3D%22width%3Ddevice-width%2Cinitial-scale%3D1%22%3E%3Cstyle%3E%2A%7Bbox-sizing%3Aborder-box%7Dhtml%2Cbody%7Bmargin%3A0%3Bwidth%3A100%25%3Bheight%3A100%25%3Boverflow%3Ahidden%7D%3Aroot%7B--dot%3Aclamp%2818px%2C3.2vw%2C54px%29%7Dbody%7Bdisplay%3Agrid%3Bgrid-template-columns%3A1fr%201fr%3Bposition%3Arelative%7D.clock%7Bborder%3A0%3Bcolor%3A%23fff%3Bfont-family%3Asystem-ui%2Csans-serif%3Bfont-weight%3A900%3Bcursor%3Apointer%3Bposition%3Arelative%3Bdisplay%3Aflex%3Balign-items%3Acenter%3Bjustify-content%3Acenter%3Bgap%3A3vw%7D%23r%7Bbackground%3A%23d92323%7D%23b%7Bbackground%3A%231769e0%7D.time%7Bfont-size%3A18vw%3Bline-height%3A1%3Bfont-variant-numeric%3Atabular-nums%7D.colon%7Bdisplay%3Aflex%3Bflex-direction%3Acolumn%3Bgap%3Acalc%28var%28--dot%29%2A.75%29%7D.colon%3Abefore%2C.colon%3Aafter%7Bcontent%3A%22%22%3Bdisplay%3Ablock%3Bwidth%3Avar%28--dot%29%3Bheight%3Avar%28--dot%29%3Bborder-radius%3A50%25%3Bbackground%3A%23fff%7D.off%7Bfilter%3Abrightness%28.65%29%7D.on%7Bbox-shadow%3Ainset%200%200%200%201vw%20%23ffffff44%7D.winner%3Abefore%7Bcontent%3A%22%F0%9F%91%91%22%3Bposition%3Aabsolute%3Btop%3A7%25%3Bleft%3A50%25%3Btransform%3AtranslateX%28-50%25%29%3Bfont-size%3A10vw%7D.controls%7Bposition%3Aabsolute%3Bz-index%3A10%3Bleft%3A50%25%3Btop%3A50%25%3Btransform%3Atranslate%28-50%25%2C-50%25%29%3Bdisplay%3Aflex%3Bflex-direction%3Acolumn%3Bgap%3Acalc%28var%28--dot%29%2A.7%29%7D.controls%20button%7Bwidth%3Avar%28--dot%29%3Bheight%3Avar%28--dot%29%3Bmin-width%3Avar%28--dot%29%3Bmin-height%3Avar%28--dot%29%3Bpadding%3A0%3Bborder%3A0%3Bborder-radius%3A50%25%3Bbackground%3A%23fff%3Bcolor%3A%23000%3Bdisplay%3Agrid%3Bplace-items%3Acenter%3Bcursor%3Apointer%3Bfont%3A700%20calc%28var%28--dot%29%2A.6%29%2F1%20system-ui%7D.controls%20span%7Btransform%3Ascale%28.7%29%7D%3C%2Fstyle%3E%3Cbutton%20class%3D%22clock%22%20id%3D%22r%22%3E%3Cspan%20class%3D%22time%20mins%22%3E3%3C%2Fspan%3E%3Cspan%20class%3D%22colon%22%3E%3C%2Fspan%3E%3Cspan%20class%3D%22time%20secs%22%3E00%3C%2Fspan%3E%3C%2Fbutton%3E%3Cbutton%20class%3D%22clock%22%20id%3D%22b%22%3E%3Cspan%20class%3D%22time%20mins%22%3E3%3C%2Fspan%3E%3Cspan%20class%3D%22colon%22%3E%3C%2Fspan%3E%3Cspan%20class%3D%22time%20secs%22%3E00%3C%2Fspan%3E%3C%2Fbutton%3E%3Cdiv%20class%3D%22controls%22%3E%3Cbutton%20id%3D%22pause%22%20aria-label%3D%22Pause%22%3E%3Cspan%3E%E2%85%A1%3C%2Fspan%3E%3C%2Fbutton%3E%3Cbutton%20id%3D%22reset%22%20aria-label%3D%22Reset%22%3E%3Cspan%3E%E2%86%BB%3C%2Fspan%3E%3C%2Fbutton%3E%3C%2Fdiv%3E%3Cscript%3Elet%20t%3D%5B180000%2C180000%5D%2Cactive%3D-1%2Clast%3Dperformance.now%28%29%2Cpaused%3Dfalse%2Cclocks%3D%5Bdocument.getElementById%28%22r%22%29%2Cdocument.getElementById%28%22b%22%29%5D%3Bfunction%20draw%28%29%7Bclocks.forEach%28%28clock%2Ci%29%3D%3E%7Blet%20s%3DMath.ceil%28Math.max%280%2Ct%5Bi%5D%29%2F1000%29%3Bclock.querySelector%28%22.mins%22%29.textContent%3DMath.floor%28s%2F60%29%3Bclock.querySelector%28%22.secs%22%29.textContent%3DString%28s%2560%29.padStart%282%2C%220%22%29%3Bclock.className%3D%22clock%20%22%2B%28active%3D%3D%3Di%26%26%21paused%3F%22on%22%3A%22off%22%29%2B%28t%5B1-i%5D%3D%3D%3D0%3F%22%20winner%22%3A%22%22%29%7D%29%3Bdocument.querySelector%28%22%23pause%20span%22%29.textContent%3Dpaused%3F%22%E2%96%B6%22%3A%22%E2%85%A1%22%7Dfunction%20tick%28now%29%7Bif%28active%3E%3D0%26%26%21paused%29%7Bt%5Bactive%5D-%3Dnow-last%3Bif%28t%5Bactive%5D%3C%3D0%29%7Bt%5Bactive%5D%3D0%3Bactive%3D-1%7D%7Dlast%3Dnow%3Bdraw%28%29%3BrequestAnimationFrame%28tick%29%7Dclocks.forEach%28%28clock%2Ci%29%3D%3E%7Bclock.onclick%3D%28%29%3D%3E%7Bif%28t%5B0%5D%26%26t%5B1%5D%29%7Bactive%3D1-i%3Bpaused%3Dfalse%3Blast%3Dperformance.now%28%29%3Bdraw%28%29%7D%7D%7D%29%3Bdocument.getElementById%28%22pause%22%29.onclick%3De%3D%3E%7Be.stopPropagation%28%29%3Bif%28active%3E%3D0%29%7Bpaused%3D%21paused%3Blast%3Dperformance.now%28%29%3Bdraw%28%29%7D%7D%3Bdocument.getElementById%28%22reset%22%29.onclick%3De%3D%3E%7Be.stopPropagation%28%29%3Bt%3D%5B180000%2C180000%5D%3Bactive%3D-1%3Bpaused%3Dfalse%3Blast%3Dperformance.now%28%29%3Bdraw%28%29%7D%3Bdraw%28%29%3BrequestAnimationFrame%28tick%29%3C%2Fscript%3E`

That is the whole application:

- No hosting.
- No domain.
- No database.
- No account.
- No app store.

Just a lump of HTML, CSS and JavaScript inside a URL, inside a QR code.

## Little useful things

This feels related to the idea behind [QR Passports](https://stephenhawkes.com/2026/07/05/qr-passports-might-be-useful-little-things/): QR codes as small pieces of useful infrastructure, rather than merely shortcuts to webpages. There are lots of tiny problems that probably do not need a service behind them: A reference card with a bit of interaction. Something useful enough to be software, but too small to deserve a platform. You could print it on a card, stick it on a wall, put it in a handbook, or keep it in a wallet.

*There are a ton of obvious limits.* QR capacity is finite. Dense codes get harder to scan. There is no server, no shared state and no automatic update mechanism. But those constraints are quite appealing.

Sometimes the infrastructure needed to solve a problem really can be a square of ink on paper.
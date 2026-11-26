# Retrospective: to the person I was in Week 1

You started this track wanting to do the least work possible. Your Week 1 workflow audit said it plainly: you used AI as a faster search box, and you wanted the internship tasks out of the way so you could get back to "real" projects. You thought a portfolio was a template with your name on it, and that the AI Fluency track was paperwork next to the ML work.

## What you set out to do

Get through the track, end up with a personal site, and keep the Machine Learning track as the thing that counts.

## What actually changed

**The site stopped being a template.** In Week 2 you rejected every bio the model wrote, because each one turned you into "a developer who integrates AI". You said: I'm a software engineer. That one sentence became the voice card (straightforward, honest, no filler), the identity kit, and finally the claim on the first screen of h0pi.github.io: "I build software you can check, not just trust." You didn't get there by prompting harder. You got there by saying no to drafts until they sounded like you.

**Other people saw what you couldn't.** You thought the site was finished after Week 5. In Week 6 a friend opened it on their phone and said, within ten seconds, "I can't see what you do, I have to scroll" and "the projects look jumbled on the phone". Both were true and both were invisible to you on a desktop. The Week 7 break-it pass found more: the page went completely blank without JavaScript, a shared link had no preview, the photos were larger than they are ever shown, and Google didn't list the site at all. Earlier, in Week 4, a single wrong flag (`--base-href` mangled by Git Bash into a Windows path) had shipped a blank page, and it took a long look to understand why.

**You stopped doing everything by hand.** By Week 5 you had an agent: a Claude Code skill that reads your internship portal (read-only) and your GitHub repo every week and tells you what is done, what is open and what to do next. Its first version let the model count notebook cells, and it miscounted placeholder cells as problems. Version 2 moved the counting into a short Python script and left the model only the judgement. On its first v2 run it found a real problem nobody had noticed: two unused notebooks that were making the repo's CI fail.

**You started writing the limitation first.** The demo video says on screen that one of the five safety tests was never run live. The site's fix log lists what is still broken. That used to feel like admitting failure. Now it reads like the most credible part of the work.

## Where AI did the work, honestly

Most of the building was done by Claude (Claude Code, and the browser extension for the portal) at my direction. My part was deciding what to build and what it must never do, rejecting what didn't sound like me, and checking results against reality. That is the skill this track actually taught, and it is different from "using AI".

## What I'd build next

The FlyRank ML capstone as a real case on the site (which content pages will lose search visibility next, 74k real pages, honest validation), and a scheduled version of the weekly-review agent that runs without my browser open.

## The three most transferable things

1. **Check it like a stranger, on their device.** Ten seconds on someone else's phone found more than hours on my own screen. Every project now gets a "what do you see first?" test and a "try to break it" pass before I call it done.
2. **Exact work goes to code, judgement goes to the model.** Counting, parsing and checking belong in a small script with a fixed rule; the model reads the result and explains it. It made the agent reliable and cheap to test.
3. **Name the limitation before someone else does.** A list of what is not tested, not fixed, or not proven turns "is this real?" into "I can see exactly how far this goes". It is the reason reviewers can trust the parts that do work.

If you, in Week 1, had to keep one thing from this: the work isn't done when it runs on your machine. It's done when a stranger can see what it is in ten seconds, and you can say exactly where it stops working.

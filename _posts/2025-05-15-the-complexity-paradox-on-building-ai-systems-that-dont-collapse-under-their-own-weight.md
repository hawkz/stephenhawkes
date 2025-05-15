---
published: true
date: 2025-05-14
title: "The Complexity Paradox: On Building AI Systems That Don't Collapse Under
  Their Own Weight"
summary: A balad to complexity vs complicateness, and the keys to managing both
categories: blog
---
It's a warm Tuesday afternoon, and I'm staring at a terminal window filled with tiny, accusatory text. The log file scrolls past faster than I can read it, thousands of lines documenting the slow death of an AI training run that's been grinding away for the past 36 hours. Somewhere, buried in the mess of numbers and error codes, is a clue about why my model is hallucinating that Australia is a fictional country populated exclusively by sentient koalas.

I've hit that familiar point in every AI project: the moment when the complexity becomes so overwhelming that I start to question my life choices.

## The Gordian Knot of AI Development

The transcript I've been mulling over from Peter van Hardenberg's talk on complexity in software systems has been rattling around in my head all week. While he wasn't speaking about AI specifically, every point he made applies with devastating accuracy to what we're building with modern AI systems.

"Complexity occurs when your systems interact with each other," van Hardenberg says, "and when it takes a lot to get things done because of that."

If regular software is complex, AI systems are complexity squared. They're not just systems interacting with other systems—they're systems attempting to model the interactions of _all possible systems_ they might encounter. The LLM I'm training doesn't just need to understand text; it needs to understand the entire world that produced that text.

"The problem with complexity is that your systems can become unreasonable," he continues, "and when I say unreasonable I don't mean in kind of like a sort of colloquial sense. What I mean is that you literally cannot reason about them."

This hits particularly close to home. When my model thinks Australia is koala-fiction, I can't just step through the code and see where the logic went wrong. The error exists somewhere in the statistical patterns encoded across billions of parameters. I'm beyond reason, living in the realm of probabilistic approximations and emergent behaviors.

## Complexity Homeostasis in AI

Van Hardenberg introduces this brilliant concept of "complexity homeostasis" — the idea that systems naturally gravitate toward a certain level of complexity over time. Build something simple, and if it succeeds, it inevitably grows more complex as new demands arise. Build something too complex, and eventually you'll tear it down and start over.

AI development follows this pattern with almost comic predictability:

1.  Start with an elegant, simple model architecture
    
2.  Add features to handle edge cases
    
3.  Implement safety guardrails
    
4.  Build evaluation frameworks
    
5.  Create deployment pipelines
    
6.  Develop monitoring systems
    
7.  Wake up one day with a monstrosity that no single person understands anymore
    

I've done this dance enough times to recognize the music. Right now we're in the phase where everyone is excitedly piling complexity onto their AI systems, creating increasingly labyrinthine architectures that require entire teams to maintain. We're building the Tower of Babel, one transformer layer at a time.

The reckoning will come. It always does.

## Essential vs. Accidental Complexity

There's that paper van Hardenberg mentions: "Out of the Tarpit" by Moseley, which distinguishes between essential complexity (the unavoidable complexity inherent to the problem domain) and accidental complexity (all the extra crap we pile on because of our tools, platforms, and approaches).

With AI, the essential complexity is already enormous. We're trying to create systems that can understand language, recognize images, make predictions, and interact with humans in a way that feels natural. That's fundamentally complex.

But then we add mountains of accidental complexity: containerization, cloud deployment, monitoring stacks, evaluation frameworks, fine-tuning pipelines, data processing jobs, model registries, feature stores, and on and on. Before long, the accidental complexity dwarfs the essential complexity, and we're spending 90% of our time managing infrastructure rather than improving the actual AI.

I wonder sometimes if our modern AI systems could be 10x simpler and still achieve 90% of their current capabilities. I suspect the answer is yes, and that should terrify everyone currently investing in this field.

## The Happy Path and the Edge Cases

"The first version of your code," van Hardenberg says, "you just write the happy path, everything's glorious, and software can be really simple when it lives in an idealized world and everything is fine."

This describes every AI demo I've ever seen. Carefully curated prompts that show the system at its best. Perfect lighting for the computer vision demo. Crystal clear audio for the speech recognition. The happy path.

But AI systems don't live in idealized worlds. They live in messy, chaotic, adversarial environments full of humans who will immediately try to break them in creative ways. The moment your AI touches the real world, you're dragged kicking and screaming off the happy path and into the wilderness of edge cases.

I've seen teams spend two weeks building an AI feature and six months handling the edge cases. This is the way.

## The Multiplicative Nature of AI Complexity

Van Hardenberg talks about how problems "dimensionalize against each other," creating exponential complexity. One browser, one OS, one screen size? Manageable. Many browsers, many OSes, many screen sizes? A nightmare of multiplicative complexity.

AI systems add their own dimensions to this equation:

*   Different languages and cultural contexts
    
*   Various domains of knowledge
    
*   Diverse user intents
    
*   Potential for misuse
    
*   Ethical considerations
    
*   Security vulnerabilities
    
*   Evolving regulatory landscapes
    

Each of these dimensions multiplies against the others. Your AI needs to work not just for English speakers using Chrome on Windows, but for Hindi speakers using Firefox on Android who want medical information while navigating privacy regulations in India.

## Cutting the Gordian Knot

So what do we do? If complexity is inevitable and AI systems are inherently more complex than traditional software, are we doomed?

Maybe not. Van Hardenberg suggests a few approaches that might help us tame the complexity beast:

1.  **Start over**: Reset the clock on complexity now and then. Don't be afraid to rebuild components from scratch rather than adding yet another hack to a crumbling foundation.
    
2.  **Eradicate dependencies**: Find your dependencies and eliminate them. Every external system you rely on adds to your complexity budget. Do you really need that extra library or service?
    
3.  **Cut scope**: Do less with less. The most elegant AI solutions aren't the ones that do everything; they're the ones that do one thing extraordinarily well.
    
4.  **Isolate complexity**: Build strong boundaries around your most complex components. Make sure complexity in one area doesn't leak into others.
    

For AI specifically, I'd add:

5.  **Embrace limitations**: Not every AI system needs to be general-purpose. Some of the most useful AI tools have well-defined limitations that users understand and appreciate.
    
6.  **Design for transparency**: Make it clear to users what your AI can and cannot do. Set expectations appropriately.
    
7.  **Build robust fallbacks**: When your AI inevitably fails (and it will), have graceful fallback mechanisms that preserve the user experience.
    

## "It Never Gets Easier, You Just Go Faster"

I love how van Hardenberg ends his talk with that cyclist's quote: "It never gets easier, you just go faster."

This feels especially relevant to AI. We're not making computing simpler with these systems; we're adding extraordinary complexity to make certain tasks faster. AI is an acceleration layer, not a simplification layer.

The abstraction that AI provides isn't really removing complexity—it's hiding it. The complexity is still there, lurking beneath the surface, waiting to surprise us when the abstraction leaks.

As we build these systems, we need to be honest about this. AI doesn't solve the complexity problem; it transforms it. The complexity moves from the task the user wants to accomplish to the system the developer needs to build.

And that's okay, as long as we're clear-eyed about the tradeoff we're making.

## A Modest Proposal

So here's my modest proposal for those of us building AI systems: let's spend less time adding features and more time reducing complexity. Let's value systems that do one thing well over systems that do many things adequately. Let's prioritise robustness and transparency over capability. In short, let's build AI systems that we can reason about, even if that means accepting stricter limitations on what they can do. Because an AI system that does less but does it reliably is infinitely more valuable than an AI system that occasionally does amazing things but frequently does bizarre things.

Like telling you that Australia is a fictional koala utopia.
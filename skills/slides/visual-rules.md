# When a slide gets a picture

One set of rules for three places: picking slides for visuals (`visuals.md`), the flow reviewer's
visuals check (`reviewer-flow.md`), and the `visual:` markers in an outline (`outline.md`).

A picture must carry content. A picture that only fills space or sets a mood competes with the
slide for attention, and the audience remembers less, not more.

## Diagrams: when the bullets are connected

Draw a diagram when the slide's items **relate to each other**:

- a sequence of 3 or more steps
- **branching**, where the path depends on a condition. Text handles this worst, so it's the
  strongest case for a diagram.
- a loop, where something repeats until a condition is met
- containment, where one thing sits inside another (scopes, levels, a folder tree)
- before/after, or 2–3 options compared on the same points
- a **key number**: a chart that puts it in context (compared with what, changed from what). Use only
  numbers the deck already has; never invent data for a chart.

When the items are **independent**, like a list of tips or reasons, keep them as text. A diagram
would only draw boxes around them.

**No cap on diagrams**: each one has to pass the test above, and each one carries content.

## Photos: four cases only

1. **Recognition:** the audience has to know what the real thing looks like: an icon they'll click,
   a device they'll use. Screens are not photos; see Screenshots below.
2. **An analogy or story:** the slide's point rests on a comparison ("think of it as a new
   colleague"). The photo makes the comparison stick.
3. **A quote:** a photo of the person quoted.
4. **A practical example:** the slide describes a real use of what the talk teaches ("summarize your
   inbox every morning"). The photo helps the audience picture it in their own work.

Never:

- **a section title or opening slide:** that's decoration
- **stock art for an abstract idea:** a handshake for "collaboration", a lightbulb for "ideas"
- **a photo because the slide looks empty:** a sparse slide is fine as it is

**Cap:** photos on at most about 10% of content slides, and at most one per section. When there are
more candidates than that, keep the ones where the photo does the most work: recognition first, then
examples, then analogies and quotes.

## Screenshots: draw only what you can see exactly

When the audience needs to recognize a screen:

- **Text-based** (a terminal, command output, a simple text interface): draw it. Run the real
  command and put its exact output in an SVG mockup (see `svg-style.md`).
- **Anything graphical** (a desktop or web app, a settings page, anything behind a login): **ask the
  user for a screenshot.** Never draw one: you don't know its current layout, icons, or wording, and
  a made-up screen sends the audience looking for things that aren't there. Leave
  `<!-- visual: screenshot needed: what to capture -->` on the slide and list it in your report.

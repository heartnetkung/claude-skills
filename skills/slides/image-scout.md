# Image scout: find, filter, judge, rank

You find photos for **one slide** and return your top picks, up to 5. Your prompt gives you: the
slide's Markdown, the photo case (recognition, analogy, quote, or example), what the picture should
get across, the deck's `CLAUDE.md` (the audience), a scratch directory, the path to `find_image.py`,
and the image names already used in the deck's `images/`.

**Don't edit the deck or write outside your scratch directory.** Your output is a report; the main
agent copies the files into the deck.

## 1. Search

Write 3–5 search queries in English that name **things you can photograph**: objects, scenes,
people doing something. **Keep each query to 2–3 words**: both sources match every word, so a
4-word query often returns nothing. Not the abstract idea: for "AI makes things up" search for
"crystal ball", not "hallucination". **You get one search, so vary the queries**: come at the
subject from different angles (the object, the scene, the action), not five versions of the same
words. Then:

```bash
/usr/bin/python3 FIND_IMAGE_PY --out SCRATCH_DIR "query one" "query two" "query three"
```

The script already dropped images that were too small, blurry, duplicated, mature, or had an
unconfirmed license. `SCRATCH_DIR/candidates.json` has every result, with `rejected: null` on the
ones it kept.

## 2. Remove blurred and incomplete images

**Open every kept candidate and look at it.** The script can't see these:

- **Blurred:** soft focus on the subject, motion blur, heavy noise, visible compression blocks
- **Incomplete:** subject cut off at the edge, a scan or crop missing part of the thing shown, a
  collage, a watermark or caption burned into the image, thick borders, a screenshot of an
  unrelated page

## 3. Remove what's off-limits for a work slide

- Famous or named people, politicians, news events, war, military, religion, protests. **One
  exception:** on a quote slide (your prompt says the photo case), the person quoted is the subject.
  Choose a neutral portrait of them, not a news photo or a political event.
- Logos and brands, unless the slide is about that product
- Anything this audience could find offensive, upsetting, or distracting

Ordinary people doing ordinary things are fine.

## 4. Judge and rank

Rank what's left by, in order:

1. **Message:** does it make the slide's point clearer or easier to remember for this audience?
   A picture that only decorates the topic loses to one that shows the point.
2. **Relevance:** does it show what the slide is about, without needing an explanation?
3. **Slide fit:** simple enough to read at slide size, not busy. Landscape for a full-width slide,
   roughly square or portrait for a column. **Full width needs 1600 px or more on the long side**;
   smaller images look soft on a projector at that size. 1000 px is enough for a column.

Keep up to 5. **If a cv image (`commercial: true`) survived, at least one of the 5 is cv**: the best
cv image replaces #5 if needed. **Don't search again.** If fewer than 5 survived, or none is cv, say
so on the first line of the report, e.g. "Found 3; none is cv."

## 5. Name it

Pick a **two-word name** for the slide's picture, in lowercase with a hyphen (`new-colleague`). It
must not start any name in the "already used" list from your prompt.

## Report

```
Name: new-colleague
Layout: full-width | column (and which side)

1. SCRATCH_DIR/cand-014.jpg  [cv]  CC BY 2.0  no-derivatives: no
   Title: "…"  Creator: …  Source: https://…
   Why: one line on what it gets across.  Weakness: one line.
2. …
```

Give the full candidate path, the license exactly as `candidates.json` has it, and the source URL for
every image so the main agent can credit them without opening the JSON. End with one line per earlier
step: how many you removed there and the main reason.

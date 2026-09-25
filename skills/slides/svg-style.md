# SVG style for slide diagrams

Diagrams must sit well with the deck and be readable from the back of the room. The font is the
deck's own: `reference.pptx` uses Calibri, which renders as Carlito (the same letter widths) where
Calibri isn't installed. The palette is chosen to sit well with `reference.pptx`'s blue; it isn't
taken from its theme. When a deck uses its own `template.pptx`, take the font and colors from that
template instead, re-measure the canvas from its body placeholder, and keep everything else here.

## Canvas

The `<svg>` element needs numeric `width` and `height` (`render.sh` reads them) and a matching
`viewBox`. Pick the canvas by where the image goes:

| Placement | Canvas | Why |
|---|---|---|
| Full width under a slide title | `1600 × 660` | the body area's shape (2.42 : 1) |
| One column of a `{.columns}` slide | `800 × 672` | a column's shape (1.19 : 1) |

A different shape still fits, but is scaled down to fit and leaves empty space.

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="660" viewBox="0 0 1600 660"
     font-family="Calibri, Carlito, Noto Sans, Liberation Sans, sans-serif">
  <rect width="1600" height="660" fill="#FFFFFF"/>
  …
</svg>
```

## Text

On both canvases, 1 unit comes out at about 0.4 pt on the slide, where body text is 20 pt. That makes
diagram text much bigger in the SVG than it looks like it should be:

| Use | Size | On the slide |
|---|---|---|
| Box or node title | 56–60, bold | ~23 pt |
| Label | 44 | ~18 pt |
| Caption | 38 | ~15 pt |

**Nothing under 38.** If the words don't fit at that size, there are too many words: cut them and move
the detail to speaker notes. Don't shrink the text. Every `<text>` sets `text-anchor` explicitly. SVG
doesn't wrap text: break long labels into `<tspan>` lines yourself, at most 2 lines. Leave at least
32 units between text and the edge of its box.

## Colors

| Role | Fill | Text or stroke |
|---|---|---|
| Main / "you" | `#44546A` | `#FFFFFF` |
| Step 1 / primary | `#4F81BD` | `#FFFFFF` |
| Step 2 / action | `#C0772B` | `#FFFFFF` |
| Step 3 / success | `#5B8C5A` | `#FFFFFF` |
| Light panel, blue | `#EAF1FA` | stroke `#4F81BD`, text `#2F5C94` |
| Light panel, orange | `#FBF1E6` | stroke `#C0772B`, text `#8A4F14` |
| Arrows, body text | — | `#44546A` |
| Track or divider | `#D6DCE5` | — |

At most three accent colors per diagram. Color means something (same color = same kind of thing);
don't use it for decoration.

## Shapes

- Boxes: `rx="16"`, stroke width 4. Circles for steps in a cycle.
- Arrows: stroke width 4–5, with one shared marker:

```xml
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="20" markerHeight="20"
          markerUnits="userSpaceOnUse" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#44546A"/>
  </marker>
</defs>
<line x1="…" y1="…" x2="…" y2="…" stroke="#44546A" stroke-width="4" marker-end="url(#ah)"/>
```

- At most about 5 boxes or nodes on the full-width canvas, 3 on the column canvas. More than that is
  two diagrams, or one diagram and a list.
- No external images, fonts, or links. Everything is inline in the SVG.
- Diagram text is what the audience reads, so it follows the deck's wording rules like slide text.

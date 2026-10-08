# Reviewer 2 — design quality

**Read `design-philosophy.md`, in this same directory, first.** Then judge the design against it:
deep modules, information hiding, complexity as something that accumulates one small decision at
a time.

**Review every name that is used outside the place it is declared** — API fields, DB columns
and enum values, class names, public functions. Skip locals and private helpers: those are read
beside their definition and cost nothing to rename.

Read each name alone, as it appears in a query, a payload or a call site, with its table, class
and module stripped away. It fails if you cannot say what it holds:

- **One word.** `position`, `content`, `name`, `version` rely on the table beside them. Add the
  word that table was supplying: `deck_order`, `deck_content`, `file_name`.
- **Does not say what kind of data it holds.** A boolean starts with `is_` or `has_`: `common`
  → `is_common`. An id ends in `_id` and names the row it points to: `related_slide` →
  `related_slide_id`, and `template_version` holding a `template_specs` row id →
  `template_spec_id`. A time ends in `_at` or `_date`: `created` →
  `created_at`.

Report each as name → what it holds → proposed name.

Two names that differ must denote different things: if you cannot say what separates them, one
of them should not exist.

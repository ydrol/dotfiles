---
name: reference-caching
version: 1.0.0
description: >
  Cache a project's expensive-to-fetch source documents locally under ./resources as Markdown, with
  front matter linking back to the origin so staleness can be detected, and a README.md index. Use
  whenever a project depends on documents that need fetching or conversion — Google Drive .docx/.doc/
  .pdf/.xlsx, Google native docs, SharePoint or Confluence exports — and whenever asked to cache,
  mirror, refresh or re-fetch such sources, or to check whether a cached copy has gone stale.
---

# Reference Caching mechanism

When a project depends on expensive-to-fetch source documents (Google Drive `.docx`/`.doc`/`.pdf`/
`.xlsx`, Google native docs, or other files that need conversion), cache them locally under
`./resources`, mirroring the source's relative path, as Markdown.

## The rules

- Convert each source to Markdown (e.g. Drive `read_file_content` → `.md`), preserving the folder
  structure of the origin under `./resources`.
- Prepend YAML front matter linking back to the origin so staleness can be detected: `source_id`,
  `source_url`, `source_mime`, `source_modified` (the origin's last-modified timestamp at cache
  time), and `cached_utc`.
- **Staleness check / refresh:** compare the live source's modified time against front-matter
  `source_modified`; if the source is newer, re-fetch and overwrite.
- Keep a `./resources/README.md` index listing every cached file, its type, and a link to the
  origin. Index (but don't convert) already-machine-readable or very large raw files — pull those on
  demand instead of caching multi-MB blobs.

## Front matter shape

```yaml
---
source_id: 1a2B3cD4eF5gH6iJ7kL8mN9oP
source_url: https://docs.google.com/document/d/1a2B3cD4eF5gH6iJ7kL8mN9oP/edit
source_mime: application/vnd.google-apps.document
source_modified: 2026-09-14T09:31:22Z
cached_utc: 2026-09-16T11:02:45Z
---
```

`source_modified` is the origin's timestamp, not the fetch time — the two are different facts and
the staleness check needs the first one.

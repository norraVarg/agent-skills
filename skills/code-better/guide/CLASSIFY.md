# Classify

This file is a reference used by `PROCEDURE.md`: how to classify a file, and how the
guide's layers relate to each other. It does not run on its own.

## Two kinds of rule

- **Safety rules** protect correctness, security, and testability: error handling,
  validation, secrets, injection, data integrity, tests. Phrased with *never*, *always*,
  *must*, *every*. They hold everywhere.
- **Style rules** shape how code looks and is organised: naming, layout, idiom choice,
  file structure, comments. Phrased with *prefer*, *avoid*, *keep*.

A project's existing conventions can outweigh a style rule: matching what the
surrounding code already does is often more valuable than enforcing this guide's
preference. Nothing outweighs a safety rule.

A rule may also describe workflow or conversational behaviour rather than the content
of the code itself — something no diff can show, such as whether a developer already
gave a go-ahead before a file was written. Such a rule has nothing for a review to
check; it produces no finding, regardless of precedence.

## Precedence

For safety rules, existing conventions never apply — they cannot override a safety
rule, so they are not part of this chain:

    rules/user-rules.md  >  universal/  >  domains/  >  languages/

For style rules, existing conventions outrank the guide's own preference, but not the
developer's explicit instruction:

    rules/user-rules.md  >  the project's existing conventions  >  universal/  >  domains/  >  languages/

Higher wins on conflict; lower adds detail. Within one layer, a safety rule wins over a
style rule.

## Classify

Do this once per file under review; a diff can span several files needing different
combinations of layers.

**Language** — from the file's extension; manifests only confirm.

| Signal | Language file |
| --- | --- |
| `.ts` `.tsx` `.mts` `.cts` `.d.ts` `.js` `.jsx` `.mjs` `.cjs`; script blocks in `.vue` `.svelte` `.astro`; `package.json`, `tsconfig.json` | `languages/typescript-javascript.md` |
| Configuration and data: `.json` `.yml` `.yaml` `.toml` `.ini` `.env*`, `Dockerfile`, `.sh`, `.sql`, CI workflows | none — universal layer only; say nothing |
| Any other programming language | none — say so in one line, once per review, and offer to add it from `languages/_TEMPLATE.md` |

**Domain** — from the dependencies of the nearest `package.json` (or equivalent) and
the file's location and content.

| Signal | Domain file |
| --- | --- |
| Frontend: `react`, `vue`, `svelte`, `angular`, `solid`, `preact`, `vite` as a dependency; `"jsx"` in tsconfig; `index.html`; `components/` or `pages/` folders | `domains/frontend.md` |
| Backend: `express`, `fastify`, `@nestjs/*`, `hono`, `koa` as a dependency; a database library (`prisma`, `typeorm`, `drizzle`, `knex`, `sequelize`, `mongoose`, `pg`, `mysql2`, `mongodb`); a cloud SDK; `Dockerfile`, `serverless.yml`; folders named `routes/`, `handlers/`, `controllers/`, `api/`, `jobs/` | `domains/backend.md` |
| Full-stack framework: `next`, `nuxt`, `remix`, `@sveltejs/kit`, `astro` as a dependency | per file — server-only code (route handlers, API routes, server actions, loaders, middleware) → `backend.md`; components and client code → `frontend.md`; a file with both → both |
| Frontend and backend signals in separate packages (monorepo) | the package containing the file decides |
| Both signals in one package without a full-stack framework | by the file: runs in a browser → `frontend.md`; runs on a server → `backend.md` |
| No domain signal (library, CLI, shared package, tooling) | none — universal and language layers only; say nothing |
| Infrastructure as code (CDK, Terraform, CloudFormation, Pulumi) | none yet — universal and language layers only |

Framework-specific rules, where needed, live in the domain file under a heading named
after the framework.

## Adding a language or domain

Copy the `_TEMPLATE.md` in the relevant folder, fill it in, and add one row to the
matching table above. Nothing else changes.

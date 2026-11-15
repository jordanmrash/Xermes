# Security

## Security boundary

This repository publishes patterns, formats, a sanitized lessons corpus, and an
adoption record. The following are **intentionally excluded** and must never be
committed here, in a fork's PR, or in an issue:

- Secrets, credentials, tokens, API keys, or private connection settings.
- Browser state, session transcripts, chat history, or anything that identifies
  a person beyond the author's public professional identity.
- Machine-specific paths, hostnames, tunnel endpoints, or device identifiers.
- Production databases, operation logs, or live agent manifests.
- Private workspace corpora (the full 120-entry source corpus; the published
  lessons file contains only host-agnostic, sanitized entries).

Machine-specific state is *intentionally* absent, the same way the
agent-construct schema excludes it by design. If any of the above ever appears
in a published tree, treat it as an incident: remove the value in a follow-up
commit and rotate the exposed credential — a commit does not unpublish what an
earlier commit revealed.

## Why the lessons corpus is safe to publish

1. The 45 seeded entries come from `agent-of-record`, which is already public.
2. The entries added afterwards (Hermes-host lessons) describe agent behavior,
   not user data: tool traps, verifier design mistakes, and protocol failures.
3. Before any batch of entries is added, the file is scanned for personal data
   (names, addresses, accounts, credentials, machine identifiers) — the same
   `public_scan` discipline used in agent-of-record.

## Reporting

Please do not open a public issue for a security problem. Use GitHub's private
vulnerability reporting on this repository, or contact the author through the
profile linked from the repository. Expect an acknowledgement within a few
days; this is a personal project with no on-call rota.

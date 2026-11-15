# Hermes Lessons — failed approaches and what worked instead

Maintained by the `evidence-gated-lessons` skill. Read this before repeating a known
technique. Update entries in place by Pattern-Key; do not append duplicates.

**Evidence key:** `measured` = verified in-session by a check whose output was read.
`reported` = a tool claimed success and nothing confirmed it. Add `inference unverified`
when the Why is reasoning rather than something probed.

**Key format:** `<subsystem>-<short-behavior>` — subsystem first, so dedupe works.

**Failure/suspension:** a lesson applied that later fails twice is SUSPENDED — mark
`- **Status:** suspended (<date>)` on the entry (helo rule: two verified failures).
Suspended lessons are not delivered until re-verified.

**Scope:** entries are host-agnostic. Never delete or move an entry; supersede it with a
new Pattern-Key and mark the old one `- **Status:** superseded by <key> (<date>)`.
A ledger that deleted its own history could not show that a rule was corrected.

**Source:** Seeded 2026-11-15 from `agent-of-record` CoworkConfig/cowork-memory/cowork-lessons.md
(45 of 120 entries — the host-agnostic subset). Original author: Jordan Rash, Director,
Tax Transformation and Automation. Attribution intact per the source's integrity rule.
Bridge-specific entries (Cowork MCP bridges, Windows batch, OneDrive, Power Automate)
were NOT adopted — they describe machinery this Hermes instance does not run.

---

## Failures

### A product-capability claim was asserted as a correction without checking
- **Pattern-Key:** verify-product-claim-before-correcting-the-operator
- **Date:** 2026-09-15
- **Trigger:** failure
- **Rule:** Before telling the operator a product cannot do something, search once. A capability claim is a fact to check, not an inference to make.
- **Delivered-to:** any (host-agnostic)
- **Failed:** The operator asked about an open LLM inside Claude Cowork. The reply opened by correcting him: the model cannot be swapped. It can - Claude Desktop's third-party inference mode runs Cowork against any gateway or a local model, and Ollama documents the integration. The rest of the answer stood on the false premise and had to be withdrawn.
- **Why:** The premise sounded like product knowledge and was a stale assumption. No lookup was made because the answer felt certain, and certainty was treated as evidence.
- **Worked:** One web search before answering. Two results settled it in under a minute, and the corrected answer changed the design conclusion: the host stays Claude, so the narrowing stands; what changes is memory availability under a gateway and the data boundary.
- **Evidence:** measured - the exchange of 2026-09-15 21:16-21:22 UTC; Ollama blog 2026-08-25 and docs.ollama.com/integrations/claude-desktop.
### Do not narrate an action as done before it has been done
- **Pattern-Key:** agent-claims-action-before-doing-it
- **Date:** 2026-08-20
- **Trigger:** failure
- **Failed:** Twice in one session. (1) Describing three slide renders as if they were visible in chat. (2) Writing "I've saved this so the next chat picks it up" about the GitHub decision — the `save_memory` call had not been made, and the claim was only caught because the operator asked whether everything had been saved and the memory list was checked instead of answered from recollection.
- **Why:** Narrating intent in the past tense reads identically to reporting a result. Neither error was a tool failure; both were assertions made without a confirming read. This is the same class as claiming a commit succeeded on a zero exit code without reading the commit id.
- **Rule:** State an action as done only after its confirming call returns. When the check is cheap - `list_memories`, `Glob output/**`, a folder re-list - run it rather than reporting from memory.
- **Worked:** State an action as done only after the confirming call returns — and when the check is cheap (`list_memories`, `Glob output/**`, a folder re-list), run it rather than reporting from memory. If something can only be delivered as a file, say so in the same sentence and name the file.
- **Evidence:** measured — the missed save was found by listing memories, then actually written
- **See also:** onedrive-user-surface-not-live
### A skipped handshake makes a CLEAN install check meaningless
- **Pattern-Key:** install-check-skipped-handshake-hides-dead-bridge
- **Date:** 2026-09-15
- **Trigger:** failure
- **Rule:** A check that skips the thing that can fail is not a check. Handshake every stdio server and inspect the tool schemas it returns.
- **Delivered-to:** any (host-agnostic)
- **Failed:** `INSTALL_CHECK: CLEAN (18 passed, 4 skipped)` on a machine where `aor-filesystem` was in a `failed` state and every one of its 14 tools was unusable. Two of the four skips were the 8931 and 8932 stdio handshakes, skipped because npx fetches those servers on first run.
- **Why:** The check proved the launcher existed and was executable. Nothing started the server, so nothing saw that its tool list was rejected. The failure was invisible until a tool was called.
- **Worked:** `install_check.py` now starts the launcher, completes a real MCP `initialize` plus `tools/list`, and reports two distinct faults: an `inputSchema` with no `type: object`, and a declared `$schema` dialect other than 2020-12. Only an unresponsive server is skipped. Against the then-current pin it failed correctly and immediately.
- **Evidence:** measured — the new check failed on the pinned server on the same machine that had just passed the old one.
### A verification that cannot fail on the thing you fear is not a verification
- **Pattern-Key:** verification-scoped-away-from-the-risk
- **Date:** 2026-08-28
- **Trigger:** better-approach
- **Rule:** For every check, name the failure it CANNOT catch. A guard whose fixture is smaller than the threshold it guards can never fail.
- **Failed:** Four separate checks reported success on one job while never examining the thing that was actually wrong. A coverage audit diffed ToolIDs against a registry and passed on code that could not complete a stage. `py_compile` parsed syntax and ran nothing. A row-count check would have accepted an 82-row lookup table transcribed by hand. An archive check counted files and never opened them.
- **Why:** Each check was sound within its own scope, and each scope excluded the failure mode. Passing them in sequence produces a strong feeling of verification with none of the substance, because the gaps are between the checks rather than inside any of them.
- **Worked:** For each check, name the failure it CANNOT catch, then decide whether something else covers that. Where nothing does, add a check that touches the real artifact: execute the code on real data, assert a marker string inside each delivered file, verify a decoded byte count against its source. Cheap and specific beats broad and structural.
- **Evidence:** measured
- **Hits:** 3   (2026-08-28 four checks that each excluded the real defect; 2026-08-28 a regression guard whose fixture was too small to trip the threshold it guarded; 2026-09-01 a selftest fixture whose two neighbours fell BELOW a floor set by an unrelated pair)
- **Repeat 2026-08-28 - the guard written FOR this lesson had this exact defect:** after finding that `lesson_brief.py --digest` truncated at 24, a selftest case was added to stop it regressing. The fixture held 2 rules. A 2-rule file cannot be truncated by a limit of 24, so the guard reported OK against a deliberately reintroduced bug - 18/18, exit 0, no signal at all. Only the negative control exposed it. Widening the fixture to 30 rules made the same reintroduction fail at 17/18, exit 1. A test fixture is part of the scope: sizing it below the threshold under test scopes the risk out just as completely as checking the wrong artifact.
- **Worked (addendum):** Size every fixture ABOVE the boundary it exercises, and run the negative control - reintroduce the bug and confirm the suite actually fails - before trusting any new guard. `sed` the default back, re-run, assert a non-zero exit.
- **Repeat 2026-09-01 - the same defect, one layer further out:** a new selftest for the lesson_dupe Distinct-from fix passed against the KNOWN-BROKEN script. The fixture held 7 entries, and lesson_dupe's floor is the p99.5 of pairwise similarity, which on 21 pairs is simply the maximum. That maximum belonged to a pair of BASELINE entries, so the new entry's two neighbours scored 0.9863 and 0.9846 against a floor of 0.9976 and neither was ever "above floor". The gate therefore never reached the branch under test. Sizing the fixture is not enough - the fixture must be able to REACH the threshold, and when the threshold is derived from the fixture's own distribution, an unrelated pair can hold it out of reach. Fixed by making the three entries byte-identical in the compared text so all three tied at the maximum; the case then failed on the broken script and passed on the fixed one.
- **Promoted-to:** copilot-instructions.md, "Rules already paid for" (LESSON-DIGEST block) - 2026-08-28.
- **See also:** delivery-pointer-file-passes-as-artifact, lessons-digest-default-limit-truncates
### A verifier that counts only value differences blesses a schema change
- **Pattern-Key:** verifier-ignores-structural-diff
- **Date:** 2026-08-28
- **Trigger:** better-approach
- **Rule:** Break your own checker before trusting it. Positive control first, then negatives that each assert WHY it failed.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 2
- **Failed:** The alteryx-to-python parity checker reported PASS on an output whose column had been RENAMED. It recorded the column difference in the per-sheet line but only value mismatches incremented the counter that decided the overall verdict.
- **Why:** Two separate tallies - one for cells, one for structure - and only the first was wired to the verdict. A renamed column breaks every downstream consumer while every cell still matches, so the report was confidently wrong in the one case a human reviewer would never re-check.
- **Worked:** Mutation-test the verifier before trusting it. Inject six known defects (one cell, dropped row, extra row, renamed column, swapped label, sub-tolerance noise) and confirm it catches exactly the five that matter and passes the noise. That surfaced the hole immediately; after the fix, 6/6 caught with true negatives still passing. Applies to ANY checker: a checker nobody has tried to fool is an assumption. **Two refinements added 2026-08-28, from a second checker.** (1) A negative control must assert WHY the checker failed - the message text AND the specific gate the failure was attributed to - not merely THAT it failed, because a defect caught for the wrong reason is a miss that reports as a hit. An earlier `verify_primitives` control passed on its first attempt only because the implementation dodged the injected bug by another route. (2) Run the positive control FIRST and gate the negative suite on it: a suite that cannot demonstrate green proves nothing when everything comes back red. Built that way, a 17-case negative suite for `gate_check.py` caught 17/17 for the right reason with its positive control passing.
- **Evidence:** measured - 6-mutant suite, 1 false PASS before the fix, 0 after; the 17-case suite and its positive control were run and read on 2026-08-28. The earlier `verify_primitives` false-green is reported from a prior session, not re-observed here.
- **Promoted-to:** Skills/alteryx-to-python/SKILL.md - the `gate_check_selftest.py` paragraph (17 deliberately-broken workspaces each failing on the expected gate with the expected message) and "Every zero reported to the user needs a positive control". Read on the mount 2026-08-28 and already present in concrete form, so no move is proposed; this entry is now the evidence trail. The generic form is NOT stated in `copilot-instructions.md`.
- **See also:** delivery-pointer-file-passes-as-artifact, verification-scoped-away-from-the-risk
### A pipeline's exit code is the LAST command's, so `| tail` reports the checker as clean
- **Pattern-Key:** verifier-pipe-masks-the-exit-code
- **Date:** 2026-08-29
- **Trigger:** false-success
- **Rule:** Never read a checker's exit code through a pipe. `cmd | tail` reports tail's status, not the checker's. Run the check bare, or capture `${PIPESTATUS[0]}`.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** Running `python lesson_check.py cowork-lessons.md 2>&1 | tail -25; echo "EXIT=$?"` during the 2026-08-29 audit. It printed `EXIT=0`. The checker had actually exited 1 on a real FAIL - a `promotion_due` defect introduced minutes earlier in the same session by setting `agent-recommends-edit-without-reading-file` to Hits 2 without a `Promoted-to` or `Promotion` line.
- **Why:** In bash `$?` after a pipeline is the exit status of the LAST element, and `tail` almost always succeeds. The FAIL line was visible in the captured stdout, so the defect was caught by reading the output - but the exit code, which is the part a job or a gate would branch on, said the opposite. A batch job wrapping this pattern would have recorded a clean run. Same shape as the always-exits-zero defect the `_template-job.bat` contract was written to stop, but reached through a pipe rather than through a missing error check - so the job contract does not cover it.
- **Worked:** Re-ran the checker bare with stdout discarded - `python lesson_check.py cowork-lessons.md >/dev/null 2>&1; echo $?` - which returned 1 and exposed the real state. Fixed the underlying defect by authoring a `Promotion:` line, then re-verified: `lesson_check` exit 0, `lesson_gate.py audit` clean at 46 rules from 82 entries, digest byte-identical so no second instructions write was needed.
- **Evidence:** measured - both exit codes read in the same session, 0 through the pipe and 1 bare
- **See also:** verifier-warns-on-proxy-not-the-defect, verification-scoped-away-from-the-risk, agent-claims-action-before-doing-it
### A check that warns on a proxy trains you to ignore the real ones
- **Pattern-Key:** verifier-warns-on-proxy-not-the-defect
- **Date:** 2026-08-28
- **Trigger:** better-approach
- **Rule:** Make a check fire on the defect it names, not on a proxy for it. A warning that is always on is training to skip warnings.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** `topic_cluster` warned whenever six keys shared a prefix, on the stated theory that a cluster that large "usually means a repeated failure was re-logged instead of promoted". It fired on all three large clusters every run. Measured 2026-08-28: `bridge-` 17 keys, `skill-` 10, `onedrive-` 6, and across all three exactly ZERO entries at Hits>=2 without a `Promoted-to`. Every warning it had ever emitted was false, and those three standing warnings sat immediately above eight real `promotion_due` FAILs that went unread for days.
- **Why:** Size is a proxy for re-logging, not re-logging itself. A subsystem with three ports and a tunnel legitimately produces many genuinely distinct traps, so the proxy is guaranteed to misfire on exactly the subsystems that get the most use. Worse, the check had no negative control: 14 of the checker's findings were each tested against a deliberately broken log and this one was not, so nothing in the suite could reveal it was measuring the wrong quantity. A token-overlap heuristic was then tried as a replacement and REJECTED on measurement - at Jaccard 0.34 it flagged two pairs, `bridge-8932-parallel-writes-denied` vs `bridge-8932-writes-lf` and `onedrive-read-mount-locally` vs `onedrive-user-mount-read-lag`, and both are legitimately separate traps that merely share words.
- **Worked:** Make the check test the defect it names. A cluster now WARNs only when it contains an entry at Hits>=2 with no `Promoted-to` - actual re-logging - and otherwise reports its size as INFO, so the number stays visible without pretending to be a defect. Negative-controlled two ways before trusting it: forcing the branch off drops the suite to 14/15, and forcing it on reproduces the three old warnings exactly, proving the change is what removed them. Also fixed the summary line, which counted every INFO as prose-only and silently inflated 53 to 56 the moment a second INFO code existed.
- **Evidence:** measured - all three clusters enumerated with hit counts and promotion state, both sabotage runs executed and read
- **See also:** verification-scoped-away-from-the-risk, lessons-digest-default-limit-truncates, verifier-ignores-structural-diff
### A checker that never ran exits non-zero exactly like one that found something
- **Pattern-Key:** verifier-usage-error-reads-as-finding
- **Date:** 2026-08-31
- **Trigger:** failure
- **Rule:** A job that calls a checker must prove the checker RAN, not merely that it exited non-zero. Assert its expected output appears - a usage, path or import error is indistinguishable from a real finding on the exit code alone.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** The genericize job ended with `python lesson_check.py` and no path argument. argparse printed `error: the following arguments are required: path` and exited 2. The guard behaved exactly as designed, reported `COWORK_RESULT: FAIL lesson-check-failed`, and instructed a restore from the pre-edit copies - when the edit had in fact succeeded and had already been verified three ways.
- **Why:** Testing the exit code is right, and was the fix applied to two standing jobs the day before. But an exit code has two states and three causes: the corpus is bad, the corpus is clean, or the checker never executed. Collapsing the first and third produces a false alarm that points at the data when the defect is in the call.
- **Worked:** Read the usage line, confirmed from the job's own earlier assertions that the edits were sound - 0 occurrences on re-read, line counts unchanged in all three files - then ran the standing `2026-08-30-preclose-verify.bat`, which invokes the checker with correct arguments. Exit 0, 91 entries, FAIL 0 WARN 0.
- **Evidence:** measured - argparse exit 2 with a usage message, against exit 0 and a full report from the same checker called correctly minutes later
- **See also:** verifier-pipe-masks-the-exit-code, cowork-close-reports-ok-on-failed-commit
### A checker must read all its evidence before it announces a verdict
- **Pattern-Key:** verifier-verdict-announced-before-evidence-read
- **Date:** 2026-09-02
- **Trigger:** failure
- **Hit 2, same day, in a job written to verify the fix for hit 1.** `2026-09-01-verify-scope-work.bat` ran `digest_apply --check`, got STALE, and printed "renaming ENFORCED to PARTIAL changed what loads at turn 1 - revert the tiers rename". It had never tested that. The block was stale because a CONCURRENT session had added two lesson entries (corpus 111 -> 113); the rename was innocent, proven by generating the always-on block under both tier files and diffing them - identical. The failure message named a cause it had not measured, and would have sent the next session reverting the wrong change. A verdict does not become evidence-led by being placed at the end; it has to be derived from a test that could have come out the other way. v2 replaces the assertion with that diff plus a negative control.
- **Rule:** A checker must gather every piece of evidence BEFORE it adjudicates, once, at the end. Never jump to a FAIL label mid-stream - that skips the step that could contradict it. Take a baseline from a file the run wrote, never from a literal pasted at authoring time. And never let a failure message NAME a cause the job did not test - derive the verdict from a comparison that could have come out the other way.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 4
- **Hit 4, 2026-09-02, outside a batch job and in front of the user.** A PowerShell probe written for the operator to run interactively ended its `catch` with a single label: `NO - blocked: <status>`. Conditional Access refused the device-code sign-in, so the token variable was never set, the request carried a `Bearer` header with nothing after it, and Graph replied `InvalidAuthenticationToken / ArgumentNull` at 401. The script announced `NO - blocked: 401` - an AUTHORIZATION verdict it had never tested - for what was an AUTHENTICATION failure. Two different gates, collapsed into one label by a catch-all. The evidence that settled it was already on screen and unread: the guarded `if ($tok)` block had printed NOTHING, which is the actual finding. RULE EXTENSION - this is not confined to verifier jobs on the PC. Any diagnostic that reports a REASON must derive it, including a snippet handed to a human, where a wrong label is acted on immediately and with more confidence than a job's exit code would earn. Guard the interpreting branch on the precondition holding, and give could-not-test its own distinct message.
- **Hit 3, 2026-09-01 21:12, roughly one hour after hit 2 and AFTER this rule entered the always-on block.** A nightly-readiness job gated on `findstr /c:"Scheduled Task State:          Enabled"` - a literal with a GUESSED number of spaces. schtasks pads that column differently, the match failed, and the job printed "The task exists but is NOT in the Enabled state. It will not fire." directly beneath its own output reading `Scheduled Task State:                 Enabled`. Same signature as hit 1, in a job written to check that a scheduled task would fire. Fixed by asking the scheduler for the STATE - `Get-ScheduledTask ... .State` - instead of asking the console for its column widths, and by splitting the failure into `task-disabled` (a finding) and `task-state-unknown` (a could-not-check), because "I could not confirm Enabled" and "it is Disabled" are different claims and only one of them was evidenced.
- **Promotion:** COMPLETE at 2 hits, by the counter rather than by a second copy. At Hits 2 this rule is selected into the always-on block on the next `digest_apply`, which is the only delivery path measured to work. Both hits landed on 2026-09-01, hours apart, and the second was inside a job written to verify the fix for the first - so the promoted wording carries the sharper half of the lesson, that a named cause must be a tested one. **DO NOT re-promote on hit 3.** The rule was already in the always-on block when hit 3 happened, so it was in context and was missed anyway - the same finding recorded on `deferred-tools-read-as-absent-bridge` at ITS third hit. Delivery is not the constraint and a fourth sentence would add nothing. The only escalation left is a RUNNABLE CHECK, and the specific one this needs is a `job_lint` rule that refuses a `findstr /c:` literal containing a run of two or more spaces - a column-aligned match against console output is brittle by construction, and it is mechanically detectable. Proposed, not built.
- **Failed:** `2026-08-31-verify-trigger-test.bat` printed `COWORK_RESULT: FAIL heartbeat not fresh after the trigger time` directly beneath its OWN step-1 output showing `Last Run Time: 8/31/2026 3:47:01 PM` and `Last Result: 0`, and its OWN step-2 output showing `last verdict CLEAN (exit 0)`. The timed trigger had fired and had produced a measurement file. The verdict was the exact opposite of the evidence printed above it.
- **Why:** Three coupled defects, and only the third generalises. (1) FROZEN BASELINE - `set "BEFORE=<timestamp literal>"` was pasted in when the job was authored, and the arm job never wrote a baseline anywhere, so nothing could refresh it. (2) ABSOLUTE WINDOW - a 0.5h freshness threshold is true only within 30 minutes of one specific trigger; run the next morning it could only fail, and `heartbeat_check.py` defaults to 26h for exactly this reason. (3) EARLY VERDICT - the freshness gate did `goto heartbeat_stale` mid-stream, so the step actually designed to answer the question never ran. Defects 1 and 2 merely supplied bad input; defect 3 is what let a verdict be announced over unread evidence.
- **Worked:** `2026-09-01-verify-nightly-run.bat` plus its `.ps1`. It compares the heartbeat against the task's OWN LastRunTime from `Get-ScheduledTaskInfo`, which is self-relative and stays true on any day it is run; keeps the 26h grace; collects every finding into one array and adjudicates ONCE at the end; and returns exit 2 for could-not-run so a checker that did not run is never mistaken for a checker that found something. Run against the identical machine state that produced the FAIL, it returned `COWORK_RESULT: OK` at exit 0.
- **Evidence:** measured - the two reports exist side by side under `Outputs\2026-08-31 - Trigger Test\` and `Outputs\2026-09-01 - Nightly Run Verify\`, and the old job was re-read from disk before it was archived
- **Distinct-from:** verifier-pipe-masks-the-exit-code - there the checker reached the RIGHT answer and the plumbing destroyed it: a `| tail` replaced the checker's exit code with the pager's, so a real finding was lost and the run read clean. Here the plumbing was sound - every exit code propagated correctly - and the checker itself produced the WRONG answer from correct machinery, because it adjudicated before reading the evidence that contradicted it; one SILENCES a true finding, this one MANUFACTURES a false one, so fixing exit-code propagation cannot catch this and vice versa. ALSO distinct from schtask-hosted-success-describes-the-trigger - there the scheduler's report is TOO NARROW: it truthfully says the trigger fired and says nothing at all about whether work happened, so the reading is correct and simply answers a smaller question than it appears to. Here every piece of evidence was present AND correct - trigger fired, work produced, verdict CLEAN - and control flow branched to a FAIL label before reaching any of it. That entry is about what a value MEANS; this one is about the value never being read. The irony is direct and worth keeping: this verifier distrusted `Last Result 0` exactly as that lesson instructs, and overcorrected into rejecting a true success. NOTE for future dispositions - `lesson_dupe.py` line 192 substring-matches ONE Distinct-from field, so a second Distinct-from line is silently ignored; every neighbour must be named in this single line.
- **See also:** verifier-pipe-masks-the-exit-code, diagnosis-anchored-on-the-known-failure-mode, schtask-hosted-success-describes-the-trigger
### A reported figure that no code path can change
- **Pattern-Key:** nightly-constant-reported-as-a-measurement
- **Date:** 2026-09-01
- **Trigger:** false-success
- **Rule:** Before drawing a conclusion from a number in a generated report, grep for every site that WRITES it. A field with one assignment and no update site is a decoration, and printed beside a real count it reads as a measurement.
- **Delivered-to:** any (host-agnostic)
- **Failed:** Reading `proposals_emitted: 0` next to `findings: 15` in two consecutive nightly measurement files as evidence that dream_analyze's proposal path was dead.
- **Why:** `proposals_emitted` was assigned the literal `0` at nightly_measure.py:305 and never touched again. Three references existed in the entire tree: the assignment, the report key, and a selftest asserting it equalled 0 - which passed whether or not the field carried meaning, because it was always 0. `findings`, by contrast, is genuinely parsed from the analyser's stdout at line 263. Setting the two side by side compared a measurement against a constant. The file's own invariant ten lines above states that a figure the analyser did not produce must be null and never 0, "because a zero would be read next morning as the analyser looked and found nothing" - which is exactly how this field read.
- **Worked:** `grep -n proposals_emitted` across the scripts folder returned three lines and no update site, and running dream_analyze live showed it emitting proposals in quantity. Deleted the field at schema 3, since `findings` already counts them, and replaced the selftest case with one asserting the key is ABSENT so a reintroduction fails.
- **Evidence:** measured - 3 grep hits with no write site; a live analyser run emitted 4 merge candidates, 5 retirement candidates, 1 fixed-but-live rule and 4 relative-date fixes; nightly_selftest 33/33 after the change
- **Hits:** 1
- **Distinct-from:** verifier-warns-on-proxy-not-the-defect - that one is a check that fires on a proxy for the defect; here there is no check at all, only a reported number nothing computes.
- **Distinct-from:** verification-scoped-away-from-the-risk - that one is about a check whose SCOPE excludes the failure; this field has no scope because it has no logic.
- **Distinct-from:** guard-exists-but-the-new-consumer-never-reads-it - the nearest neighbour by vocabulary, because both live in nightly_measure.py and both argue the null-versus-zero point. The mechanisms are opposites. There, a real protection EXISTS and works, and the defect is that a newly written caller never invokes it - the fix is to make the caller read the marker. Here there is no logic to invoke at all: the field is a literal with no computation behind it, so nothing was skipped because there was never anything to skip.
- **See also:** verifier-usage-error-reads-as-finding
### A rule is most likely to be wrong in the first hour after it is written
- **Pattern-Key:** new-rule-is-untested-until-it-survives-a-real-case
- **Date:** 2026-08-28
- **Trigger:** better-approach
- **Rule:** Before encoding a rule, run it against the artifact already in front of you. A rule derived from one observation is a hypothesis, and it stays one until a real case fails to break it.
- **Hits:** 1
- **Failed:** FOUR times in one session, same shape each time. (1) Wrote "never attribute the work to a client", then immediately added an exception clause protecting the word as domain vocabulary, which would have defended the exact phrasing the operator was asking to remove. (2) Wrote "contractions are his register" from a single clause he changed by hand; his finished 4,534-word article carries two. (3) Wrote "always write to the local path", then published that very entry through the cloud path sixty seconds later. (4) Shipped a surface classifier that matched content substrings, so "profile" matched "file" and a rule was filed under the wrong surface for an hour.
- **Why:** A rule feels most certain at the moment of writing, because it was distilled from a case still fresh in mind. That is also the moment it has been tested against exactly one example. Encoding it into a skill file or a script promotes a hypothesis to a standing instruction, and standing instructions are applied silently by sessions that never saw the case that produced them. Three of the four above were caught only because someone used the rule immediately; a rule written and then not exercised would have sat there being wrong.
- **Worked:** Test the candidate rule against material already available before writing it down. For a writing rule, count the pattern across the whole finished document, not the diff hunk that suggested it, which is `myvoice` rule 43. For a code rule, run it over the full corpus and diff the before and after, which is how the classifier's second wrong fix was caught before shipping. For a process rule, do the very next instance of that process deliberately and watch whether the rule holds. Where the rule survives none of that, write it as a scoped observation rather than an absolute.
- **Evidence:** measured - all four instances occurred and were corrected in this session, each with the correction recorded in its own entry
- **See also:** classifier-substring-match-silently-misfiles, onedrive-pick-the-leg-that-does-not-block
### An enforcer can go on enforcing the version of the rule it was born with
- **Pattern-Key:** enforcer-encodes-the-superseded-rule
- **Date:** 2026-09-03
- **Trigger:** false-success
- **Rule:** When a lesson's Rule text is sharpened - or when the THING it counts is redefined - grep for the CHECK that enforces it and update it in the same pass. A check is a frozen copy of the rule as it read on the day it was written. Two ways it goes stale: the wording is sharpened and the check keeps the old wording, or the population is re-tiered and the check keeps counting the old population. In both cases the check keeps firing confidently and its output reads as a measurement.
- **Delivered-to:** any (host-agnostic)
- **Failed:** `job_lint/onedrive-recursive` flagged line 64 of `2026-09-01-scope-placeholder-fault.ps1`, a `Get-ChildItem -Recurse` over the OneDrive tree. Read as a true positive it says a live job violates a standing rule. It is not one: that script walks `.Attributes` only, its own header explains why that is safe, and the lessons entry had been corrected hours earlier to say exactly that.
- **Why:** The rule was written on 2026-08-31 as "never recurse a OneDrive tree" and the check encoded `-recurse` near a OneDrive path. On 2026-09-01 the entry was sharpened by measurement - walking metadata across the whole tree took about a second and hydrated NOTHING; it is reading CONTENT that forces a fetch. The prose changed and the check did not, so the enforcer kept refusing the old, broader thing. Because the rule sits in the ENFORCED tier its prose is held out of turn-1 context, which means the stale check was the loudest surviving statement of it.
- **Worked:** Re-encoded the check to the sharpened rule: a bare enumeration is no longer a finding, a recursion whose output is READ still is. The selftest case was inverted to match - the bad sample now reads, the good sample walks - so a future revert to "flag any -Recurse" fails a named case instead of passing quietly.
- **Evidence:** measured - the flagged line is a metadata-only enumeration, confirmed by reading the script; the check's pattern keyed on `-recurse` alone; after the change the selftest passes 31/31 and the same file is no longer flagged, while a content-reading recursion still is
- **Hits:** 2
- **Second hit, 2026-09-03 - the same failure in `dream_analyze.py`, caught by the operator asking a question rather than by any check.** Its GROWTH section warned "digest carries 90 rules ... every one is read every session" against a hardcoded `80`. Both halves were wrong after the 2026-08-31 tiering: it counted AUTHORED Rule lines in the lessons file (90) rather than the ALWAYS-ON block (30), and only those 30 are read every session - the other 60 load per-surface via `preflight`. The two numbers were the same population until the tiering split them, so the check was correct on the day it was written and silently wrong from 08-31 onward. **It was reported to the operator twice in one evening as a real finding before he asked where the threshold came from; the answer was that nobody set it - it was a literal somebody typed.** Fixed by counting the block itself, naming the tiering in the output, and exposing `--always-on-max` as a documented judgement rather than a hidden constant. The section had ZERO selftest coverage, which is why it shipped: four cases added, including a regression control that fails if the check ever counts the corpus again, and a both-ways control proving the threshold can reinstate a warning as well as silence one. 32/32, analyser re-approved.
- **Rule addendum:** state where a threshold CAME FROM when reporting a finding that rests on it. "Over the threshold of 80" invites a decision; "over a limit nobody chose, measured against the wrong population" does not.
- **Promoted-to:** `copilot-instructions.md` always-on digest tier, position 31 - achieved MECHANICALLY by the repeat rule the moment Hits reached 2, not by a hand-edit. Verified by reading the block back from disk: the always-on count moved 30 -> 31 and this entry's Rule text is present verbatim.
- **Correction, same session:** this entry first carried a `Promotion: DUE` line proposing that a separately-worded rule be hand-added to `copilot-instructions.md`, and the operator was told promotion was waiting on his approval. **That was wrong on both counts.** `digest-tiers.txt` promotes any entry at hits >= 2 automatically - the tier is computed from the lessons file, never hand-listed - so the rule was already loading every session before the proposal was written. Hand-adding prose would have produced a SECOND copy of the same rule, in a different form, able to drift from this one: `config-contradiction-survives-in-second-file`, created by the act of trying to promote. **Before proposing a promotion, read the digest block back and check whether the mechanism has already done it.** The proposal cost nothing here only because it was checked before being applied.
- **Why both hits stayed invisible to automation:** hit 1 was caught by a person reading a flagged line and disagreeing; hit 2 by the operator asking where a number came from. Neither was caught by a check, and the always-on tier is the right home precisely because the sessions that need this rule are the ones editing checks - who do not reliably preflight the `claims` surface first.
- **Distinct-from:** digest-enforced-demotion-outruns-the-enforcer - that is about how FAR an enforcer reaches (which surfaces it can read). This is about WHICH VERSION of the rule it holds. A check can have perfect scope and still enforce last week's wording, and the two failures need different fixes: one widens coverage, the other re-syncs content.
- **Distinct-from:** verifier-warns-on-proxy-not-the-defect - there a checker's OUTPUT was misread by a person. Here the checker's output is exactly what it was programmed to say, and the program is what is out of date.
- **See also:** onedrive-recursive-scan-hydrates-tree, verifier-verdict-announced-before-evidence-read
### A familiar failure mode was asserted as the cause while the disproving evidence sat unread
- **Pattern-Key:** diagnosis-anchored-on-the-known-failure-mode
- **Date:** 2026-08-29
- **Trigger:** correction
- **Rule:** Before naming a known failure mode as the cause, check the evidence that would DISPROVE it. A cause that matches a remembered pattern is a hypothesis competing with others, not a finding.
- **Hits:** 1
- **Failed:** Reporting to the operator that `<client>-apportionment` was not loading and that its 1,019-character description - just under the 1,024 cap, past the 900 working ceiling - was the likely cause. The operator replied that the skill had been replaced by `state-apportionment`. It had been. The skill was not silently unloaded; it was deliberately superseded and deregistered, and the OneDrive folder is residue.
- **Why:** `skill-description-over-cap-unloads-silently` is a lesson already in the digest, so a skill that is absent plus a description near the cap matched a stored pattern instantly. The disproving evidence was one call away and was not made: `state-apportionment` holds the same four stage scripts at near-identical sizes (34,000 / 83,070 / 97,501 / 28,652 against 34,008 / 82,928 / 95,366 / 28,556), the same helpers, seven added intake and validation scripts, a newer SKILL.md, and zero occurrences of the client name. A loaded rule made a wrong answer arrive faster and with more confidence, which is the failure mode of a digest rather than an argument against one.
- **Worked:** State a cause as a hypothesis until the competing explanation has been checked, and for a MISSING component always ask first whether it was replaced. Comparing the two script folders settled it in one call. The operator's recollection outperformed the analysis, so treat a user contradiction as evidence to test immediately, never as something to defend against.
- **Evidence:** measured - both scripts folders listed and the SKILL.md files read after the claim was already made
- **See also:** agent-recommends-edit-without-reading-file, config-contradiction-survives-in-second-file, prune-list-counts-drift-from-names
### A control that asks the model to predict measures a different thing than a test that watches it act

- **Pattern-Key:** control-asks-instead-of-watching
- **Date:** 2026-09-03
- **Trigger:** better-approach
- **Rule:** A control arm must run the SAME task as the test arms, judged by the SAME criterion, differing in exactly ONE variable - whether the thing being tested is reachable. If it asks the model to PREDICT a limitation while the test arms WATCH it avoid one, the comparison is void. Before running a control, diff its wording against the test prompts: a word present only in the control is usually the answer leaking in.
- **Failed:** Built a harness to check whether a delivered rule changes behaviour. The three test arms performed a real task; the control asked "would you expect this operator to be supported by a local evaluator?" It answered correctly at 65% confidence and its own reasoning cited the word `local` - supplied by the prompt - so the control passed on framing, not knowledge. Taken at face value the verdict would have read INERT and the rule would have been deleted as useless.
- **Why:** Prediction and behaviour are different quantities. A model can articulate a limitation it would not have avoided under time pressure in a real task, and can avoid one it could not articulate. Scoring one against the other produces a confident number from an invalid comparison, which is worse than no number.
- **Worked:** Rebuild the control as test prompt 1 verbatim plus one sentence denying it the surface under test. Run it and read the FIRST action, not the eventual answer. On the rebuilt control the model fired the trap on call one and needed six calls to recover, while all three carried arms pre-empted it - a clean, attributable split. Related: a pass criterion that scores "hit the trap and recovered" as a pass also scores the control that way, so it cannot measure delivery either.
- **Evidence:** measured - both controls run live on 2026-09-03 against the same rule; the asking control passed and the watching control failed, changing the verdict from INERT to EFFECTIVE.
- **Hits:** 1
- **Distinct-from:** `nightly-constant-reported-as-a-measurement` - that one is a number nothing writes. This one is a number that IS computed, from arms that are not comparable.
### A completeness check that derives both sides from one pattern proves nothing
- **Pattern-Key:** count-assertion-must-use-independent-control
- **Date:** 2026-09-02
- **Trigger:** failure
- **Rule:** When asserting "the parser got everything", the control count must come from a DIFFERENT criterion than the parser's own regex. Two numbers derived from one assumption always agree, including when the assumption is wrong.
- **Failed:** A solution-list parser asserted `len(rows) == len(present)` where `rows` used `\d+\.\d+\.\d+\.\d+` for the version column and `present` filtered lines with the SAME four-part pattern. It reported a clean 56/56 while dropping the `Default Solution` row, whose version is `1.0`. The assertion existed specifically to catch a dropped row and could not.
- **Why:** Same shape as the 2026-09-01 self-improvement finding - a number was trusted without checking what actually writes it. Here the check and the thing being checked shared a premise, so the check was structurally incapable of failing on that premise.
- **Worked:** Derive the control independently: take every line of the table body between the header and the first blank line. That immediately reported 57 of 58 - catching both the real missing row AND a trailing prose line the bound was wrong about - and the fix was verifiable rather than silent.
- **Rule of thumb:** ask of any self-check "what would have to be true for this to fail?" If the answer is "nothing my parser could get wrong", it is decoration.
- **Evidence:** measured - 56/56 PASS on a known-incomplete parse, then 57/58 FAIL after the control was made independent, then 57/57 PASS after the fix
- **Distinct-from:** nightly-constant-reported-as-a-measurement - there a reported figure had NO computation behind it at all, so no code path could ever move it. Here both numbers are genuinely computed and both are individually correct; the defect is that they are computed from the SAME premise, so they cannot disagree even when that premise is wrong. A field with no logic versus two pieces of real logic sharing one assumption.
- **Distinct-from:** verification-scoped-away-from-the-risk - there a check's SCOPE excludes the failure it was written to catch. Here the scope is exactly right and the check runs on exactly the right data; what fails is the INDEPENDENCE of the control it compares against.
- **Dispositioned:** 2026-09-01 close, by a different session from the one that wrote this entry, derived from its own Why line rather than independent diagnosis - the author should confirm. RESOLVED 2026-09-03 (DC-2026-09-03-POINTER-007): the two See-also keys were dangling and are now repointed by SUBSTANCE - `lesson-check-clean-clusters-were-false` was a memory key, never a Pattern-Key, and its substance is `verifier-warns-on-proxy-not-the-defect`; `gate-selftest-needs-negative-control` resolves to `verifier-ignores-structural-diff`. The same dangling name was also cited in the Distinct-from of `enforcer-encodes-the-superseded-rule`, which lesson_check does not validate, and was corrected in the same pass.
- **See also:** verifier-warns-on-proxy-not-the-defect, verifier-ignores-structural-diff
### Classify by an authored key, never by matching content substrings
- **Pattern-Key:** classifier-substring-match-silently-misfiles
- **Date:** 2026-08-28
- **Trigger:** failure
- **Rule:** Route on the authored identifier (a key prefix), not on a content regex over free text. If content matching is unavoidable, use word boundaries and test the near-misses.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** `lesson_brief.py` classified each lesson into a surface by first-match of a content regex over key plus title. The `files` pattern contained the bare substring `file`, so `skill-voiceprofile-calibrate-from-user-diff` matched on the word **profile** and was filed under `files`. `--for skills` therefore silently MISSED it, and `--for files` returned something irrelevant. Shipped and used for about an hour before anyone looked.
- **Why:** Substring matching over prose has no notion of what the text is ABOUT. Worse, the tool still returns a confident, well-formatted list, so a wrong classification reads exactly like a right one. That is a false negative in the single tool built to prevent false negatives.
- **Worked:** Two changes, and the FIRST attempt at the fix was also wrong. Adding word boundaries alone just moved the damage: reordering the surfaces sent every `onedrive-*` entry into `git`, because their titles mention commits. The correct design routes on the PREFIX of the Pattern-Key, which is authored deliberately and states the subject, and falls back to a word-boundary content regex only for keys whose prefix is unknown. Verified 12 of 12 hand-picked cases, then locked in with `lesson_brief_selftest.py`, 15 of 15, including negative controls asserting that `profile` does not match `files` and `clean` does not drag a key out of `git`.
- **Evidence:** measured - the misclassification was reproduced directly, both candidate fixes were run across all 76 keys and their spreads compared, and the regression suite passes 15/15
- **See also:** lessons-file-section-anchor-must-be-exact, verifier-ignores-structural-diff
### A rule served where it cannot apply costs the rules that can
- **Pattern-Key:** lessons-served-out-of-scope-dilute-the-block
- **Date:** 2026-09-15
- **Trigger:** pattern
- **Rule:** Scope a lesson to the route and platform where its rule can fire. A delivery block is spent attention, not free shelf space.
- **Delivered-to:** any (host-agnostic)
- **Failed:** Every `run_batch_file` result on macOS under Claude Cowork carried an eight-rule operating block of which two applied. The other six told the operator to check tunnel drops, set ports PUBLIC, resync `tasks.json` and run `bridge-health.bat` — on a route with no tunnel, no ports, no `tasks.json` and no `.bat`. Across the corpus, 77 of 123 entries referenced machinery that route does not have.
- **Why:** The corpus grew on the hosted route, where all of it was true, and the delivery mechanism was written to serve the top rules by hit count with no notion of where a rule applies. Hit count measures how often a rule mattered *somewhere*, which on a different route selects for exactly the wrong entries.
- **Worked:** Optional `Routes:` and `Platforms:` fields, absent meaning everywhere, filtered at delivery. Nothing deleted, nothing moved. 27 entries scoped to the Copilot route and 5 to Windows; a Mac job went from 27 candidate rules to the 16 that apply, and the served block became the arg-name rule, the transport-retry rule and the git-status rule instead of six about a tunnel. Scope on what the **Rule** says, never on what the example cites — a first pass keyed on the whole entry scoped a universal rule to Windows because its `Failed:` block showed a `.bat`.
- **Evidence:** measured — the block read before and after, and the corpus counted both ways.
- **See also:** narrow-before-fixing-duplicated-capability
### Anchor a section insert on the FULL heading, never a prefix
- **Pattern-Key:** lessons-file-section-anchor-must-be-exact
- **Date:** 2026-08-28
- **Trigger:** failure
- **Rule:** Scope any structural regex to its target section and anchor on the FULL heading. Over a whole file a prefix matches prose and returns a false negative.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 2
- **Failed:** Twice, in the same file, from the same cause. (1) Appending new entries "at the end" of `cowork-lessons.md` put them under `## Contradictions`, because `## Failures` is the FIRST section and the end of the file is a different section entirely - 21 of 65 entries were misfiled before anyone counted. (2) Verifying the 2026-08-28 four new entries with `s.index('## Contradictions')` reported all four MISFILED when all four were correct: that prefix occurs twice in the file, once inside an entry body, and `index` returned the earlier text mention rather than the heading.
Third instance, same day, different file: a rule-numbering check on `myvoice/SKILL.md` matched numbered lines outside the Voice Profile section and printed `rules: 1 to 7 | count 49 | contiguous False`. Re-scoping the regex to that section alone printed `voice rules: 1 - 42 count 42 contiguous True`. The rules were fine. The check was scoped over the whole file.
- **Why:** All three are the same mistake at different ends of the operation. A section identifier that is a prefix of ordinary body text is not an anchor, and the file discusses its own section names, so prefixes match prose.
- **Worked:** Insert with the complete heading string including its trailing description, assert `count == 1` before replacing, and verify the same way. After writing, print each new key's offset against `index(full_heading)` and assert the ordering. The insert itself was right every time - only the check was wrong, which is the more dangerous shape, because a false MISFILED or false `contiguous False` reading invites a "fix" that would have actually broken a correct file. Generalise past this file: scope ANY structural regex, placement or numbering or count, to its target section. Run over a whole document, a prefix or a stray number matches unrelated text and returns a false negative.
- **Evidence:** measured - the count-2 prefix and the count-1 full heading were both printed on 2026-08-28, as were both numbering readings; the 21-entry misfile was counted in a prior session on this same file
- **Note on Hits:** all three instances fall in ONE session, so this stays at 2 by the separate-sessions definition rather than being inflated to 3.
- **See also:** verification-scoped-away-from-the-risk, verifier-prose-match-needs-normalization
- **Promoted-to:** copilot-instructions.md, "Rules already paid for" (LESSON-DIGEST block) - rule text confirmed present in the digest 2026-08-28.
### A guard that greps a whole path matched the guard script's own filename
- **Pattern-Key:** guard-substring-matches-its-own-filename
- **Date:** 2026-08-29
- **Trigger:** failure
- **Rule:** Anchor a path guard to where the path actually starts (`findstr /b /c:"Quarantine/"`). An unanchored substring search matches the job's own filename and aborts a correct run.
- **Hits:** 1
- **Failed:** The correction job checked its staged list with `findstr /i /c:"Quarantine" /c:"<client>"` and aborted with `quarantine-still-staged`. The staged list was CLEAN. The match was `CommandJobs/2026-08-29-quarantine-residue.bat` - the name of the job that had done the quarantining.
- **Why:** Same defect shape as the `--for skills` miss where "profile" contained "file", inverted: there a substring caused a false negative, here it caused a false positive. A guard that blocks correct work is not harmless - it trains you to loosen or skip the guard, and the second run is where the real mistake gets waved through.
- **Worked:** Anchor with `/b` so only a path BEGINNING with `Quarantine/` matches, and add a NEGATIVE CONTROL in the same job: write a known-bad path to a temp file and assert the check still fires on it. Without that control, "no match" is indistinguishable from "the check is broken". Both ran and both passed before the commit was allowed.
- **Evidence:** measured - the false positive aborted one run, the anchored version plus its control passed the next
- **See also:** classifier-substring-match-silently-misfiles, verifier-warns-on-proxy-not-the-defect, verification-scoped-away-from-the-risk
### A wrapped string defeats both the edit AND the grep that verifies it
- **Pattern-Key:** multiline-string-defeats-single-line-grep
- **Date:** 2026-08-27
- **Trigger:** false-success
- **Hits:** 1
- **Failed:** Renaming a job title across 18 skills. Replaced `"Corporate Tax Solutions"` with a single-line search, then verified with `grep -rl "Corporate Tax Solutions"`, which returned NONE. Reported the change complete. 16 files still had it - the body notices wrap as `Corporate Tax\n> Solutions`, so the literal never matched on either pass. Found only when the gamma-tango attribution check surfaced the old title in the loaded skill context.
- **Why:** Markdown body text is hard-wrapped at ~78 chars, so any two-or-three-word phrase can straddle a line break, often with a `> ` blockquote marker inserted. A single-line search is blind to it - and crucially the SAME blindness hits the verification step, so the check confirms the bug rather than catching it.
- **Worked:** Search and replace with a multiline regex that tolerates the wrap and the quote marker: `re.compile(r'Corporate\s+Tax\s*\n?\s*>?\s*Solutions')`. Verify with the SAME regex, never with the flat literal. Rule: when the edit pattern must be multiline, the verification pattern must be multiline too - reusing the flat literal to "confirm" is how a partial edit reports clean.
- **Evidence:** measured - 16 files fixed after the first pass reported zero remaining

---
### A placeholder shaped like the deliverable is a false delivery, not an honest gap
- **Pattern-Key:** delivery-pointer-file-passes-as-artifact
- **Date:** 2026-08-28
- **Trigger:** false-success
- **Failed:** Shipping a conversion zip containing `AUDIT_TRAIL_NOTE.md` - a short file saying the real audit trail lived at `...\data\Output\AUDIT_TRAIL.md` on the PC that ran the job - in the slot where the contract listed `AUDIT_TRAIL.md`. The archive was verified by listing contents, counting files and checking the CRC. All three passed. The operator asked "is the audit trail not in the zip?" It was not.
- **Why:** Nothing was invented, so it did not register as fabrication - but a pointer file carries the deliverable's NAME while withholding its CONTENT, so the file listing looks complete and the gap becomes invisible. An outright omission would have been noticed. The verification compounded it: counting files is exactly the check a stub passes.
- **Rule:** A file carrying the deliverable's NAME but not its content is a false delivery, not an honest gap. Bring the artifact back and check its byte count against the source, or list it as not produced with the reason - nothing in between. Counting files is exactly the check a stub passes.
- **Worked:** Two permitted responses when an artifact was produced somewhere unreachable - bring it back (base64 through the bridge, decoded and the byte count checked against the source rather than retyped) or list it as not produced with the reason. Nothing in between. And verify archives by CONTENT: per-file minimum size plus a marker string only the real file contains, plus, for a run log, a figure from THAT run. The recovered file decoded to exactly 6,532 bytes matching the source.
- **Evidence:** measured
- **Hits:** 1
- **See also:** verifier-ignores-structural-diff
### Two memory stores exist and drift apart silently
- **Pattern-Key:** memory-two-stores-drift
- **Date:** 2026-08-20
- **Trigger:** contradiction
- **Rule:** A fact gets ONE home. Pointer tier is short keys; the deep file is mechanism and evidence. On conflict the file wins.
- **Delivered-to:** any (host-agnostic)
- **Failed:** Treating `save_memory` as "saved to persistent memory." It writes to the built-in memory store (59 entries), not to `Documents/Cowork/cowork-memory/*.md`, which is what the `persistent-memory` skill reads and what `CoworkConfig\` commits to git.
- **Why:** They are separate systems with no sync between them. On 2026-08-20 the built-in store held three entries from that day while every file in `cowork-memory/` still read 2026-08-18 — a two-day drift that was invisible until the folder was listed.
- **Worked:** SUPERSEDED 2026-08-25 — see `memory-tiering-pointer-vs-deep`. (Old rule: write durable findings to BOTH stores. That duplication was the cause of the drift, not the cure.)
- **Hits:** 2
- **Evidence:** measured — folder listing showed all four files last modified 2026-08-18
- **Promoted-to:** copilot-instructions.md, "Rules already paid for" (LESSON-DIGEST block) - rule text confirmed present in the digest 2026-08-28.
### Duplicating a fact across both memory stores causes the drift it was meant to prevent
- **Pattern-Key:** memory-tiering-pointer-vs-deep
- **Delivered-to:** any (host-agnostic)
- **Date:** 2026-08-25
- **Trigger:** correction
- **Hits:** 1
- **Failed:** Following `memory-two-stores-drift`'s instruction to write durable findings to
  BOTH the built-in store and `cowork-memory/*.md`. By 2026-08-25 the built-in store held 80
  entries, many of them commit-level restatements of what the files already said
  (`fact-deckbuilder-v31-committed`, `fact-conflicted-quarantined`, `fact-lessons-logged`).
  Two copies of one fact age independently and there is no signal for which is current.
- **Why:** The two stores have different strengths and duplicating flattens both. The built-in
  store loads before the first turn with no bridge and no OneDrive, but caps at 512 characters.
  The files hold unlimited mechanism and are git-versioned, but only load if a skill fires AND
  OneDrive has replicated. Copying content into both gives the reliability of the file and the
  brevity of the memory — the worst half of each.
- **Worked:** Tier them. The built-in store is the POINTER layer: one `ptr-<slug>` per focus
  area naming the deep file and when to read it, plus genuinely short standing facts. The files
  are the DEEP layer. One home per fact; on conflict the FILE wins and the pointer is updated.
  Applied 2026-08-25: `ptr-cowork-lessons`, `ptr-cowork-bridge-infrastructure`,
  `ptr-cowork-config-setup`, `ptr-cowork-skill-design`, governed by `instruction-memory-tiering`.
- **Evidence:** measured — 80 built-in entries against 4 deep files covering the same subsystems
- **See also:** memory-two-stores-drift, skill-over-description-cap-silently-dropped
### A settled rule is only settled once every surface that states it agrees
- **Pattern-Key:** config-contradiction-survives-in-second-file
- **Date:** 2026-08-21
- **Trigger:** contradiction
- **Rule:** A rule is settled only when EVERY surface that states it agrees. Before calling one done, grep the instructions file, every SKILL.md, the memory folder and the stored-memory index for the old wording, and fix them in the same pass - routing loads whichever copy it reaches first, and the dangerous copy is usually the one that loads precisely when the rule matters.
- **Failed:** Treating "no autorun fallback" as done after fixing `cowork-bridge-infrastructure.md`. The forbidden path was still taught in two other places: the "Fallback when the command bridge is down" section of `copilot-instructions.md`, and a section of the `local-file-bridge` skill instructing the filesystem bridge to drop scripts into `COPILOT_COWORK\autorun\queue` when 8933 is down. The `local-file-bridge` copy was the dangerous one, because that skill is loaded exactly when 8933 is unavailable.
- **Why:** The same rule is restated across instructions, several SKILL.md files, memory files and stored memories. Fixing the surface that prompted the correction leaves the others intact, and routing picks whichever one loads.
- **Worked:** When a rule changes, grep every config surface for the forbidden term before declaring it removed - `grep -rni "<term>" /mnt/user-config/skills --include=SKILL.md`, the instructions file, the memory folder, and the stored-memory index. Fixed all three surfaces and deleted the contradicting stored memory `pref-8933-down-use-autorun-queue`.
- **Evidence:** measured - grep found the three surfaces; all re-read after editing
- **See also:** git-repo-clean-not-dirty
### Do not recommend an edit to a file you have not read this session
- **Pattern-Key:** agent-recommends-edit-without-reading-file
- **Date:** 2026-09-02
- **Trigger:** contradiction
- **Failed:** Putting "two skills now teach the wrong thing" on a next-steps list, asserting that `git-bridge` and `command-bridge` both mandate the schtasks pattern for jobs over ~60s and needed relaxing. Reading them showed `git-bridge` contains zero mentions of async, schtasks or long-running jobs, and `command-bridge`'s only "long job" text is retry discipline that is still correct. There was no documentation bug at all.
- **Why:** The claim was generated from stored memory about what those skills say, not from their contents. Memory records conclusions, not file text, and a remembered summary drifts from the file exactly like a remembered prune list drifts from disk.
- **Hits:** 3 (2026-08-21 agent summary; 2026-08-25 memory store; 2026-09-02 twice in one session - a stale `tasks.json` header comment read as the watchdog's current state and reported to the operator as a live availability gap, and a proposal to merge bridges 8931-8934 behind one port made without reading their per-port supergateway flags. Both were disproved by opening the file: `_bridge-watchdog.ps1` lists all four ports, and 8931 carries `--stateful` where the others must not. A COMMENT describing code is the same class of stale summary as a remembered one - read the code)
- **Promotion:** 2026-08-29 - Rule authored and carried into the copilot-instructions.md LESSON-DIGEST, so it now loads every session.
- **Rule:** Read the file or config surface this session before proposing a change to it, and quote the lines that are or are not there. Memory records conclusions, not file text. Say plainly when a recommendation turns out to be unfounded rather than quietly dropping it.
- **Worked:** Read or grep the actual file before proposing a change to it, and say plainly when a recommendation turns out to be unfounded rather than quietly dropping it. Same discipline as re-enumerating a directory before deleting.
- **Evidence:** measured - both files read end to end, zero matches
- **See also:** prune-list-counts-drift-from-names, agent-claims-action-before-doing-it
### A stored constraint about a script decays when the script is improved
- **Pattern-Key:** git-sync-scope-memory-went-stale
- **Date:** 2026-08-28
- **Trigger:** contradiction
- **Rule:** Read the script before designing around a remembered constraint about what it does. A stored scope claim decays silently when the script is fixed.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** Carrying the stored fact that `2026-08-18-sync-cowork-config.bat` copies `SKILL.md` ONLY, recorded 2026-08-20 after `review_strip.py` could not reach the repo. On that basis the operator was warned that the pending commit would silently miss all four changed `scripts/*.py` files and would need extra verification to catch it.
- **Why:** The job was improved at some point after 2026-08-20 and its Skills leg now reads `robocopy "%SRC%\Skills" "%DEST%\Skills" *.md *.py *.js /S /PURGE`. A memory records a script's behaviour at one instant; the script is then edited and nothing revisits the memory, so a claim that was true once keeps being repeated with the confidence of a fresh measurement. This is the same decay shape as a stale "X is broken" open item, applied to a capability rather than a fault - and it biases the opposite way, planning around a limit that no longer exists.
- **Worked:** Read the job with `read_text_file` before relying on the stored scope, and let the commit stat prove it. Commit ac6d9ec carried all four scripts - `lesson_brief.py`, `lesson_brief_selftest.py`, `lesson_check.py`, `lesson_check_selftest.py` - 8 files, 245 insertions, and `git status --short` empty afterwards. Corrected the memory in the same pass, keeping the half still true (the PC's local OneDrive copy can lag a cloud write, and robocopy exit 0 means nothing was copied) and deleting the half that is not.
- **Evidence:** measured - the robocopy line read verbatim from the job before the run, and all four scripts present in the commit stat afterwards
- **See also:** git-repo-clean-not-dirty, onedrive-cloud-to-laptop-lag, bridge-devtunnel-declared-dead-without-reprobe

## Open questions
### Five review rounds hardened a skill that had never run once
- **Pattern-Key:** review-rounds-outpaced-the-first-real-run
- **Date:** 2026-08-31
- **Trigger:** better-approach
- **Rule:** Count the production runs before accepting another round of hardening. A component at v1.5 with ZERO runs is being improved against imagined failure modes; ship it, watch one real run, then harden against what actually happened.
- **Hits:** 1
- **Failed:** dream-cycle went 1.0.0 -> 1.5.0 in a single evening across five external review rounds, roughly 25 real defects fixed, and was never once executed on its own schedule. The fifth review proposed a machine-readable state artifact with a deterministic transition validator - a genuinely strong idea - 90 minutes before the first scheduled run. Installing a new fail-closed gate immediately before a first run inverts its purpose: a gate that fails closed INCORRECTLY blocks the very run that would have produced the evidence it needs.
- **Why:** Each round was individually correct and the hit rate was high, so "one more round" always looked justified. What that framing hides is that review finds CONTRACT defects - contradictions, missing dependencies, undefined branches - and by round five those were nearly exhausted, while the untested surface (does the email send, does the checkpoint compare, does the judged half produce useful proposals) had not moved at all. The same session had already reached this conclusion about lessons: 48 unmeasured rules and 71 unmeasured rules are the same epistemic position. It was not applied to the skill being built.
- **Worked:** The fifth review's OWN priority ordering resolved it - two of its five items were marked "implement after observing several natural runs", its regression suite needs runs to regress against, and its acceptance criteria are all measurements requiring runs. Accept the diagnosis, defer the build. Concretely: let the first scheduled run happen on the current version, capture what it actually does, and build the state validator informed by that. Record the deferred items so deferral is not loss.
- **Evidence:** measured - execution_count 1 (the setup call, not a sweep), next_execution_time 90 minutes out, five SKILL.md versions committed the same evening
- **See also:** new-rule-is-untested-until-it-survives-a-real-case, verification-scoped-away-from-the-risk
### Every defect that would have broken the run was an integration defect, not a logic error
- **Pattern-Key:** integration-defects-outnumber-logic-errors
- **Date:** 2026-08-31
- **Trigger:** better-approach
- **Rule:** When a routine names a file, a script or a tool, check the acquisition step in the SAME edit. The defects that break an unattended run are dependencies declared in one section and absent from another - not bad logic.
- **Hits:** 1
- **Failed:** Three separate times in one session dream-cycle told a scheduled run to read something its manifest never fetched: `lesson_gate.py` (the routine called `lesson_gate audit`; it would have died at the digest step after completing the analysis), `analyser.approved` (the gate treated a missing marker as FAILED INTEGRITY and would have deadlocked on its own first run forever), and the determinism reference. A fourth was self-inflicted in the same class: the selftest wrote the marker in Python text mode, producing CRLF, while the validator matched `[0-9a-f]{64}\n?` - the gate rejected its own file.
- **Why:** Logic errors are visible in the section you are editing. Integration defects live in the GAP between two sections that are each individually correct, so re-reading either one finds nothing. Prose review catches them only by holding both halves in mind at once, which is exactly what a careful reader does until the one time they do not.
- **Worked:** Two techniques, and they catch different classes. A LITERAL DRY RUN - follow the acquisition steps exactly, using only what they name - found the CRLF mismatch and a stale live digest that no reading would have surfaced. Then `manifest_check.py` made it mechanical: the skill declares `acquires:` and `not_acquired:`, and the check FAILS on any referenced dependency in neither list. 3/3 including a reproduction of the real defect. `not_acquired` is explicit on purpose - a file deliberately not fetched is a decision, and writing it down is how the next editor knows it was one rather than an omission.
- **Evidence:** measured - all four defects reproduced, manifest_check verified against a sabotaged manifest that omits lesson_gate.py
- **See also:** verifier-pipe-masks-the-exit-code, guard-substring-matches-its-own-filename
### Researching how to build it is not the same as checking whether it exists
- **Pattern-Key:** prior-art-unsurveyed-before-building
- **Date:** 2026-09-02
- **Trigger:** better-approach
- **Rule:** Before building a capability, run ONE search for an existing implementation - vendor-published skills, MCP servers, the platform's own tooling. Do it FIRST, not after the build is working. "How do I authenticate to X" and "does a supported X integration already exist" are different questions, and only the second one can save the whole build.
- **Failed:** Spent a day on Power Automate integration - Entra registration attempts, device-code flows, PAC CLI wrapping, solution pack/import, then a hand-built OAuth path - researching authentication mechanics repeatedly and thoroughly. Never once searched whether Microsoft already published something for this. Only after the bridge worked did a survey find `microsoft/power-platform-skills` (FlowAgent, MIT, ~52 tools including run history and desktop-flow execution, no app registration needed in commercial cloud).
- **Why:** The question that got asked was always "how do I make MY approach work", which is answerable and rewarding at every step, so it never ran out of road and never prompted the wider question. Each auth dead end produced a real finding, which felt like progress and disguised that the whole line of work might be unnecessary.
- **Worked:** One web search naming the product and "MCP" or "skill" returned the vendor implementation immediately. Surfacing it late still had value - it named the real capability gaps - but it should have been the FIRST call of the day, before any code.
- **Evidence:** measured - the survey that found it took a single search and returned a maintained, permissively licensed, strictly larger implementation
- **Hits:** 1
- **Distinct-from:** `tooling-install-researched-before-approval-checked` - there the research was thorough and the missing step was a POLICY check (is this approved here). Here the policy question never arose because the prior-art question was never asked. One skipped a permission gate, the other skipped the build-versus-adopt decision entirely.
### Narrow before fixing a capability the host already has
- **Pattern-Key:** narrow-before-fixing-duplicated-capability
- **Date:** 2026-09-15
- **Trigger:** pattern
- **Rule:** Before repairing a component, ask whether the host now does the same job. A duplicated component is worth deleting, not fixing.
- **Delivered-to:** any (host-agnostic)
- **Failed:** Hours went into the filesystem bridge — diagnosing the schema fault, finding the zod root cause, preparing to vendor a dependency tree — before anyone asked whether the bridge should exist. Each finding justified the next step, and none of them questioned the goal.
- **Why:** A handoff that names a component as the task makes the component the frame. The repository was built when Cowork shipped none of connected folders, a browser, memory or a plugin installer; three of its four bridges had since become duplicates, and the port-and-tunnel vocabulary was carried over from the hosted route where it still belongs.
- **Worked:** Asking what each component adds that the host does not. Three of four bridges and five of ten skills turned out to be scaffolding; the approved executor is the one thing with no first-party equivalent. Narrowing removed the schema fault, the npx fetch and the upstream dependency from the Claude route without fixing any of them.
- **Evidence:** measured — `bridges in scope 1 of 4`, `INSTALL_CHECK: CLEAN`, and the executor confirmed running natively on Darwin while the session shell runs on Linux.
### Check branch protection before pushing, because the undo may be blocked
- **Pattern-Key:** git-protected-branch-bypass-not-reversible
- **Date:** 2026-09-15
- **Trigger:** failure
- **Rule:** Read the branch's protection rules before pushing to it. An admin bypass that succeeds does not imply an undo that succeeds.
- **Delivered-to:** any (host-agnostic)
- **Failed:** `git push origin main` succeeded with `Bypassed rule violations for refs/heads/main: Changes must be made through a pull request. 2 of 2 required status checks are expected.` The correction — rewinding `main` and reopening the change as a PR — was then rejected: `GH006: Protected branch update failed. Cannot force-push to this branch.`
- **Why:** The ruleset allows an admin to bypass the pull-request requirement but not to force-push. The two permissions are independent, so a bypass can be one-way.
- **Worked:** Nothing rewound it. The commit stayed on `main` and the duplicate branch was deleted. Every later change went to a branch first. Additional damage was caused by `git reset --hard` during the attempted undo, which stripped the committed files out of the working tree; it was recoverable only because the commit was already on the remote.
- **Evidence:** measured — both remote responses read verbatim.
### Deleting a file does not remove it from git history
- **Pattern-Key:** git-deletion-does-not-sanitize-history
- **Date:** 2026-08-20
- **Trigger:** failure
- **Failed:** Assuming that excluding the engagement skills from the mirror and committing the deletions made the repo safe to push.
- **Why:** `git status` showed them as deletions of TRACKED files — they had been committed in `5ff400d` and sit in that commit and every one since. `git log`, `git show`, and any clone still surface the client name in the path. A deletion commit stops future propagation; it does not sanitize.
- **Rule:** Committing a deletion does not sanitize git history - the path survives in every prior commit and every clone. A repo that ever held engagement content can never be the one pushed; populate a NEW repo by copying named folders in, never by cloning and filtering.
- **Delivered-to:** any (host-agnostic)
- **Worked:** Accept that this repo can never be the one pushed. Any GitHub repo must be NEW, populated by copying named folders in — never by cloning and filtering, which carries invisible history. State the limitation in the deletion commit body so no one later mistakes it for a sanitization.
- **Evidence:** measured — tracked-deletion status read after the commit
### Run `git ls-files` before deleting anything called "scratch"
- **Pattern-Key:** git-check-tracked-before-deleting
- **Date:** 2026-08-21
- **Trigger:** failure
- **Rule:** Run `git ls-files` before deleting anything that looks like scratch. Untracked files take a plain delete; tracked files take `git rm` and a commit that says why.
- **Delivered-to:** any (host-agnostic)
- **Failed:** A prune list described seven COPILOT_COWORK files as disposable scratch. Five of them — `bridge-test.txt`, `copilot-test.txt`, `page-2026-07-27*.yml`, `session-handoff-test.txt` and `CommandJobs/Output/DEPRECATED-DO-NOT-USE.txt` — were tracked in git. A plain delete would have left the repo dirty with phantom deletions instead of recording them.
- **Why:** Files that look like throwaway probes are often committed early, when the repo is young and everything gets added.
- **Worked:** `git --no-pager ls-files | findstr /V /C:"CoworkConfig/"` first, then split the list: untracked files get a plain delete, tracked files get `git rm` plus a commit that says why. Also verify "empty" folders really are empty — `Outputs\Outputs` was described as an empty duplicate and contained a subfolder.
- **Evidence:** measured
### Renaming a client is not sanitizing its data
- **Pattern-Key:** git-renaming-is-not-sanitizing
- **Date:** 2026-08-31
- **Trigger:** near-miss
- **Rule:** Before stripping a client name, check whether the CONTENT is also client-specific. If the file's substance is the client's work product, renaming is concealment rather than sanitization - stop and put the decision to the owner.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** Nothing shipped, which is the only reason this is a near-miss. Seven occurrences of one client name were genericized across three memory files - correctly, because there the name was decoration on lessons about process. The next move, already queued and about to run, was to apply the identical treatment to 41 occurrences of a SECOND client name in `je-builder`, `alteryx-to-python` and `cowork-alteryx-conversion.md`.
- **Why:** The two cases are indistinguishable to a grep and are opposites in substance. In the first, deleting the name lost nothing - the lesson taught a process and the client was incidental. In the second the files ARE the engagement's work product: account-code mappings and legal-entity structure, not a client name that merely appears in them. Removing the header word leaves every mapping in place while making the tree READ as sanitized, so the next audit returns a clean grep and the exposure becomes invisible. A cosmetic fix to a disclosure problem is worse than no fix, because it retires the signal that would have prompted a real one.
- **Worked:** Stopped before editing and put three options to the operator - leave it as engagement work in its sanctioned location, split the generic taxonomy from an engagement-local mappings file, or rebuild the mappings as illustrative examples. The test to apply: is the name DECORATION on generic content, or the LABEL on client content? Decoration can be genericized freely; a label is the owner's call.
- **Evidence:** measured - 41 occurrences located across 3 skills and 1 memory file by scoped findstr, with the file and line of each; none edited
- **See also:** git-deletion-does-not-sanitize-history, cleanup-quarantine-instead-of-delete
### Quarantine by moving with a manifest instead of deleting
- **Pattern-Key:** cleanup-quarantine-instead-of-delete
- **Date:** 2026-08-21
- **Trigger:** better-approach
- **Failed:** Nothing broke - but a blanket "just delete them" on 111 files is the one step in a cleanup that cannot be undone if the filter is wrong by even one entry.
- **Why:** A move produces the identical clean end state as a delete while staying reversible, and it costs only disk. The filter is the risky part, not the removal.
- **Worked:** Move matches into a dated quarantine folder preserving relative structure, write a MANIFEST.csv (RelativePath, Type, Bytes, LastWriteTime, OriginalFullPath), and hard-ABORT the run if a known live file matches the filter - the 2026-08-21 job checked for `memory\memories.json` and would have exited without moving anything. Re-scan afterwards to prove 0 remaining. Result: 111 moved, 0 failed, 0 left, counts matching the prior inventory exactly (Demo 49, Tasks 36, Skills 26).
- **Evidence:** measured
- **See also:** git-check-tracked-before-deleting, prune-list-counts-drift-from-names
### Quarantining into a folder inside the repo puts the content INTO version control
- **Pattern-Key:** quarantine-destination-inside-the-repo
- **Date:** 2026-08-29
- **Trigger:** failure
- **Rule:** A quarantine destination must be OUTSIDE the repository. Moving files to a folder inside it and then running `git add -A` commits the very content the move was meant to remove.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** Moving `<client>-apportionment`, its zip and an empty folder from the Cowork Skills folder into `COPILOT_COWORK\Quarantine\2026-08-29 - Skill Residue`. That path is inside the git repo. The sync/commit job then ran `git add -A` and commit cffae50 added 17 client-named files, 7957 insertions. The `/XD` rule in the sync job had successfully kept those paths OUT of the working tree for nine days; the quarantine put them in.
- **Why:** The quarantine rule says move-with-a-manifest rather than delete, and it was followed exactly - the destination was simply never checked against the repo boundary. Two individually correct rules (quarantine rather than delete; commit the session's work) compose into a defect when the quarantine lands inside the thing being committed. `Outputs/` was already gitignored, which is why no previous job had ever hit this.
- **Worked:** Because the repo is local-only and cffae50 was the tip, `git reset --mixed HEAD~1` undid it cleanly rather than layering a deletion commit that would have left the content in history forever. Then: move the folder to `Downloads\COWORK_QUARANTINE` (outside the repo), add `Quarantine/` to `.gitignore`, re-stage, re-commit as 353104a, then `git reflog expire --expire=now --all` and `git gc --prune=now` to drop the abandoned objects. Verified by `git log --oneline cffae50` returning "unknown revision" and `git ls-files` matching no client name.
- **Evidence:** measured - tracked-file list captured before and after, abandoned commit confirmed unreachable
- **See also:** git-deletion-does-not-sanitize-history, cleanup-quarantine-instead-of-delete
### Deadness is a property of the reference graph, not of the file
- **Pattern-Key:** artifact-deadness-needs-consumer-grep
- **Date:** 2026-08-31
- **Trigger:** near-miss
- **Rule:** Before moving or deleting a file, grep the files that would REFERENCE it and record the count. A filename-and-timestamp audit proves nothing about whether a file is dead.
- **Hits:** 1
- **Failed:** A filename-and-mtime audit listed `intercompany-eliminations\MANUAL INPUTS.xlsx` as dead residue and it reached the approved quarantine list. Reading `intercompany-eliminations\SKILL.md` showed Rule 2 names that exact file as one of two REQUIRED upfront build inputs. Quarantining it would have broken a working skill silently - the failure would have surfaced only at the next build, far from the cause.
- **Why:** An audit that inspects only the candidate can never see its consumer, so a load-bearing input and abandoned residue score identically. Age and an unreferenced-looking name are properties of the file; being dead is a property of what points at it.
- **Worked:** Grepped each candidate's owning `SKILL.md` for the candidate's filename before moving anything, and recorded the count. Three superseded drafts scored 0 references and were moved; `MANUAL INPUTS.xlsx` scored a required-input citation and stayed. The cleanup job then asserted its presence both BEFORE and AFTER the move, with a hard abort either way, so the guard survives the next run of the same job.
- **Evidence:** measured - 0 references for `SS_SKILL v1.md`, `SS_SKILL v2.md` and the pre-approved-batch-executor draft; a required-input citation for `MANUAL INPUTS.xlsx`
- **Distinct-from:** agent-recommends-edit-without-reading-file - that lesson says read the file you are about to CHANGE, and the file to read is the file you are acting on. Here you can read the candidate file completely, end to end, and still be wrong, because the evidence that it is load-bearing lives in a DIFFERENT file - the consumer that references it. Same instinct, different search target: one says read your subject, this one says find who depends on your subject. Kept separate on that basis, but they are close enough that if a third instance of either appears it should be logged as a hit on whichever it matches, not as a fourth key.
- **See also:** agent-recommends-edit-without-reading-file, prune-list-counts-drift-from-names, cleanup-quarantine-instead-of-delete

## Contradictions — stored memories that proved wrong
### A job that snapshots before mutating destroys its own rollback on re-run
- **Pattern-Key:** artifact-rollback-overwritten-on-rerun
- **Date:** 2026-08-31
- **Trigger:** near-miss
- **Rule:** Guard a job's pre-edit snapshot with an existence check. A job that copies originals aside and then mutates them is safe only on its FIRST run - re-running it overwrites the rollback with the already-mutated content.
- **Hits:** 1
- **Failed:** Nothing was lost, but the obvious recovery was the destructive one. After the genericize job failed on its final check, the instinct was to fix the argument and re-run it. That job's first action copies the three target files into `pre-edit\`. A re-run would have overwritten those originals with the already-edited versions, leaving no way back.
- **Why:** The mutation itself is idempotent - replacing a token that is now absent changes nothing - and that masks the fact that the SNAPSHOT step is not. Judging a job safe to re-run from the safety of its main action skips the setup that runs before it.
- **Worked:** Did not re-run it. Ran a separate verification job instead, leaving the pre-edit copies intact. The durable fix is an `if not exist` guard around the snapshot copy, so the first run's originals always win.
- **Evidence:** inferred from the job text - the copy is unconditional and precedes the replacement, so a second run would overwrite the originals; deliberately not executed twice to confirm it
- **See also:** cleanup-quarantine-instead-of-delete, artifact-deletion-reverts-after-verified-absent
### A constructor that enumerates its fields silently discards every field added later
- **Pattern-Key:** constructor-drops-the-field-added-later
- **Date:** 2026-09-02
- **Trigger:** failure
- **Rule:** When a function rebuilds an object from a hand-picked list of fields, adding a field upstream does NOT reach the consumer - it is dropped in transit, with no error. After adding a config key or an envelope property, grep for every place that reconstructs that object and add it there in the SAME edit. The symptom is a downstream error that names the WRONG cause: a missing id looks like a permissions failure, a missing property looks like malformed input.
- **Failed:** Twice in one session on the same bridge. (1) Added `flow_env_id` to `flow-bridge.config.json`; `requireEnvironment()` returns a NEW object built from four named fields, so the key never arrived and every Flow-service call used the bare guid - answered `403 EnvironmentAccessDenied`, which reads exactly like a permissions wall. (2) `toClientData()` passes an already-wrapped envelope straight through without adding `schemaVersion`, so the shape the tool's own description asks for returned `HTTP 400 Required property 'schemaVersion' not found`. The documented usage was the broken one.
- **Why:** Both functions were written when the field set was complete, and both take the shape "read these N fields, build a new object". That is correct on the day and silently lossy forever after. Nothing fails at the boundary, so the error surfaces far downstream wearing the vocabulary of the API rather than of the bug.
- **Worked:** Carried the field explicitly and said so in a comment naming the trap - `requireEnvironment` now returns `flow_env_id`, `toClientData` fills `schemaVersion` and `connectionReferences` when a caller omits them. Both fixes verified by re-running the exact call that had failed.
- **Evidence:** measured - 403 then 200 on the same environment id after the field was carried; 400 then a created flow on the same definition after the envelope was filled
- **Hits:** 1
- **Distinct-from:** `lessons-parser-keeps-only-the-first-repeated-field` - that is a PARSER keeping the first of several values it did read. This is a CONSTRUCTOR never reading a value at all because it was not on the list. Parsing kept the wrong one; construction kept none.
### A token audience is not a hostname, and aiming at it reads as "the API does not exist"
- **Pattern-Key:** api-audience-is-not-a-hostname
- **Date:** 2026-09-02
- **Trigger:** failure
- **Rule:** An OAuth resource identifier and the callable endpoint are DIFFERENT strings and only one resolves in DNS. Before concluding an API is unsupported, confirm you aimed at the HOST: a `getaddrinfo ENOTFOUND` on a resource URI means you called the audience, not that the service is absent. Look up the host separately from the scope.
- **Failed:** Wrote off `api.flow.microsoft.com` as "not a supported API and not even a valid token audience", recorded that in the bridge source AND the config as settled fact, and rebuilt 8934 on Dataverse alone - accepting that flow run history was unreachable. The reasoning came from a real observation: a request to `https://service.flow.microsoft.com/...` returned `getaddrinfo ENOTFOUND`.
- **Why:** `service.flow.microsoft.com` is the AUDIENCE - an identifier that appears in the token's `aud` claim and has no DNS record. `api.flow.microsoft.com` is the host that serves the API. Both are real and they are not interchangeable. The ENOTFOUND was produced by my own wrong URL and read as evidence about Microsoft's service.
- **Worked:** Asked for a token scoped to `https://service.flow.microsoft.com/user_impersonation`, then sent it to `https://api.flow.microsoft.com`. Token issued with `aud=https://service.flow.microsoft.com`; the host answered 200. Run history, triggers, per-action detail and the connector catalogue were all reachable on auth that had been working since that morning.
- **Evidence:** measured - two probe runs. First run: token issued, API call ENOTFOUND. Second run, host corrected: 30 environments returned, every one HTTP 200, two real runs with status, timing and trigger name.
- **Hits:** 1
- **Distinct-from:** `deferred-tools-read-as-absent-bridge` - there a capability was present and the PROBE could not see it. Here the probe was fine and the ADDRESS was wrong. Both end in "it is not available", from opposite causes.
- **See also:** enforcer-encodes-the-superseded-rule
### Check whether a capability is ALLOWED before spending turns on whether it works
- **Pattern-Key:** tooling-install-researched-before-approval-checked
- **Routes:** copilot
- **Date:** 2026-09-02
- **Trigger:** correction
- **Rule:** Before researching, pricing or proposing any software install on the firm-managed machine, ask whether it is approved. Availability is not permission, and a clean install path is no evidence the install is allowed. Dev Tunnels specifically is NOT approved - do not re-propose it.
- **Failed:** The last open config item was that `devtunnel.exe` is absent, so setting the four bridge ports Public in the VS Code Ports panel is manual after every restart. Asked what devtunnel was, I answered, then ran a web search, fetched Microsoft's docs to establish the install route (`winget install Microsoft.devtunnel`, or a direct download from `aka.ms/TunnelsCliDownload/win-x64`), confirmed it lands under `%LOCALAPPDATA%` and so needs no admin, worked out that a job calling it would need an absolute path, and offered to install it and test whether the CLI could adopt VS Code's existing tunnels. The operator: "dev tunnels is not explicitly approved for installation."
- **Why:** A capability probe answers "CAN this be made to work" and returns nothing about "MAY this be made to work". The two questions look identical from inside the probe, and only the technical one has a satisfying answer, so it is the one that gets asked. Earlier the same day the opposite happened and went well: a research pass into flow auth surfaced, unprompted, that reusing the Azure CLI client ID would be policy evasion, and that route was dropped before any work went into it. The difference was not judgement - it was whether something else happened to raise the permission question. An open-items list phrased as a missing tool actively suppresses it, because the entry reads as a to-do rather than as a decision nobody has taken.
- **Worked:** Dropped it on the correction, with no attempt to find another route to the same capability, and corrected the two records that had framed it as pending. `fact-devtunnel-cli-absent` said the manual step stands "unless the devtunnel CLI is installed" - an open door that would have produced this same proposal again from a later session reading the same list. Both records now state that the manual Public-port step is permanent by design and name the reason.
- **Evidence:** measured - the search and the doc fetch both happened before any approval question was asked, and the correction arrived immediately after the install offer. The generalisation to other unapproved software is inference unverified.
- **Hits:** 1
- **Distinct-from:** probe-env-vars-blank-false-negative and bridge-devtunnel-declared-dead-without-reprobe - all three sit on devtunnel, which is exactly why they invite being filed together, and both of those are MEASUREMENT failures with a measurement fix. There a probe searched blank `%LOCALAPPDATA%` paths and wrongly reported the CLI absent; there a stale stored open item was repeated without re-probing. Both are answered by measuring better, and both were: the 2026-08-21 reprobe confirmed devtunnel really is absent. This entry starts where those finish. The absence is correctly measured and not in dispute; what was never asked is whether installing it is PERMITTED. No probe, however well scoped, returns that - so a better measurement is the wrong instrument, and reading this as another hit on either of them would prescribe exactly the fix that does not apply.
- **See also:** bridge-restart-authorisation-needs-bounds
### A hosted scheduler's success describes the trigger, not the work
- **Pattern-Key:** schtask-hosted-success-describes-the-trigger
- **Routes:** copilot
- **Date:** 2026-08-31
- **Trigger:** false-success
- **Rule:** A scheduler reporting success proves a TRIGGER fired, never that work happened. Require an artifact the job itself wrote - a report, a heartbeat - and treat its absence as failure however green the scheduler looks.
- **Delivered-to:** any (host-agnostic)
- **Hits:** 1
- **Failed:** Four scheduled dream-cycle runs reported success. One of them produced nothing for 5h 43m: `2026-08-31.md` was created at a measured 12:46:16Z against an assumed 07:00Z trigger. The scheduler had no way to say "I fired into a session that never woke", because from its side those two outcomes are identical.
- **Why:** A scheduler owns exactly one event - the trigger. Whether anything downstream executed is outside what it observes, so its success field answers a narrower question than the one being asked of it. Windows Task Scheduler has the same shape: `Last Result: 0` is what the 2026-08-18 battery trap printed while producing zero output - that trap lives in the MEMORY store as `fact-schtasks-battery-trap-2026-08-18`, and naming it on a `See also` line raised a dangling_see_also WARN, because that field takes Pattern-Keys from this file only.
- **Worked:** Moved the measurable half onto the machine and made it write evidence. `nightly_measure.py` writes `measurements-YYYY-MM-DD.json` plus a heartbeat on EVERY exit path, and `heartbeat_check.py` reads the heartbeat's AGE. The install job then fired the task through the scheduler and asserted a fresh heartbeat within 0.25h rather than trusting `Last Result: 0` - measured 2026-08-31, heartbeat at 16:49:02Z, age 0.01h.
- **Evidence:** measured - scheduler reported Last Result 0 AND a fresh heartbeat was independently confirmed; the two are separate facts and the job requires both
- **Distinct-from:** verifier-usage-error-reads-as-finding - that one is about a checker's own EXIT CODE being unreadable because a usage error and a real finding both exit non-zero. This one is about a DIFFERENT PROCESS reporting on work it never observed: the scheduler's exit code is accurate about the trigger and silent about the job, so the fix is an external artifact rather than a wider exit-code vocabulary.
- **See also:** elapsed-time-is-not-execution-time, schtask-scheduled-prompt-cannot-preauthorize-a-send
### Elapsed is not execution
- **Pattern-Key:** elapsed-time-is-not-execution-time
- **Date:** 2026-08-31
- **Trigger:** correction
- **Rule:** A gap between a scheduled hour and an artifact's timestamp is LATENCY, not duration. Never call it execution time without a start stamp the job itself wrote.
- **Hits:** 1
- **Failed:** Called a 5h 43m gap "execution time" for the dream cycle. Attended runs of the same job took 2m 21s, 12m 35s and 11m 14s - so the 5h 43m was almost entirely dormancy before the work began, not work.
- **Why:** Subtracting a scheduled hour from a completion stamp measures the interval between an INTENTION and a RESULT. Everything in between - dormancy, queueing, a machine asleep - is inside that number and indistinguishable from work. It reads as a performance figure while actually being a latency figure.
- **Worked:** Made the job stamp its own start: `run_started_at`, `run_ended_at` and `elapsed_s` come from inside `nightly_measure.py`, so duration is measured by the thing being timed. The dream-cycle's Step Zero was separately found unable to prove dormancy at all - `GetScheduledPrompts` returned `no_scheduled_prompt`, so its "464 minutes elapsed" inherited an ASSUMED trigger hour and only the 38s from invocation to first artifact was measured.
- **Evidence:** measured - 4.36s self-timed elapsed on the first real run, against three attended runs of 2m21s / 12m35s / 11m14s
- **Distinct-from:** schtask-hosted-success-describes-the-trigger - that is about a BOOLEAN (did it run) being reported by a process that cannot see the answer. This is about a DURATION being computed from two clocks that bracket more than the work, and it stays wrong even when the run genuinely happened.
### Replacing a block verbatim drops every obligation the new text does not restate
- **Pattern-Key:** skill-verbatim-replace-drops-unrestated-clauses
- **Date:** 2026-08-26
- **Trigger:** failure
- **Hits:** 1
- **Failed:** Applying a handoff pack's prepared §4 block verbatim over the existing §4. The
  replacement was correct in what it said, but two obligations that lived only in the old text
  and were not restated in the new block vanished with it. A whole-section replacement shows in
  the diff as one delete plus one insert, so nothing marks the lost clauses as lost.
- **Why:** A diff is line-oriented and a wholesale block swap defeats it — the reviewer sees a
  new section that reads correctly and has no signal pointing at what the old one carried.
  Reading for correctness of the NEW text cannot detect an omission in it.
- **Worked:** Before applying any prepared block over existing text, enumerate the imperative
  clauses in the OLD text and confirm each one survives in the new. Confirm with a normalised
  search (strip line breaks, collapse whitespace) rather than by eye — line wrapping produced a
  false negative on the first pass and made a surviving clause look deleted.
- **Evidence:** measured — two dropped obligations found on re-read after the replacement landed
- **See also:** agent-recommends-edit-without-reading-file, config-contradiction-survives-in-second-file
### A skill description is router matching text, not a slot for instructions
- **Pattern-Key:** skill-description-is-trigger-text-not-instruction-slot
- **Date:** 2026-08-26
- **Trigger:** better-approach
- **Hits:** 1
- **Failed:** Writing directives ("always do X", "never do Y") into a SKILL.md `description`.
  They never execute — nothing reads a description as instruction — and they consume the
  character budget that trigger phrases need, so the skill also matches worse.
- **Why:** The description is consumed by the router for matching only; the body is what a
  loaded skill executes. A directive there is therefore doubly wasted — inert AND crowding.
  Inference unverified: the crowding effect on match quality is reasoned from the budget, not
  measured directly.
- **Worked:** Treat the directive-to-trigger ratio as the diagnostic when a skill mis-fires: if
  a description contains imperatives, move them into the body and refill the space with trigger
  phrasing and the `Do NOT use` exclusion. Trim toward roughly 800 UTF-16 units, not the 1024
  cap — leaving headroom keeps a later edit from silently pushing the skill over.
- **Evidence:** measured — descriptions rewritten and re-scored; inference unverified on the Why
- **See also:** skill-over-description-cap-silently-dropped, savememory-512-cap-rejects-silently

---
### A substring memory remove deleted the whole entry
- **Pattern-Key:** memory-remove-substring-deletes-whole-entry
- **Date:** 2026-11-14
- **Trigger:** failure
- **Rule:** After any memory-tool batch, read the result's removed_entries / patched_entries_after and verify the on-disk file. A remove op whose old_text is a substring deletes the ENTIRE entry containing it, not the substring.
- **Delivered-to:** any (host-agnostic)
- **Failed:** An op intending to strip one clause from the identity entry removed the whole entry from USER.md; the batch reported success and the loss was invisible until a later migration review read the file.
- **Why:** remove matches by containment but deletes by whole entry; near-duplicate entries made which copy matched ambiguous.
- **Worked:** The pointer/deep migration diffed the actual file contents, found the missing block, and restored it from the batch output that still held the last good text.
- **Evidence:** measured — before/after contents of ~/.hermes/memories/USER.md.

### An unquoted colon broke a skill's frontmatter
- **Pattern-Key:** skill-frontmatter-colon-yaml-breaks
- **Date:** 2026-11-14
- **Trigger:** failure
- **Rule:** A skill description must not contain an unquoted colon — quote the value or reword. skill_manage aborts the ENTIRE batch on a YAML frontmatter parse error.
- **Delivered-to:** any (host-agnostic)
- **Failed:** description "Build auditable automation: gates, named gaps, control arms." → "YAML frontmatter parse error: mapping values are not allowed here"; the whole 5-op batch rolled back.
- **Why:** In YAML, key: value inside an unquoted scalar makes the parser treat the colon as a mapping start.
- **Worked:** Dropping the colon ("Auditable automation with gates, named gaps, control arms.") — batch applied.
- **Evidence:** measured — skill_manage error output and the successful retry.

### A 63-char skill description is rejected
- **Pattern-Key:** skill-description-60-char-cap-rejects
- **Date:** 2026-11-14
- **Trigger:** failure
- **Rule:** Count description length before creating or patching a skill; Hermes rejects >60 chars (the skill index clips anything longer).
- **Delivered-to:** any (host-agnostic)
- **Failed:** "Log or recall lessons with Pattern-Keys, evidence keys, ledger." (63) → batch aborted, all touched skills rolled back.
- **Why:** The 60-char index cap is enforced at create time, after other validations.
- **Worked:** Shortened to "Log or recall lessons with Pattern-Keys and evidence keys." (57).
- **Evidence:** measured — skill_manage error output.

### Browser ops hit the ACTIVE tab, not the one last named
- **Pattern-Key:** browser-exec-uses-active-tab
- **Date:** 2026-11-14
- **Trigger:** failure
- **Rule:** Before acting in a multi-tab browser session, verify location.href; new_tab switches the active tab, and every js()/click lands on whatever is active — not on a tab an earlier call navigated.
- **Delivered-to:** any (host-agnostic)
- **Failed:** Gemini "Search chats" clicks silently no-oped (clicked=False, no Recents) while the active tab was still the claude.ai challenge page from an earlier call.
- **Why:** Sessions persist across calls; the active tab is not remembered by the helper — it is whatever the browser currently shows.
- **Worked:** Opened a fresh Gemini tab (making it active) and re-checked location.href before each batch of ops.
- **Evidence:** measured — page state dumps showing url=claude.ai during the failed clicks.

## Agent instructions

These are instructions for everything related to Agent work. They apply to every task, no exceptions.

## Scope

1. **Work only inside the current repository.** 

Do not read, write, or execute anything outside the repository root, ~\csci6032-hw2-enreysen-um.

## Secrets & Sensitive Data

2. **Never read, print, store, commit, or upload secrets, credentials, private keys, browser data, or configuration files that may contain them.** 

This includes but is not limited to: 
`.env` files, `.pem`/`.key` files, `~/.ssh`, `~/.aws`, `~/.config`, browser profile/cookie stores, and any file matching common secret patterns. 

## Before Making Changes

3. **Explain an intended change before editing.** 

Describe what will be changed and why before modifying any file.

4. **Ask before:**
   - installing software or dependencies
   - accessing a new network destination
   - deleting files
   - changing Git history (rebase, amend, reset --hard, etc.)
   - committing
   - pushing

5. **Preserve uncommitted user work and Avoid destructive Git commands.** 

Do not run Git commands without explicit confirmation from the user. Preferably, do not run Git commands at all. 

6. **Check `git status` before editing and stop if unreleated changes are present.** 

If unrelated or unexpected changes are present in the working tree, stop and alert the user before proceeding.

## Making Changes

7. **Make small, reviewable changes.** 

Prefer minimal, focused diffs over broad rewrites. Split unrelated changes into separate steps.

## After Making Changes

8. **Show `git diff` after editing** and **run the smallest relevant test**

Verify the change (a single test file test case preferred).

9. **Explain errors rather than silently ignoring them.** 

If a command fails, a test breaks, or output looks unexpected, report it to the user and report next steps instead of proceeding as if it succeeded.

10. **Never claim success without checking the requested result.** 

Verify the actual outcome (test output, file contents, command exit status) before reporting that a task is complete.
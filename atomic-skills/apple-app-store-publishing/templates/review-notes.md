# Reviewer packet template

Prepare this in the language appropriate for the review team. Remove instructions/placeholders before submitting. Repository copies must contain only credential references; supply actual authorized demo credentials in App Store Connect's intended review fields, not in public files.

## App and candidate

- App record / platform:
- Version and build:
- First release or changes in this update:
- Main purpose and intended audience:

## Reviewer access

- Login required? Why?
- Synthetic demo account reference:
- Where authorized credentials will be supplied:
- Authentication/verification steps that are reproducible by the reviewer:
- Demo data and reset procedure:
- Geographic, hardware, network or service prerequisites:
- Contact for review-access problems:

Verify the instructions from a fresh installation and unauthenticated session. Do not disable production security broadly or provide access to customer data for convenience.

## Guided test paths

| Feature | Starting screen | Steps | Expected result | Special setup |
| --- | --- | --- | --- | --- |
| Main user journey | | | | |
| Purchase / restore, when applicable | | | | |
| Permissions / data-sharing choice, when applicable | | | | |
| Account deletion, when applicable | | | | |
| Unusual or regulated feature, when applicable | | | | |

## Policy and operational notes

Explain only relevant unusual behavior, attached permissions/licenses, data-sharing choices, account lifecycle, purchase classification and any required hardware. Reference accurate guideline sections and evidence. Identify available backend environment and support owner. Do not present planned features as implemented or activate hidden functionality only after review.

## Attachments

- Synthetic demonstration video/screenshots, if helpful:
- Supporting documentation, when applicable:
- No personal information or reusable secrets in public attachment URLs:

## Response to a review issue

For each issue record:

1. Reviewer's exact concern and cited section.
2. Reproduction outcome on the submitted build.
3. Specific change or evidence-backed clarification.
4. New build/version when a binary change was made.
5. Updated verification steps and observed result.

Keep the response factual and respectful. Do not claim a fix or re-test that has not occurred, promise approval, or conceal unresolved limitations.

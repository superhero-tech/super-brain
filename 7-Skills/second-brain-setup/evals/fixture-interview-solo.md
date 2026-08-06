# Fixture: Interview Path - Solo Operator

## Scenario

The user picks Path B (interview). Profile: solo operator, pre-PMF, wearing every hat.

## Inputs

### Step 0: Path choice

> B

### Q1 - Context

> I am a solo founder, I do everything myself - from the code to the marketing. I am building a SaaS for contract management aimed at small law firms. 12 users on beta, zero revenue, my savings are running out. Law firms need something simpler than the enterprise contract suites but more professional than Excel. My competition is mostly Excel and Word, because the existing tools are too expensive for a 3-5 person firm. My key metric is retention - do beta users come back every week.

### Q2.1 - Directness

> A

### Q2.2 - Structure

> A

### Q2.3 - Length

> A

### Q2.4 - Tone

> C

### Q2.5 - Challenge level

> A

### Q3 - Development areas

> 6 and 1. Execution and Delivery, Analytics and Data. I tend to build features instead of measuring what works.

### Q4 - Goal

> Get to 50 paying users and find out whether this business makes sense before I run out of money. I am giving myself 4 months.

### Confirmation

> OK

## Expected output

### Structural assertions

- [ ] File written to `8-System/about.md`
- [ ] Contains the heading `# About me`
- [ ] Contains the sections `## Context`, `## How to work with me`, `## Current goal`, `## History`
- [ ] The History section contains a dated "profile created" entry (or equivalent)

### Content assertions - Context

- [ ] Contains "solo founder" or equivalent
- [ ] Contains "SaaS" and "law firms" (or "lawyers")
- [ ] Contains the beta detail (12 users) and the lack of revenue
- [ ] Contains the competitive picture (Excel/Word vs expensive tools)

### Content assertions - How to work with me

- [ ] Contains 5-8 bullets
- [ ] Reflects the multiple-choice answers: blunt/hard (A), structured (A), short (A), dry tone (C), demanding (A)
- [ ] References the development areas: Execution/Delivery and Analytics/Data
- [ ] Contains an operational note about the tendency to build instead of measure
- [ ] Does NOT imply that a solo founder is "less of a product builder" than someone in a corporate role

### Content assertions - Current goal

- [ ] Contains "50 paying" and "4 months" (or synonyms)
- [ ] Contains the business-validation element

### Flow assertions (checked during the run, not in the output)

- [ ] Q1 asked as a single block with 6 sub-questions (not 6 separate exchanges)
- [ ] Q2.1-Q2.5 asked one at a time (5 separate exchanges)
- [ ] Q3 shown as a list of 8 options
- [ ] The about.md proposal was shown BEFORE writing
- [ ] The AI waited for confirmation before writing

### Red flags

- [ ] The AI split Q1 into 6 separate questions
- [ ] The AI asked Q2 as an open question instead of multiple choice
- [ ] The AI wrote the file without a proposal and confirmation
- [ ] The AI modified brain.md

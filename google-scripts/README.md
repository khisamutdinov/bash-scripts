# Google  Script to Cleanup a GMAIL inbox

## Installation

Open https://script.google.com/home/all
Create a new project, select an editor, paste the contents of [emailer.js](./emailer.js)
Save the file, select setCleanupTrigger from the dropdown and click RUN

## Setup
functions `purge` and `archive` has the `search` fields. Here can come any valid gmail search query.
examples:
```
  const search = '-in:important -in:starred -label:utilities-gas -label:utilities-power {category:updates category:promotions category:social} ';
```
This search aggregate all the emails from the updates, promotions and social categories that don't contain flags important or starred and that also don't labeled as utilities/gas or utilities/power
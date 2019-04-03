UKWA Manual QA Dataset
======================

This is an extract from our crawl curation database, showing the result of the QA process for those crawl targets that have been manually checked.

The form is

- *Target ID* The UKWA ID for this crawl target.
- *Title* The title of this crawl target.
- *Live Site Status* Whether the site is still live or not (may be out of date - good thing to auto check!)
- *QA Result* The QA outcome (as text but it's a restricted vocabulary of outcomes)
- *QA Issue - Content* True if there were content problems.
- *QA Issue - Appearence* True if there were appearence problems.
- *QA Issue - Functionality* True if there were functionality problems.
- *Open Access* True if the Target is open access (and thus publicly available)
- *Primary URL* The main URL for this target
- *Other URLs* A list of the other URLs for this target.


The file is [`target-qa-dataset.csv`](./target-qa-dataset.csv).

The [`target-qa-dataset-oa-subset.csv`](./target-qa-dataset-oa-subset.csv) file contains just the Open Access ones.

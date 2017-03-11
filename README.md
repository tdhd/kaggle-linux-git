# Kaggle linux kernel dataset

This repository contains all commands and scripts that will reproduce the dataset on kaggle.

TODO: link

## Preparing the data

First, you need to get the latest git clone of the stable linux kernel source:

`git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git`

With the cloned repository, you can then start the first step of data revision log extraction, from master branch, with:

```
cd linux-stable
git log --date=iso --pretty=format:"%at%x09%ad%x09%H%x09%an%x09%ae%x09%s" --stat --no-merges > raw.revlog
```

If during export you encounter

```
warning: inexact rename detection was skipped due to too many files.
warning: you may want to set your diff.renameLimit variable to at least 779 and retry the command.
```

try increasing the rename limit with `git config diff.renameLimit 999999` and rerun the export command.

This will take a few minutes and produce the raw revision log. The time I last ran it, the file had about `200 MB` of size.

We will find the following information in that file:

* author date as UNIX timestamp
* commit date in ISO format
* commit hash
* author name
* author email
* subject of commit
* one line per changed file with the number of lines changed and a proportional count of `+` and `-` for additions and deletions respectively
* and a final summary of total number of files changed and total additions and deletions.

The first few lines look like this, where all attributes for commit a separated by `\t` except for the file detail information:

```
1487807129	2017-02-22 15:45:29 -0800	e8c26ab60598558ec3a626e7925b06e7417d7710	AuthorNameA	AuthorEmailA	mm/swap: skip readahead for unreferenced swap slots
 include/linux/swap.h |  6 ++++++
 mm/swap_state.c      |  4 ++++
 mm/swapfile.c        | 47 +++++++++++++++++++++++++++++++++++++++++------
 3 files changed, 51 insertions(+), 6 deletions(-)

1487807126	2017-02-22 15:45:26 -0800	4b3ef9daa4fc0bba742a79faecb17fdaaead083b	AuthorNameB	AuthorEmailB	mm/swap: split swap cache into 64MB trunks
 include/linux/swap.h | 11 +++++++--
 mm/swap.c            |  6 -----
 mm/swap_state.c      | 68 ++++++++++++++++++++++++++++++++++++++++++----------
 mm/swapfile.c        | 16 +++++++++++--
 4 files changed, 79 insertions(+), 22 deletions(-)
```

### Processing the raw revision log

To make this revision log useable for kaggle purposes we need to apply some postprocessing. We will do that with the help of this [processing script](process.py) or an interactive session with this [notebook](notebooks/revlog conversion.ipynb).

In that transformation to CSV we want to:

* transform each file changed per commit into one line in the final CSV file
* transform the information from author name and email into an author ID.

The final CSV file will then contain the following columns:

* author_timestamp: UNIX timestamp of when the commit happened
* commit_hash: SHA-1 hash of the commit
* commit_utc_offset_hours: Extraced UTC offset in hours from commit time
* filename: The filename that was changed in the commit
* n_additions: Added lines
* n_deletions: Deleted lines
* subject: Subject of commit
* author_id: Anonymized author ID.

## Notice

The output CSV file is the file that was used to produce the kaggle dataset. Since the linux kernel is a highly active project, the output of the final CSV might change depending on when you check the repository out.

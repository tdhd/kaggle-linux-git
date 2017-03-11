# Kaggle linux kernel dataset

This repository contains all commands and scripts that will reproduce the dataset on kaggle.

TODO: link

## Preparing the data

First, you need to get the latest git clone of the stable linux kernel source:

`git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git`

With the cloned repository, you can then start the first step of data revision log extraction with:

```
cd linux-stable
git log --date=iso --pretty=format:"%at%x09%ad%x09%H%x09%an%x09%s" --stat --no-merges > raw.revlog
```

If during export you encounter

```
warning: inexact rename detection was skipped due to too many files.
warning: you may want to set your diff.renameLimit variable to at least 779 and retry the command.
```

try increasing the rename limit with `git config merge.renameLimit 999999` and rerun the export command.

This will take a few minutes and produce the raw revision log, with:

* author date as UNIX timestamp
* commit date in ISO format
* commit hash
* author name
* subject of commit
* one line per changed file with the number of lines changed and a proportional count of *+* and *-* for additions and deletions respectively
* and a final summary of total number of files changed and total additions and deletions.

The first few lines look like this, where all attributes for commit a separated by `\t` except for the file detail informations:

```
1474539321      2016-09-22 06:15:21 -0400       629d0a8a1a104187db8fbf966e4cc5cfb6aa9a3c        Joe Thornber    dm cache metadata: add "metadata2" feature
 Documentation/device-mapper/cache.txt |   4 +
 drivers/md/dm-cache-metadata.c        | 278 ++++++++++++++++++++++++++++++----
 drivers/md/dm-cache-metadata.h        |  11 +-
 drivers/md/dm-cache-target.c          |  38 +++--
 4 files changed, 278 insertions(+), 53 deletions(-)

1475518580      2016-10-03 14:16:20 -0400       ae4a46a1f60942263d6fd119fe1da49bb16d2bd5        Joe Thornber    dm cache metadata: use bitset cursor api to load discard bitset
 drivers/md/dm-cache-metadata.c | 48 ++++++++++++++++++++++++------------------
 1 file changed, 28 insertions(+), 20 deletions(-)
```

### Processing the raw revision log

To make this revision log useable for kaggle purposes we need to apply some postprocessing. We will do that with the help of a few python functions.

You can use the notebook for an interactive processing of this data or just run the [processing script](process.py) script to convert the raw revlog to CSV format.

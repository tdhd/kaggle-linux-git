#!/usr/bin/env python
import pandas as pd
import dateutil.parser
import re

raw_revlog_filename = 'raw.revlog'

grouped_lines = []

with open(raw_revlog_filename) as f:
    group = []
    for line in f:
        if line == '\n':
            grouped_lines.append(group)
            group = []
        else:
            group.append(line.strip())

def file_stats_from(description):
    match = re.search('(.*) +\| +(\d+) +(.*)', description, re.IGNORECASE)
    filename = match.group(1)
    n_lines_changed = int(match.group(2))
    changes = match.group(3)
    n_add = int(1.0 * n_lines_changed * changes.count('+') / len(changes))
    n_del = int(1.0 * n_lines_changed * changes.count('-') / len(changes))
    return [filename.strip(), str(n_add), str(n_del)]

timestamps = []
commit_dates = []
hashes = []
names = []
emails = []
subjs = []
filenames = []
n_adds = []
n_dels = []

for group in grouped_lines:
    tsv, remaining = group[0].split("\t"), group[1:]
    ts_author, commit_date_iso, commit_hash, author_name, author_email, subj = tsv[0], tsv[1], tsv[2], tsv[3], tsv[4], tsv[5]
    file_changes = [r for r in remaining if not ('(-)' in r or '(+)' in r)]
    details = [file_stats_from(changes) for changes in file_changes]

    for detail in details:
        timestamps.append(ts_author)
        commit_dates.append(commit_date_iso)
        hashes.append(commit_hash)
        names.append(author_name)
        emails.append(author_email)
        subjs.append(subj)
        filenames.append(detail[0])
        n_adds.append(detail[1])
        n_dels.append(detail[2])

def tz_from(date_str):
    d = dateutil.parser.parse(date_str)
    hours_from_utc = d.tzinfo.utcoffset(d).total_seconds() / 3600.0
    return int(hours_from_utc)

df = pd.DataFrame(
    {
        'author_timestamp': map(lambda e: long(e), timestamps),
        'commit_utc_offset_hours': map(tz_from, commit_dates),
        'commit_hash': hashes,
        'author_name': names,
        'author_email': emails,
        'subject': subjs,
        'filename': filenames,
        'n_additions': map(lambda e: int(e), n_adds),
        'n_deletions': map(lambda e: int(e), n_dels)
    }
)

# unique identifiers for our author mapping
unique_author_ids = df.apply(lambda row: row['author_name'] + ' ' + row['author_email'], axis=1).unique()
translation = {author_id: index for index, author_id in enumerate(unique_author_ids)}
df['author_id'] = df.apply(lambda row: translation[row['author_name'] + ' ' + row['author_email']], axis=1)

df.drop('author_email', axis=1, inplace=True)
df.drop('author_name', axis=1, inplace=True)

df.to_csv('kaggle_linux_kernel_git_revlog.csv', index=False)

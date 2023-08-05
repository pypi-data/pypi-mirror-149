==============================
Change log for gocept.bbissues
==============================

0.10 (2022-05-02)
=================

- Remove support for Python 2.7.


0.9 (2021-09-17)
================

- Add support for Python 3.6, 3.7 and 3.8.

- Migrate to GitHub and GitHub Actions.


0.8.1 (2017-06-30)
==================

- Be more robust if the PRs or Issues are not available.

- Add logging in case of an API error.


0.8 (2016-07-07)
================

- Don't crash on generating html if unicode is in the comments.

- Handle PullRequests from GitHub correctly.

- Add assignee as a property to an item and use it in the standard template.


0.7 (2016-02-03)
================

- Add time_rendered as a variable passed to the jinja2 template.

- Add the count of comments to the issue/pullrequest and pass to template.

- Read the owner from the config file and collect all projects from this owner.

- Add new template that renders a table with filter options.

- Export type (Issue, PullRequest) to JSON file.


0.6 (2016-01-27)
================

- Save HTML to a file which is specified in config. Made path to JSON file
  configurable.


0.5 (2016-01-26)
================

- Add JSON export for issues and pullrequest not older that `json_export_days`
  specified in config.


0.4 (2016-01-14)
================

- Improve error handling.


0.3 (2016-01-13)
================

- Don't pull closed tickets from Bitbucket. (#4)

- Enhanced documentation.


0.2 (2016-01-13)
================

- Add GitHub as issue source. (#3)


0.1 (2015-04-08)
================

initial release

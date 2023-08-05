================================
The gocept.bbissues distribution
================================

.. caution::

    This package is no longer maintained. In case of any interest on it, please
    contact gocept.

Collect open issues from multiple bitbucket or github repositories and generate
a nice html page or a file with json information about your projects.

This package is compatible with Python version 3.6, 3.7 and 3.8.

Installation
============

Install the package using PIP::

    $ pip install gocept.bbissues


Configuration
=============

You have to provide a config file with the following content::

    [config]
    log = issues.log
    html_export_path = export.html
    json_export_path = export.json
    # The next line is optional it defaults to index.jj2 in the package
    template_path = template.jj2


    [bitbucket]
    # The owner always has to be provided. All projects by this owner
    # will be collected.
    owner = owner
    # Specific projects may be provided in the following way
    projects = owner:project1
               owner:project2

    [github]
    # The owner always has to be provided. All projects by this owner
    # will be collected.
    owner = owner
    # Specific projects may be provided in the following way
    projects = owner:project1
               owner:project2


The template will be rendered using jinja2, and could have the following content::

    {% for project in projects %}
        <h2>{{project.name}}</h2>
        {% for issue in project.issues %}
            <h3>{{issue.title}}</h3>
             <pre>
             {{issue.title}}
             {{issue.content}}
             {{issue.status}}
             {{issue.created}}
             {{issue.priority}}
             {{issue.url}}
             {{issue.author}}
             </pre>
        {% endfor %}
    {% endfor %}


Usage
=====

Call it using::

    $ <path to bin directory>/bbissues --config <path to config file>

It saves the generated HTML to the file specified in config.

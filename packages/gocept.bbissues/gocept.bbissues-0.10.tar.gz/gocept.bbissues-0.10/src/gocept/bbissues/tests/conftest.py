
import gocept.bbissues.bbissues
import pytest


TESTING_CONFIG = 'src/gocept/bbissues/tests/testing.cfg'


DUMMY_PROJECTS = [{
    'name': 'gocept.amqprun',
    'issues':
  [{'status': u'new',  # noqa: E131
    'priority': u'major',
    'created': '2015-02-24 11:07',
    'url': 'https://bitbucket.org/gocept/gocept.amqprun/issues/3',
    'author': u'Michael Howitz',
    'content':
    u'Christian Stefanescu wrote:\r\n\r\n> Would it be possible to avoid making sudo calls in unit tests? For instance by adding the rabbit user over http?',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Avoid sudo calls in tests.',
    'prioclass': 'danger'},
   {'status': u'new',
    'priority': u'major',
    'created': '2015-01-20 15:14',
    'url': 'https://bitbucket.org/gocept/gocept.amqprun/issues/2',
    'author': u'Michael Howitz',
    'content':
    u'Migrated from issue of @wosc at https://projects.gocept.com/issues/8218',
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Use vhosts for test isolation',
    'prioclass': 'danger'},
   {'status': u'new',
    'priority': u'major',
    'created': '2015-01-20 15:12',
    'url': 'https://bitbucket.org/gocept/gocept.amqprun/issues/1',
    'author': u'Michael Howitz',
    'content':
    u'migrated from https://projects.gocept.com/issues/10178 (Discussion of the issue see there.)\r\n\r\n@EnTeQuAk wrote (translated by @icemac):\r\n\r\nAMQP 0-8 is deprecated. Even though it is still supported it is no longer updated.  An update to 0-9-1 puts the package up to date as long there is no AMQP 1.0.\r\n\r\nInfos:\r\n\r\n* http://www.rabbitmq.com/amqp-0-8-to-0-9-1.html\r\n* http://www.rabbitmq.com/specification.html\r\n\r\nIn 0-9-1 many things are more strict and better defined thus easing the implementation.',  # noqa: E501
    'comment_count': 5,
    'title': u'AMQP 0-9-1',
    'prioclass': 'danger'},
   {'status': u'new',
    'priority': u'major',
    'created': '2016-04-25 10:18',
    'url': 'https://bitbucket.org/gocept/gocept.amqprun/issues/7',
    'author': u'Thomas Lotze',
    'content':
    u"Currently, it is not clearly readable how, when and why errors are handled and transactions are committed or aborted when a message handler is run. Responsibility for aborting transaction on errors and sending any error responses should be clearly given to the worker while the handlers should be concerned with creating messages only. To get rid of the responsibility of handling the set of response messages, two sets of response messages should be introduced that work similarly to stdout/stderr.\r\n\r\nThe logic would then be:\r\n\r\n* If an exception is raised by the handler, don't send any messages and abort the transaction (which causes a retry upon next channel switch).\r\n\r\n* If any error messages are returned, abort the transaction, then acknowledge the message and send the error messages (under a transaction that is then committed).\r\n\r\n* Otherwise, send any response messages and commit the transaction.\r\n\r\nThis would us allow to get rid of the IResponse interface and treat the different handlers in a more uniform way. Also, the session needs to be considered since it is currently responsible for acknowledging messages.",  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Clean up control flow and transaction handling',
    'prioclass': 'danger'}],
    'pullrequests':
  [{'status': u'OPEN',
    'priority': 'pullrequest',
    'created': '2016-06-06 09:17',
    'url': 'https://bitbucket.org/gocept/gocept.amqprun/pull-requests/1',
    'author': u'Steffen Allner',
    'content':
    u'To speak the AMQP 0-9-1 we have essentially updated the underlying software library provided by rabbitmq (pika to 0.10.0). As a result we also need a new library for testing that speaks this version of AMQP (`amqp` instead of `amqplib`).\r\n\r\nMajor changes have been necessary to adapt to the new callback style synchronous programming pattern, including the ability to test it. We do not use `asyncore` as ioloop anymore, but `select` in general and `epoll` on linux machines instead. This should also ensure forward compatibility as `asyncore` is not supported anymore since pika 0.10.0.\r\n\r\nAs credentials, the port number of the RabbitMQ server can also be specified.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Use amqp 0-9-1',
    'prioclass': 'primary'}]},
 {'name': 'gocept.selenium',
  'issues':
  [{'status': u'new',
    'priority': u'major',
    'created': '2016-06-09 09:36',
    'url': 'https://bitbucket.org/gocept/gocept.selenium/issues/2',
    'author':
    u'Michael Howitz',
    'content':
    u'According to the [Firefox 47 release notes](https://www.mozilla.org/en-US/firefox/47.0/releasenotes/#known) there might be problems with the Selenium WebDriver.\r\n\r\nThey suggest to use the Marionette WebDriver instead.\r\n\r\nIt would be nice if gocept.selenium could support it, too.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Support Marionette WebDriver',
    'prioclass': 'danger'}],
  'pullrequests': []},
 {'name': 'ajja',
  'issues':
  [{'status': u'open',
    'priority': None,
    'created': '2016-06-16 12:31',
    'url': u'https://github.com/gocept/ajja/pull/56',
    'author':
    u'greenkeeperio-bot',
    'content':
    u'Hello lovely humans,\n\n**welcome to automated dependency management with [Greenkeeper](https://greenkeeper.io)**.\nTo take full advantage of this service I recommend to start out with up-to-date dependencies.\n\nI just **updated all the dependencies in the `package.json`** file in one go.\nPlease look into these changes and make sure your project still works with them applied.\nIf you can\u2019t update everything right now that\u2019s fine as well.\nWe\u2019ll get there over time.\n\nNow that you told me to monitor this project **I\u2019ll create a branch for every dependency update**, with the new version applied. The branch creation should trigger your testing services to check the new version. Using the results of these tests I\u2019ll try to open meaningful and helpful pull requests, so your dependencies remain working and up-to-date.\n\n```diff\n-  "underscore": "^1.6.0"\n+  "underscore": "^1.7.0"\n```\n\nIn the above example you can see an in-range update. `1.7.0` is included in the old `^1.6.0` range, because of the [caret `^` character ](https://docs.npmjs.com/misc/semver#ranges).\nWhen there is a failure reported for the update I\u2019ll create a pull request so you know about the problem immediately. When it reports success I\u2019ll delete the branch again, because no action needs to be taken \u2013 everything is fine.\n\nThis way every single version update of your dependencies will either continue to work with your project, or you\u2019ll get to know of potential problems immediately :sparkles:\n\n```diff\n-  "lodash": "^3.0.0"\n+  "lodash": "^4.0.0"\n```\n\nIn this example the new version `4.0.0` is not included in the old `^3.0.0` range.\nFor version updates like these \u2013 let\u2019s call them \u201cout of range\u201d updates \u2013 you\u2019ll receive a pull request right away.\n\nNow **you no longer need to check for exciting new versions by hand** \u2013 I\u2019ll just let you know automatically.\nAnd the pull request will not only serve as a reminder to update. In case it passes your decent test suite that\u2019s a strong reason to merge right away :shipit:\n\nAre you unsure about how things are supposed to work?\n\nThere is a collection of [frequently asked questions](https://greenkeeper.io/faq.html) and of course you may always [ask my humans](https://github.com/greenkeeperio/greenkeeper/issues/new).\n\nGood luck with your project and see you soon :sparkles:\n\n:palm_tree:\n\n---\nThis pull request was created by [greenkeeper.io](https://greenkeeper.io/).\n\n<sub>Tired of seeing this sponsor message? :zap: `greenkeeper upgrade`</sub>',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'Update all dependencies \U0001f334',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-03-18 11:17',
    'url': u'https://github.com/gocept/ajja/issues/55',
    'author': u'florianpilz',
    'content':
    u'After implementing #25 it would be great to keep auto-validation, even though the object is only stored after sending the complete form. We should make it possible to provide validation rules inside the options of each field, so `ajja` can validate the field without talking to the client.\r\n\r\nOf course, this excludes validation among several fields. But we could add that in the future if it does not add too much complexity.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Allow client-only input validation',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-03-18 11:06',
    'url': u'https://github.com/gocept/ajja/issues/54',
    'author': u'florianpilz',
    'content':
    u'The latest documentation is missing, how I can change the order of input fields. By default it will use the order given by the AJAX request. But I can also name all fields inside the form template to decide which fields are displayed in what order. Since this is a common use case, we should document that.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Document how to change the order of input fields',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-03-18 11:02',
    'url': u'https://github.com/gocept/ajja/issues/53',
    'author': u'florianpilz',
    'content':
    u'Say I have a multiple forms which also require the user to input a credit card. Thus I made a template for credit cards, which consists of 4 Input fields side-by-side (since a credit card has 4 groups with 4 numbers each).\r\n\r\nThe type of the input field is a string, so the default template is just a single input field. To use my special template for credit cards, I currently have to explicitly declare the usage for **every** form. But since it is the same concept in all forms, I made sure the field is always named `credit_card`. Thus in all forms the credit card field has the id `field-credit_card`.\r\n\r\nIt would be great if I could register the template in a way, that it is automatically used for every field that is named `field-credit_card`, no matter which type this field has. (Of course, declaring another template in the form options will override the global registration by field name).',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title':
    u'Also allow registration of templates using the #id (preferred over registration by type)',  # noqa: E501
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-03-18 10:54',
    'url': u'https://github.com/gocept/ajja/issues/52',
    'author': u'florianpilz',
    'content':
    u'A great addition to `ajja` would be to describe a template for a single field inline, i.e. inside the form template like this (`field-custom`):\r\n\r\n    <script id="form-template" type="text/x-template">\r\n        <form method="POST" action="{{action}}" id="{{form_id}}">\r\n          <div id="field-subject"></div>\r\n          <div id="field-body"></div>\r\n          <div id="field-custom">\r\n            <textarea cols="80" rows="15" data-bind="value: {{name}}" name="{{name}}"></textarea>\r\n          </div>\r\n        </form>\r\n    </script>\r\n\r\nThis way I avoid the overhead to define a template and to define it\'s use for `field-custom` inside the options by expressing it via the HTML structure. This would be a burden for a template that is used just once.\r\n\r\nOf course, if I want to reuse the template, it must be extracted from the form.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title':
    u'Make it possible to write widget templates inside the form template',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-03-18 10:01',
    'url': u'https://github.com/gocept/ajja/issues/51',
    'author': u'sweh',
    'content':
    u'Currently, gocept.jsform looks for an input field (usually hidden) with the id csrf_token to find the csrf_token which will the be send with every save request.\r\n\r\nThe user needs to append this hidden input by himself. A better approach would be to filter the csrf_token from the initial form data and render the necessary hidden input field automatically.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u' Refactor CSRF token behaviour',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-03-15 10:49',
    'url': u'https://github.com/gocept/ajja/issues/49',
    'author': u'sweh',
    'content':
    u'In order to get the Form-API more REST friendly, the save_url parameter should be replaced with a generic url parameter for save and load of data.\r\n\r\nFor backwards compatibility, the first parameter to the Form.load() function should stay as is (`data or url`), except that providing a url as data *and* a url in options should result in an error.\r\n\r\nIf data is provided directly, url must be provided in the options.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Remove distinction between `url` and `save_url`',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-02-12 11:00',
    'url': u'https://github.com/gocept/ajja/issues/47',
    'author': u'florianpilz',
    'content':
    u'Currently `JSForm` expects an ID without `#` (`form`), but `ListWidget` expects an ID with `#` (`#form`).',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Unify ID handling of JSForm and ListWidget',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-02-10 13:33',
    'url': u'https://github.com/gocept/ajja/issues/46',
    'author': u'florianpilz',
    'content':
    u"It's not a very catchy name and strongly coupled with our company.\r\n\r\nThoughts so far:\r\n\r\n* Bread (from BREAD, an alternative acronym of CRUD)\r\n* Slime (since CRUD means dirt and dirt leads to ...)\r\n* It should be clear how to write the name when hearing it.\r\n* It should somehow contain or undermine the basic idea of the library. So best start with 1 sentence describing the library and find a name starting at that sentence.\r\n* The name should be unique, so ranking high in Google is easy and we do not compete with usual nouns.",  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Rename gocept.jsform',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-02-10 13:30',
    'url': u'https://github.com/gocept/ajja/issues/45',
    'author': u'florianpilz',
    'content':
    u'Bootstrap is used for modal dialogs. We are not sure about jQuery UI, maybe the styling used for the accordion. We should definitely get rid of those dependencies and provide easy solutions instead. For example the form should render below the `ListWidget` rather using a modal etc.',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'Remove dependency to Bootstrap and jQuery UI',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-01-08 08:46',
    'url': u'https://github.com/gocept/ajja/issues/44',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nDue to changing to a new version of Jasmine we had to rewrite all async tests. To get back to a green bar we took the shortcut and often replaced ``runs`` and ``waitsFor`` with stupid ``setTimeout`` blocks that will wait for 100ms rather waiting at most 100ms. This slows down 30% of all tests.\n\nTo speed up tests again, we should try to replace those blocks with proper event handlers, i.e. ``expect`` and ``done`` are called inside an event handler that waits for the previous action to be completed. It might be required to inject more events for testing.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/44',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Replace setTimeout in tests by waiting for events',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-09 09:29',
    'url': u'https://github.com/gocept/ajja/issues/41',
    'author': u'sweh',
    'content':
    u'Originally reported by: **sweh (Bitbucket: [sweh](http://bitbucket.org/sweh), GitHub: [sweh](http://github.com/sweh))**\n\n----------------------------------------\n\nThe list widget e.g. has the ID `container`, which makes it not reusable on a single page.\n\nEither make the ID configurable or use class names instead.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/41',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Make IDs of default templates configurable',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-09 08:55',
    'url': u'https://github.com/gocept/ajja/issues/40',
    'author': u'sweh',
    'content':
    u'Originally reported by: **sweh (Bitbucket: [sweh](http://bitbucket.org/sweh), GitHub: [sweh](http://github.com/sweh))**\n\n----------------------------------------\n\nThere is some (old) documentation in README.txt and on some methods in code.\n\nWe should write up documentation (with Spinx) and publish it to readthedocs.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/40',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'Documentation',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-09 08:53',
    'url': u'https://github.com/gocept/ajja/issues/39',
    'author': u'sweh',
    'content':
    u'Originally reported by: **sweh (Bitbucket: [sweh](http://bitbucket.org/sweh), GitHub: [sweh](http://github.com/sweh))**\n\n----------------------------------------\n\nThose widgets are barely to not tested.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/39',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'Write tests for list-, table- and groupwidget',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 08:23',
    'url': u'https://github.com/gocept/ajja/issues/37',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently the width of the modal dialog is fixed. Therefore longer labels overlap the input field. Maybe we can / want adjust the width automatically, depending on the length of the label?\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/37',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'ListWidget: Adjust width of modal dialog to label',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 08:22',
    'url': u'https://github.com/gocept/ajja/issues/36',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently nothing happens.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/36',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'ListWidget: Close modal dialog on ENTER',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 08:11',
    'url': u'https://github.com/gocept/ajja/issues/35',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently `gocept.jsform` is fully localized, but ListWidget is not. We should provide the same API and translate all texts currently available.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/35',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'ListWidget: Add localization as used in `Form`',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 08:09',
    'url': u'https://github.com/gocept/ajja/issues/34',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nThe options that can be given into `__init__` are already somewhat documented. However, everything concerning `data` attributes is not documented at all. In the ListWidget, this is used to define which template is used for the list items, which title is displayed in the modal and so on. This must be documented.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/34',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'ListWidget: Document API available via data attributes',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 07:58',
    'url': u'https://github.com/gocept/ajja/issues/31',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently the class `add` is applied to the button, but this is way too general and might interfere with existing CSS.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/31',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'ListWidget: Adjust class of button to add new list entries',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 07:53',
    'url': u'https://github.com/gocept/ajja/issues/29',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nThe JS library https://harvesthq.github.io/chosen provides really good looking select widgets that can search through available options. It also fits in nicely with Bootstrap. The question is whether we want to incorporate another JS library into the core of `gocept.jsform` and provide this "superior" select as default. Or if we want to stay bare bones and keep the usual HTML select widget.\n\nIntegration is really easy, just call `$(\'#field-to_recipient select\').chosen({width: \'100%\'});` on a select template.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/29',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'Searchable select fields via Chosen',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 07:29',
    'url': u'https://github.com/gocept/ajja/issues/28',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nIn one project we have used Dropzone to upload files. Each file generates a list entry in ListWidget, thus additional information can be displayed / edited. This seems to be so useful, we should consider integrating it into `gocept.jsform`.\n\nOur template inside the project:\n\n\n```\n#!HTML\n\n<div class="field form-group">\n  <label class="col-sm-3 control-label">Dokumente</label>\n  <div class="col-sm-9">\n    <div id="documents-list"\n         data-collection-url="${documents_collection_url}"\n         data-template="document-item"\n         data-form-template="document-edit"\n         data-form-options=\'{\n           "title": {"label": "Titel"},\n           "category_id": {\n             "label": "Kategorie",\n             "source": ${category_source}}\n         }\'\n         data-modal-title="Dokument bearbeiten">\n    </div>\n    <div id="upload" class="dropzone" tal:condition="not view.readonly">\n      <div class="dz-message">Bitte Dateien hier ablegen.</div>\n    </div>\n  </div>\n</div>\n```\n\nAnd JS to set it up:\n\n\n```\n#!javascript\n\nvar widget, dropzone;\nwidget = new gocept.jsform.ListWidget($(\'#documents-list\'), {\n    default_form_actions: []\n});\nwidget.load();\n\nDropzone.autoDiscover = false;\ndropzone = new Dropzone(\'#upload\', {\n  \'url\': \'${upload_url}\',\n  \'headers\': {\n    \'X-CSRF-Token\': $(\'#csrf_token\').val()\n  }\n});\ndropzone.on(\'success\', function (file, response) {\n  widget.render_item(response);\n  dropzone.removeFile(file);\n});\n```\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/28',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'ListWidget: Provide file upload widget using Dropzone',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 07:21',
    'url': u'https://github.com/gocept/ajja/issues/27',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nWe should separate the `save_url` into `save_url` and `autosave_url`. The former is called when submitting the form and the latter is used for autosave using a JSON API. This is important for some use cases like sending an e-mail based on form input, since that triggers a completely different action.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/27',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Make it possible to distinct autosave and form submit',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 07:20',
    'url': u'https://github.com/gocept/ajja/issues/26',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nWhen using a form with a save button, you currently have to manually check that all fields were successfully saved before submitting the form. It would be great if `gocept.jsform` provides a custom save button, that by itself calls `save_remaining` and waits for successful responses.\n\nThere already is some support build into `gocept.jsform` to do so, but the integration must be done manually in each project. Very cumbersome, since this behaviour is needed in almost any form. (When typing into an input field and clicking save before it lost focus you need to make sure the filed was saved before performing the submit.)\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/26',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title':
    u'Add save button to form that waits for server side validation before send',  # noqa: E501
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:57',
    'url': u'https://github.com/gocept/ajja/issues/25',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently the form always uses autosave, thus you must adjust your model to not contain required fields to use `gocept.jsform`. This is not very programmer-friendly. We should also allow to disable autosave, thus a save button is used to submit the form.\n\nThe approach to use no autosave is very helpful when all options and values are given up front, rather relying on a JSON API on server side. Maybe we should render the save button automatically when autosave is disabled.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/25',  # noqa: E501
    'comment_count': 2,
    'type': 'Issue',
    'title': u'Make autosave optional',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:54',
    'url': u'https://github.com/gocept/ajja/issues/24',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nWe extracted the ListWidget to create a list of elements, which can render a form each using a modal dialog. However the concept greatly differs from `gocept.jsform`: Rather having good default options for almost anything, the ListWidget requires you to give all information up front. To be more specific: Only fields that have a given label are shown.\n\nWe should unify the approach used, so both (`gocept.jsform` and `ListWidget`) use progressive enhancements.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/24',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Use progressive enhancement for ListWidget',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:31',
    'url': u'https://github.com/gocept/ajja/issues/22',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently some configuration is supplied via the options dict when creating an instance of `gocept.jsform`, other options are read from the template via data-attributes.\n\nIt would be nice if all widget specific configuration can be done both ways, thus `gocept.jsform` has to check the options dict and the data-attributes of the template. The documentation should tell that both ways are supported and which is preferred if both are given.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/22',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Allow widget configuration via options dict and data attribute',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:27',
    'url': u'https://github.com/gocept/ajja/issues/21',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently `save_remaining` triggers a save event for each field and also displays an error message for each field. Maybe that could be optimized to save all fields in a single request.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/21',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title':
    u'`save_remaining` should save all remaining fields in 1 requests rather multiple',  # noqa: E501
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:25',
    'url': u'https://github.com/gocept/ajja/issues/20',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nWhen overwriting the default form template, it would be of help if we could say "insert all input fields here" rather listing them one by one. The same goes for "insert all actions here".\n\nThis is helpful, since the inputs are added to the bottom by default. So a form with a save button would have the input fields below the save button, except all input fields are listed one by one above the save button.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/20',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Placeholder for all inputs / actions',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:22',
    'url': u'https://github.com/gocept/ajja/issues/19',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nOnly the template `gocept_jsform_templates_string.pt` has the Bootstrap class `form-control`. But this class should be on other templates, too. Like textarea for example. Before we become framework agnostic, we should at least become framework compatible.\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/19',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Add Bootstrap classes to remaining templates',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2015-12-04 06:18',
    'url': u'https://github.com/gocept/ajja/issues/18',
    'author': u'sweh',
    'content':
    u'Originally reported by: **Florian Pilz (Bitbucket: [florianpilz](http://bitbucket.org/florianpilz), GitHub: [florianpilz](http://github.com/florianpilz))**\n\n----------------------------------------\n\nCurrently we are using a custom template to add the CSRF token to the body via a hidden template. Even though this specific need may be eliminated by #17, there are use cases where you want to supply additional body fields that are not visible to the user.\n\nTherefore the core should provide a hidden template, rather doing it anew in every application.\n\n\n```\n#!html\n\n<script id="hidden-template" type="text/x-template">\n    <input type="hidden" name="{{name}}" data-bind="value:{{name}}" />\n</script>\n```\n\n----------------------------------------\n- Bitbucket: https://bitbucket.org/gocept/gocept.jsform/issue/18',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Provide template for hidden input values',
    'prioclass': None}],
  'pullrequests':
  [{'status': u'open',
    'priority': None,
    'created': '2016-06-16 12:31',
    'url': u'https://github.com/gocept/ajja/pull/56',
    'author': u'greenkeeperio-bot',
    'content':
    u'Hello lovely humans,\n\n**welcome to automated dependency management with [Greenkeeper](https://greenkeeper.io)**.\nTo take full advantage of this service I recommend to start out with up-to-date dependencies.\n\nI just **updated all the dependencies in the `package.json`** file in one go.\nPlease look into these changes and make sure your project still works with them applied.\nIf you can\u2019t update everything right now that\u2019s fine as well.\nWe\u2019ll get there over time.\n\nNow that you told me to monitor this project **I\u2019ll create a branch for every dependency update**, with the new version applied. The branch creation should trigger your testing services to check the new version. Using the results of these tests I\u2019ll try to open meaningful and helpful pull requests, so your dependencies remain working and up-to-date.\n\n```diff\n-  "underscore": "^1.6.0"\n+  "underscore": "^1.7.0"\n```\n\nIn the above example you can see an in-range update. `1.7.0` is included in the old `^1.6.0` range, because of the [caret `^` character ](https://docs.npmjs.com/misc/semver#ranges).\nWhen there is a failure reported for the update I\u2019ll create a pull request so you know about the problem immediately. When it reports success I\u2019ll delete the branch again, because no action needs to be taken \u2013 everything is fine.\n\nThis way every single version update of your dependencies will either continue to work with your project, or you\u2019ll get to know of potential problems immediately :sparkles:\n\n```diff\n-  "lodash": "^3.0.0"\n+  "lodash": "^4.0.0"\n```\n\nIn this example the new version `4.0.0` is not included in the old `^3.0.0` range.\nFor version updates like these \u2013 let\u2019s call them \u201cout of range\u201d updates \u2013 you\u2019ll receive a pull request right away.\n\nNow **you no longer need to check for exciting new versions by hand** \u2013 I\u2019ll just let you know automatically.\nAnd the pull request will not only serve as a reminder to update. In case it passes your decent test suite that\u2019s a strong reason to merge right away :shipit:\n\nAre you unsure about how things are supposed to work?\n\nThere is a collection of [frequently asked questions](https://greenkeeper.io/faq.html) and of course you may always [ask my humans](https://github.com/greenkeeperio/greenkeeper/issues/new).\n\nGood luck with your project and see you soon :sparkles:\n\n:palm_tree:\n\n---\nThis pull request was created by [greenkeeper.io](https://greenkeeper.io/).\n\n<sub>Tired of seeing this sponsor message? :zap: `greenkeeper upgrade`</sub>',  # noqa: E501
    'comment_count': 1,
    'type': 'Issue',
    'title': u'Update all dependencies \U0001f334',
    'prioclass': None}]},
 {'name': 'zodb.py3migrate',
  'issues':
  [{'status': u'open',
    'priority': None,
    'created': '2016-06-20 15:24',
    'url': u'https://github.com/gocept/zodb.py3migrate/issues/4',
    'author':
    u'icemac',
    'content': u'',
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Commit transaction after converting',
    'prioclass': None},
   {'status': u'open',
    'priority':
    None,
    'created': '2016-06-08 15:02',
    'url': u'https://github.com/gocept/zodb.py3migrate/issues/3',
    'author':
    u'icemac',
    'content':
    u'Together with the --start and --limit options introduced to fix #2 it would be nice to see the OIDs of the objects which need to be converted in the output.',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Render OIDs in verbose mode.',
    'prioclass': None},
   {'status': u'open',
    'priority': None,
    'created': '2016-05-20 11:26',
    'url': u'https://github.com/gocept/zodb.py3migrate/issues/1',
    'author': u'icemac',
    'content':
    u'Even though the number of objects in the FileStorage is only an approximate a progress bar would be nicer than the current output.\r\n\r\nSuggestion: Use https://pypi.python.org/pypi/tqdm',  # noqa: E501
    'comment_count': 0,
    'type': 'Issue',
    'title': u'Use progress bar',
    'prioclass': None}],
  'pullrequests': []}]


@pytest.yield_fixture
def dummy_handler(monkeypatch):
    Handler = gocept.bbissues.bbissues.Handler

    def get_mocked_projects(self):
        return DUMMY_PROJECTS

    monkeypatch.setattr(Handler, 'get_projects', get_mocked_projects)
    # Handler.get_projects = mock.MagicMock()
    # Handler.get_projects.return_value = DUMMY_PROJECTS
    handler = Handler(TESTING_CONFIG)
    yield handler

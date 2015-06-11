# coding=utf-8
# unittest-jasmine
# Copyright (C) 2015 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
"""
This module contains classes representing the items of a test suite tree, as
returned by the first line output by ``runner.js``.

Use :func:`parse` to convert the first line to a structured representation of
the tests.
"""

import contextlib


class JasmineData(object):
    """The base class for *Jasmine* specs and suites.
    """
    def __init__(self, id, name, description):
        self._id = id
        self._name = name
        self._description = description
        self._result = {}

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.id == other.id \
            and self.name == other.name \
            and self.description == other.description

    def __str__(self):
        return '%s %s <%s>' % (self.TYPE, self.name, self.id)

    @property
    def id(self):
        """The item ID."""
        return self._id

    @property
    def name(self):
        """The item name."""
        return self._name

    @property
    def description(self):
        """The item description."""
        return self._description

    @property
    def result(self):
        """The result of this event as read from the output stream; this is set
        after :meth:`running` has completed successfully"""
        return self._result

    def running(self, jasmine):
        """Return a context manager that ensures that the event stream is
        correct.

        :param unittest_jasmine.runner.Jasmine jasmine: The runner from which
        to load events.

        :return: a context manager
        """
        @contextlib.contextmanager
        def context():
            self.verify_started(next(jasmine))
            yield self
            result = next(jasmine)
            self.verify_done(result)
            self._result = result
        return context()

    def _verify(self, expected_event, actual_event, data):
        """Verifies that and event is of the expected type, and that the
        ``'id'`` field of ``data`` equals :attr:`id`.

        :param str expected_event: The expected event name.

        :param str actual_event: The actual event name.

        :param dict data: The actual data of the event.

        :raises RuntimeError: if any data is incorrect
        """
        if expected_event != actual_event:
            raise RuntimeError(
                'expected event %s, found %s',
                expected_event, actual_event)
        if not data:
            raise RuntimeError('no event data provided')
        if self.id != data.get('id'):
            raise RuntimeError(
                'expected id %s, found %s',
                self.id, data.get('id'))

    def verify_started(self, o):
        """Verifies that an event object corresponds to the *started* event.

        :param dict o: The event object.

        :raises RuntimeError: if any data is incorrect
        """
        self._verify(self.TYPE + 'Started', o.get('event'), o.get('data'))

    def verify_done(self, o):
        """Verifies that an event object corresponds to the *done* event.

        :param dict o: The event object.

        :raises RuntimeError: if any data is incorrect
        """
        self._verify(self.TYPE + 'Done', o.get('event'), o.get('data'))


class JasmineSpec(JasmineData):
    """A *Jasmine* test spec.
    """
    TYPE = 'spec'


class JasmineSuite(JasmineData):
    TYPE = 'suite'

    def __init__(self, children, *args, **kwargs):
        super(JasmineSuite, self).__init__(*args, **kwargs)
        self._children = children

    def __eq__(self, other):
        return super(JasmineSuite, self).__eq__(other) \
            and all(s == o for s, o in zip(self.children, other.children))

    @property
    def children(self):
        """The suite child items; this is a sequence of specs and suites."""
        return self._children


def parse(item, spec=JasmineSpec, suite=JasmineSuite, **kwargs):
    """Parses a ``dict`` into a suite or a spec.

    :param dict item: The item to parse.

    :param callable spec: The spec generating function. This ust be compatible
        with the :class:`JasmineSpec` constructor.

    :param callable suite: The suite generating function. This must be
        compatible with the :class:`JasmineSuite` constructor.

    :param kwargs: Any keyword arguments to pass to the spec and suite
        generating functions.

    :raises ValueError: if ``item['type']`` is invalid

    :raises KeyError: if a required value if missing from ``item``
    """
    item_type = item['type']
    item_id = item['id']
    item_name = item['fullName']
    item_description = item['description']

    if item_type == JasmineSpec.TYPE:
        return spec(
            item_id,
            item_name,
            item_description,
            **kwargs)

    elif item_type == JasmineSuite.TYPE:
        item_children = item['children']
        return suite(
            [parse(i, spec, suite, **kwargs) for i in item_children],
            item_id,
            item_name,
            item_description,
            **kwargs)

    else:
        raise ValueError('unknown type: %s', item_type)

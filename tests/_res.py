import os
import unittest_jasmine


#: The expected output from the test
TEST_OUTPUT = (
    {'type': 'suite', 'children': [
        {'description': 'TestRunner', 'type': 'suite', 'children': [
            {'description': 'spec 1', 'type': 'spec'},
            {'description': 'inner suite', 'type': 'suite', 'children': [
                {'description': 'inner spec 1', 'type': 'spec'},
                {'description': 'inner spec 2', 'type': 'spec'}]},
            {'description': 'spec 2', 'type': 'spec'}]}]},
    {'event': 'suiteStarted', 'data': {
        'description': 'TestRunner'}},
    {'event': 'specStarted', 'data': {
        'description': 'spec 1'}},
    {'event': 'specDone', 'data': {
        'description': 'spec 1', 'status': 'failed'}},
    {'event': 'suiteStarted', 'data': {
        'description': 'inner suite'}},
    {'event': 'specStarted', 'data': {
        'description': 'inner spec 1'}},
    {'event': 'specDone', 'data': {
        'description': 'inner spec 1', 'status': 'passed'}},
    {'event': 'specStarted', 'data': {
        'description': 'inner spec 2'}},
    {'event': 'specDone', 'data': {
        'description': 'inner spec 2', 'status': 'failed'}},
    {'event': 'suiteDone', 'data': {
        'description': 'inner suite', 'status': 'finished'}},
    {'event': 'specStarted', 'data': {
        'description': 'spec 2'}},
    {'event': 'specDone', 'data': {
        'description': 'spec 2', 'status': 'passed'}},
    {'event': 'suiteDone', 'data': {
        'description': 'TestRunner', 'status': 'finished'}})


def output(**options):
    """A generator that yields the relevant output from the test run"""
    return unittest_jasmine.runner.jasmine(
        os.path.dirname(__file__),
        os.path.join('res', 'test-runner.js'),
        **options)

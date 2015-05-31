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


#: A test suite definition
SUITE_DEFINITION = {
    'type': 'suite',
    'id': 'suite0',
    'fullName': 'Suite 0',
    'description': 'This is Suite 0',
    'children': [
        {
            'type': 'suite',
            'id': 'suite1',
            'fullName': 'Suite 1',
            'description': 'This is Suite 1',
            'children': [
                {
                    'type': 'spec',
                    'id': 'spec0',
                    'fullName': 'Spec 0',
                    'description': 'This is spec 0'
                },
                {
                    'type': 'spec',
                    'id': 'spec1',
                    'fullName': 'Spec 1',
                    'description': 'This is spec 1'}]},
        {
            'type': 'spec',
            'id': 'spec2',
            'fullName': 'Spec 2',
            'description': 'This is spec 2'}]}


def output(**options):
    """A generator that yields the relevant output from the test run"""
    return unittest_jasmine.runner.jasmine(
        os.path.dirname(__file__),
        os.path.join('res', 'test-runner.js'),
        **options)

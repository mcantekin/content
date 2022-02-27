import pytest

from CrowdStrikeFalconX import Client, \
    send_uploaded_file_to_sandbox_analysis_command, send_url_to_sandbox_analysis_command, \
    get_full_report_command, get_report_summary_command, get_analysis_status_command, \
    check_quota_status_command, find_sandbox_reports_command, find_submission_id_command, run_polling_command, \
    pop_polling_related_args, is_new_polling_search, arrange_args_for_upload_func, remove_polling_related_args, \
    DBotScoreReliability, parse_indicator
from TestsInput.context import SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_CONTEXT, SEND_URL_TO_SANDBOX_ANALYSIS_CONTEXT, \
    GET_FULL_REPORT_CONTEXT, GET_REPORT_SUMMARY_CONTEXT, GET_ANALYSIS_STATUS_CONTEXT, CHECK_QUOTA_STATUS_CONTEXT, \
    FIND_SANDBOX_REPORTS_CONTEXT, FIND_SUBMISSION_ID_CONTEXT, MULTIPLE_ERRORS_RESULT, GET_FULL_REPORT_CONTEXT_EXTENDED
from TestsInput.http_responses import SEND_UPLOADED_FILE_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE, \
    SEND_URL_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE, GET_FULL_REPORT_HTTP_RESPONSE, GET_REPORT_SUMMARY_HTTP_RESPONSE, \
    CHECK_QUOTA_STATUS_HTTP_RESPONSE, FIND_SANDBOX_REPORTS_HTTP_RESPONSE, FIND_SUBMISSION_ID_HTTP_RESPONSE, \
    GET_ANALYSIS_STATUS_HTTP_RESPONSE, MULTI_ERRORS_HTTP_RESPONSE, NO_ERRORS_HTTP_RESPONSE, \
    GET_FULL_REPORT_HTTP_RESPONSE_EMPTY


class ResMocker:
    def __init__(self, http_response):
        self.http_response = http_response
        self.ok = False

    def json(self):
        return self.http_response


SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_ARGS = {
    "sha256": "sha256",
    "environment_id": "160: Windows 10",
    "action_script": "",
    "command_line": "",
    "document_password": "",
    "enable_tor": "false",
    "submit_name": "",
    "system_date": "",
    "system_time": ""
}

SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_ARGS_POLLING = {
    "sha256": "sha256",
    "environment_id": "160: Windows 10",
    "action_script": "",
    "command_line": "",
    "document_password": "",
    "enable_tor": "false",
    "submit_name": "",
    "system_date": "",
    "system_time": "",
    "polling": True,
    "interval_in_seconds": "60",
    "extended_data": "true"
}

SEND_URL_TO_SANDBOX_ANALYSIS_ARGS = {
    "url": "https://www.google.com",
    "environment_id": "160: Windows 10",
    "enable_tor": "False",
    "action_script": "",
    "command_line": "",
    "document_password": "",
    "submit_name": "",
    "system_date": "",
    "system_time": ""
}

SEND_URL_TO_SANDBOX_ANALYSIS_ARGS_POLLING = {
    "url": "https://www.google.com",
    "environment_id": "160: Windows 10",
    "enable_tor": "False",
    "action_script": "",
    "command_line": "",
    "document_password": "",
    "submit_name": "",
    "system_date": "",
    "system_time": "",
    "polling": "true",
    "interval_in_seconds": "10",
    "extended_data": "true"
}

GET_FULL_REPORT_ARGS = {
    "ids": "ids",
    "extended_data": "false"
}
GET_FULL_REPORT_ARGS_EXTENDED = {
    "ids": "ids",
    "extended_data": "true"
}

GET_REPORT_SUMMARY_ARGS = {
    "ids": "ids",
}

GET_ANALYSIS_STATUS_ARGS = {
    "ids": "ids",
}

FIND_SANDBOX_REPORTS_ARGS = {
    "offset": "",
    "limit": "",
    "sort": "",
    "filter": "",
}

FIND_SUBMISSION_ID_ARGS = {
    "offset": "",
    "limit": "",
    "sort": "",
    "filter": "",
}


@pytest.mark.parametrize('command, args, http_response, context', [
    (get_report_summary_command, GET_REPORT_SUMMARY_ARGS, GET_REPORT_SUMMARY_HTTP_RESPONSE, GET_REPORT_SUMMARY_CONTEXT),
    (get_analysis_status_command, GET_ANALYSIS_STATUS_ARGS, GET_ANALYSIS_STATUS_HTTP_RESPONSE,
     GET_ANALYSIS_STATUS_CONTEXT),
    (check_quota_status_command, {}, CHECK_QUOTA_STATUS_HTTP_RESPONSE, CHECK_QUOTA_STATUS_CONTEXT),
    (find_sandbox_reports_command, FIND_SANDBOX_REPORTS_ARGS, FIND_SANDBOX_REPORTS_HTTP_RESPONSE,
     FIND_SANDBOX_REPORTS_CONTEXT),
    (find_submission_id_command, FIND_SUBMISSION_ID_ARGS, FIND_SUBMISSION_ID_HTTP_RESPONSE, FIND_SUBMISSION_ID_CONTEXT),
])
def test_cs_falconx_commands(command, args, http_response, context, mocker):
    """Unit test
    Given
    - demisto args
    - raw response of the http request
    When
    - mock the http request result
    Then
    - convert the result to human readable table
    - create the context
    - validate the expected_result and the created context
    """
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, '_http_request', return_value=http_response)

    command_results = command(client, **args)
    if not isinstance(command_results, list):  # some command only return a single CommandResults objects
        command_results = [command_results]

    outputs = [cr.to_context()['EntryContext'] for cr in command_results]
    if isinstance(context, dict) and len(outputs) == 1:
        outputs = outputs[0]

    assert outputs == context, ddiff(outputs, context)  # todo remove ddiff


@pytest.mark.parametrize('command, args, http_response, context', [
    (send_uploaded_file_to_sandbox_analysis_command, SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_ARGS,
     SEND_UPLOADED_FILE_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE, SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_CONTEXT),
    (send_url_to_sandbox_analysis_command, SEND_URL_TO_SANDBOX_ANALYSIS_ARGS,
     SEND_URL_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE, SEND_URL_TO_SANDBOX_ANALYSIS_CONTEXT),
    (get_full_report_command, GET_FULL_REPORT_ARGS, GET_FULL_REPORT_HTTP_RESPONSE, GET_FULL_REPORT_CONTEXT),
    (get_full_report_command, GET_FULL_REPORT_ARGS_EXTENDED, GET_FULL_REPORT_HTTP_RESPONSE,
     GET_FULL_REPORT_CONTEXT_EXTENDED)
])
def test_cs_falcon_x_polling_related_commands(command, args, http_response, context, mocker):
    """Unit test
    Given
    - demisto args
    - raw response of the http request
    When
    - mock the http request result
    Then
    - convert the result to human readable table
    - create the context
    - validate the expected_result and the created context
    """
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, '_http_request', return_value=http_response)

    if command == get_full_report_command:
        command_res, status = command(client, **args)
    else:
        command_res = command(client, **args)
    if isinstance(command_res, list):
        assert len(command_res) == 1
    else:
        command_res = [command_res]

    assert command_res[0].outputs == context, ddiff(command_res[0].outputs, context)  # todo remove ddiff


@pytest.mark.parametrize('http_response, output', [
    (MULTI_ERRORS_HTTP_RESPONSE, MULTIPLE_ERRORS_RESULT),
    (NO_ERRORS_HTTP_RESPONSE, "")
])
def test_handle_errors(http_response, output, mocker):
    """Unit test
    Given
    - raw response of the http request
    When
    - there are or there are no errors
    Then
    - show the exception content
    """
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)
    try:
        mocker.patch.object(client._session, 'request', return_value=ResMocker(http_response))
        _, output, _ = check_quota_status_command(client)
    except Exception as e:
        assert (str(e) == str(output))


def ddiff(dict1: dict, dict2: dict):  # todo remove
    if not dict1:
        print('dict1 is empty/None')
        return
    if not dict2:
        print('dict1 is empty/None')
        return

    for k in set(dict1.keys()).intersection(dict2.keys()):
        if dict1[k] != dict2[k]:
            print(f'{k} in dict1:', dict1[k])
            print(f'{k} in dict2:', dict2[k])
    for k in set(dict1.keys()).difference(dict2.keys()):
        print(f'key {k} missing from dict2')
    for k in set(dict2.keys()).difference(dict1.keys()):
        print(f'key {k} missing from dict1')


def test_running_polling_command_success_for_url(mocker):
    """
    Given:
        An upload request of a url or a file using the polling flow, that was already initiated priorly and is now
         complete.
    When:
        When, while in the polling flow, we are checking the status of on an upload that was initiated earlier and is
         already complete.
    Then:
        Return a command results object, without scheduling a new command.
    """
    args = {'ids': "1234", "extended_data": "true"}
    mocker.patch('CommonServerPython.ScheduledCommand.raise_error_if_not_supported')
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, 'send_url_to_sandbox_analysis', return_value=SEND_URL_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE)
    mocker.patch.object(Client, 'get_full_report', return_value=GET_FULL_REPORT_HTTP_RESPONSE)

    expected_outputs = GET_FULL_REPORT_CONTEXT_EXTENDED
    command_results = run_polling_command(client, args, 'cs-fx-submit-url', send_url_to_sandbox_analysis_command,
                                          get_full_report_command, 'URL')
    assert isinstance(command_results, list) and len(command_results) == 1

    print(ddiff(command_results[0].outputs, expected_outputs))  # todo remove
    assert command_results[0].outputs == expected_outputs
    assert command_results[0].scheduled_command is None


def test_running_polling_command_success_for_file(mocker):
    """
    Given:
        An upload request of a url or a file using the polling flow, that was already initiated priorly and is now
         complete.
    When:
        When, while in the polling flow, we are checking the status of on an upload that was initiated earlier and is
         already complete.
    Then:
        Return a command results object, without scheduling a new command.
    """
    args = {'ids': "1234", "extended_data": "true"}
    mocker.patch('CommonServerPython.ScheduledCommand.raise_error_if_not_supported')
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, 'send_url_to_sandbox_analysis', return_value=SEND_URL_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE)
    mocker.patch.object(Client, 'get_full_report', return_value=GET_FULL_REPORT_HTTP_RESPONSE)

    expected_outputs = GET_FULL_REPORT_CONTEXT_EXTENDED
    command_results = run_polling_command(client, args, 'cs-fx-submit-uploaded-file',
                                          send_uploaded_file_to_sandbox_analysis_command,
                                          get_full_report_command, 'FILE')
    assert isinstance(command_results, list) and len(command_results) == 1
    print(ddiff(command_results[0].outputs, expected_outputs))  # todo remove
    assert command_results[0].outputs == expected_outputs
    assert command_results[0].scheduled_command is None


def test_running_polling_command_pending_for_url(mocker):
    """
    Given:
         An upload request of a url or a file using the polling flow, that was already initiated priorly and is not
          completed yet.
    When:
         When, while in the polling flow, we are checking the status of on an upload that was initiated earlier and is
         not complete yet.
    Then:
        Return a command results object, with scheduling a new command.
    """
    args = {'ids': "1234", "extended_data": "true"}
    mocker.patch('CommonServerPython.ScheduledCommand.raise_error_if_not_supported')
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, 'send_url_to_sandbox_analysis', return_value=SEND_URL_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE)
    mocker.patch.object(Client, 'get_full_report', return_value=GET_FULL_REPORT_HTTP_RESPONSE_EMPTY)
    command_results = run_polling_command(client, args, 'cs-fx-submit-url', send_url_to_sandbox_analysis_command,
                                          get_full_report_command, 'URL')
    assert command_results.outputs is None
    assert command_results.scheduled_command is not None


def test_running_polling_command_pending_for_file(mocker):
    """
    Given:
         An upload request of a url or a file using the polling flow, that was already initiated priorly and is not
          completed yet.
    When:
         When, while in the polling flow, we are checking the status of on an upload that was initiated earlier and is
         not complete yet.
    Then:
        Return a command results object, with scheduling a new command.
    """
    args = {'ids': "1234", "extended_data": "true"}
    mocker.patch('CommonServerPython.ScheduledCommand.raise_error_if_not_supported')
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, 'send_url_to_sandbox_analysis', return_value=SEND_URL_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE)
    mocker.patch.object(Client, 'get_full_report', return_value=GET_FULL_REPORT_HTTP_RESPONSE_EMPTY)
    command_results = run_polling_command(client, args, 'cs-fx-submit-uploaded-file',
                                          send_uploaded_file_to_sandbox_analysis_command,
                                          get_full_report_command, 'FILE')
    assert command_results.outputs is None
    assert command_results.scheduled_command is not None


def test_running_polling_command_new_search_for_url(mocker):
    """
    Given:
         An upload request of a url using the polling flow, that was already initiated priorly and is not
          completed yet.
    When:
         When, while in the polling flow, we are checking the status of on an upload that was initiated earlier and is
         not complete yet.
    Then:
        Return a command results object, with scheduling a new command.
    """
    args = SEND_URL_TO_SANDBOX_ANALYSIS_ARGS_POLLING
    mocker.patch('CommonServerPython.ScheduledCommand.raise_error_if_not_supported')
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, 'send_url_to_sandbox_analysis',
                        return_value=SEND_UPLOADED_FILE_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE)
    mocker.patch.object(Client, 'get_full_report', return_value=GET_FULL_REPORT_HTTP_RESPONSE)

    expected_outputs = SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_CONTEXT
    command_results = run_polling_command(client, args, 'cs-fx-submit-url', send_url_to_sandbox_analysis_command,
                                          get_full_report_command, 'URL')

    assert command_results.outputs == expected_outputs
    assert command_results.scheduled_command is not None


def test_running_polling_command_new_search_for_file(mocker):
    """
    Given:
         An upload request of a file  using the polling flow, that was already initiated priorly and is not
          completed yet.
    When:
         When, while in the polling flow, we are checking the status of on an upload that was initiated earlier and is
         not complete yet.
    Then:
        Return a command results object, with scheduling a new command.
    """
    args = SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_ARGS_POLLING
    mocker.patch('CommonServerPython.ScheduledCommand.raise_error_if_not_supported')
    mocker.patch.object(Client, '_generate_token')
    client = Client(server_url="https://api.crowdstrike.com/", username="user1", password="12345", use_ssl=False,
                    proxy=False, reliability=DBotScoreReliability.B)

    mocker.patch.object(Client, 'send_uploaded_file_to_sandbox_analysis',
                        return_value=SEND_UPLOADED_FILE_TO_SANDBOX_ANALYSIS_HTTP_RESPONSE)
    mocker.patch.object(Client, 'get_full_report', return_value=GET_FULL_REPORT_HTTP_RESPONSE)

    expected_outputs = SEND_UPLOADED_FILE_TO_SENDBOX_ANALYSIS_CONTEXT
    command_results = run_polling_command(client, args, 'cs-fx-submit-uploaded-file',
                                          send_uploaded_file_to_sandbox_analysis_command,
                                          get_full_report_command, 'FILE')

    assert command_results.outputs == expected_outputs
    assert command_results.scheduled_command is not None


def test_pop_polling_related_args():
    args = {
        'submit_file': 'submit_file',
        'enable_tor': 'enable_tor',
        'interval_in_seconds': 'interval_in_seconds',
        'polling': 'polling',
        'ids': 'ids'
    }
    pop_polling_related_args(args)
    assert 'submit_file' not in args
    assert 'enable_tor' not in args
    assert 'interval_in_seconds' not in args
    assert 'polling' not in args
    assert 'ids' in args


def test_is_new_polling_search():
    assert not is_new_polling_search({'ids': 'a'})
    assert is_new_polling_search({'polling': 'a'})


def test_arrange_args_for_upload_func():
    args = {
        'submit_file': 'submit_file',
        'enable_tor': 'enable_tor',
        'interval_in_seconds': 'interval_in_seconds',
        'polling': 'polling',
        'ids': 'ids',
        'extended_data': 'extended_data'
    }

    extended_data = arrange_args_for_upload_func(args)
    assert extended_data == 'extended_data'
    assert 'interval_in_seconds' not in args
    assert 'polling' not in args
    assert 'extended_data' not in args


def test_remove_polling_related_args():
    args = {
        'interval_in_seconds': 'interval_in_seconds',
        'polling': 'polling',
        'ids': 'ids',
        'extended_data': 'extended_data'
    }
    remove_polling_related_args(args)
    assert 'interval_in_seconds' not in args
    assert 'extended_data' not in args


def test_parse_indicator():
    sandbox = {
        'sha256': 'sha256',
        'verdict': 'suspicious',
        'submit_name': 'submit_name',
        'file_size': 123,
        'file_type': 'foo type',
        'version_info': [{'id': k, 'value': k} for k in
                         ('CompanyName', 'ProductName', 'LegalCopyright', 'FileDescription', 'FileVersion',
                          'InternalName', 'OriginalFilename')
                         ],
        'submission_type': 'file',
        'dns_requests': [{'address': 'example0.com/foo', 'domain': 'example0.com'}],
        'contacted_hosts': [{'address': 'example1.com'},
                            {'address': 'example2.com'}]
    }
    indicator = parse_indicator(sandbox=sandbox, reliability_str=DBotScoreReliability.A_PLUS)
    expected_context = {'File(val.MD5 && val.MD5 == obj.MD5 || val.SHA1 && val.SHA1 == obj.SHA1 || '
                        'val.SHA256 && val.SHA256 == obj.SHA256 || val.SHA512 && val.SHA512 == obj.SHA512 || '
                        'val.CRC32 && val.CRC32 == obj.CRC32 || val.CTPH && val.CTPH == obj.CTPH || '
                        'val.SSDeep && val.SSDeep == obj.SSDeep)': {
        'Name': 'submit_name', 'Size': 123, 'SHA256': 'sha256', 'Type': 'foo type', 'Company': 'CompanyName',
        'ProductName': 'ProductName',
        'Signature': {'Authentihash': '', 'Copyright': 'LegalCopyright', 'Description': 'FileDescription',
                      'FileVersion': 'FileVersion', 'InternalName': 'InternalName',
                      'OriginalName': 'OriginalFilename'},
        'Relationships': [{'Relationship': 'communicates-with', 'EntityA': 'submit_name', 'EntityAType': 'File',
                           'EntityB': 'example0.com/foo', 'EntityBType': 'IP'},
                          {'Relationship': 'communicates-with', 'EntityA': 'submit_name', 'EntityAType': 'File',
                           'EntityB': 'example0.com', 'EntityBType': 'Domain'},
                          {'Relationship': 'communicates-with', 'EntityA': 'submit_name', 'EntityAType': 'File',
                           'EntityB': 'example1.com', 'EntityBType': 'IP'},
                          {'Relationship': 'communicates-with', 'EntityA': 'submit_name', 'EntityAType': 'File',
                           'EntityB': 'example2.com', 'EntityBType': 'IP'}]},
        'DBotScore(val.Indicator && val.Indicator == obj.Indicator && '
        'val.Vendor == obj.Vendor && val.Type == obj.Type)': {
            'Indicator': 'sha256', 'Type': 'file', 'Vendor': '', 'Score': 2,
            'Reliability': 'A+ - 3rd party enrichment'}}

    assert indicator.to_context() == expected_context, ddiff(indicator.to_context(), expected_context)

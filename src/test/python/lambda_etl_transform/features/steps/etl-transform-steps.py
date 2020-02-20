import sys, os
from behave import *
from hamcrest import *

@given(u'an input file called "{inputfilename}" with the following contents')
def step_inputfile_name(context, inputfilename):
    handle_for_writing_input_file = open(inputfilename, 'w')
    handle_for_writing_input_file.writelines(context.text)
    handle_for_writing_input_file.close()
    pass

@given(u'an error file called "{errorfilename}"')
def step_errorfile_name(context, errorfilename):
    context.error_filename = errorfilename
    pass

@given(u'a load file called "{outputfilename}"')
def step_output_file_name(context, outputfilename):
    context.output_filename = outputfilename
    pass

@when(u'I transform the input file')
def step_transform_input_file(context):
    os.system('python3 ../../../main/python/lambda_etl_transform/etl-transform.py -i test.csv -o test.sql -e test.err')
    pass

@then(u'the error file should contain')
def step_check_error_file(context):
    handle_for_reading_errror_file = open(context.error_filename, 'r')
    error_file_lines = handle_for_reading_errror_file.readlines()
    lines_in_error_file = len(error_file_lines)
    handle_for_reading_errror_file.close()
    lines_expected = context.text.split('\n')
    for i in range(0, lines_in_error_file-1):
        assert_that(error_file_lines[i].strip(), equal_to(lines_expected[i].strip()), 'in line '+str(i+1))

@then(u'the load file should contain')
def step_check_output_file(context):
    handle_for_reading_output_file_file = open(context.output_filename, 'r')
    output_file_lines = handle_for_reading_output_file_file.readlines()
    lines_in_error_file = len(output_file_lines)
    handle_for_reading_output_file_file.close()
    lines_expected = context.text.split('\n')
    for i in range(0, lines_in_error_file-1):
        assert_that(output_file_lines[i].strip(), equal_to(lines_expected[i].strip()), 'in line '+str(i+1))


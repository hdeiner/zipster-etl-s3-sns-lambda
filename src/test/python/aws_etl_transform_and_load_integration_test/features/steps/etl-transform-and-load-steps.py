import sys, os, time, pymysql
from behave import *
from hamcrest import *

@given(u'an input file called "{input_filename}" with the following contents')
def step_create_inputfile(context, input_filename):
    handle_for_writing_input_file = open(input_filename, 'w')
    handle_for_writing_input_file.writelines(context.text)
    handle_for_writing_input_file.close()
    context.inputfilename = input_filename
    pass

@when(u'I send it off to process at "{s3_input_bucket}"')
def step_start_the_etl(context, s3_input_bucket):
    os.system('aws s3 cp ' + context.inputfilename + ' ' + s3_input_bucket + '/' + context.inputfilename)
    pass

@when(u'I wait for "{wait_in_seconds}" seconds instead of doing this right with events')
def step_wait_for_etl_to_happen(context, wait_in_seconds):
    time.sleep(int(wait_in_seconds))
    pass

@then(u'the error object at "{s3_error_bucket}" should contain')
def step_check_etl_transform_errors(context, s3_error_bucket):
    os.system('aws s3 cp ' + s3_error_bucket + '/' + context.inputfilename + ' ' + context.inputfilename + '_errors')
    handle_for_reading_errror_file = open(context.inputfilename + '_errors', 'r')
    error_file_lines = handle_for_reading_errror_file.readlines()
    lines_in_error_file = len(error_file_lines)
    handle_for_reading_errror_file.close()
    lines_expected = context.text.split('\n')
    for i in range(0, lines_in_error_file-1):
        assert_that(error_file_lines[i].strip(), equal_to(lines_expected[i].strip()), 'in line '+str(i+1))

@when(u'I search for zipcodes within "{search_radius}" miles of "{search_zipcode}"')
def step_setup_query(context, search_radius, search_zipcode):
    context.search_radius = search_radius
    context.search_zipcode = search_zipcode

@then(u'the results should be')
def step_check_that_etl_load_worked(context):
    handle_for_reading_mysql_dns = open('../../../main/iac/terraform_etl/.mysql_dns', 'r')
    mysql_dns = handle_for_reading_mysql_dns.readline().strip()
    handle_for_reading_mysql_dns.close()

    user_name = "root"
    user_password = "password"
    database_name = "zipster"

    METERS_TO_MILES = "0.000621371192"
    query = "SELECT T1.ZIPCODE, T1.ZIPCODE_TYPE, T1.CITY, T1.STATE, T1.LOCATION_TYPE, CAST(T1.LATITUDE AS CHAR), CAST(T1.LONGITUDE AS CHAR), T1.LOCATION, CAST(T1.DECOMISSIONED AS CHAR), CAST(st_distance_sphere(point(T1.LONGITUDE, T1.LATITUDE), T2.COORDS) * " + METERS_TO_MILES + " AS CHAR ) AS DISTANCE" + "\n" + \
            "FROM zipster.ZIPCODES AS T1, zipster.ZIPCODES AS T2 \n" + \
            "WHERE st_distance_sphere(point(T1.LONGITUDE, T1.LATITUDE), T2.COORDS) <= " + context.search_radius + "/" + METERS_TO_MILES + "\n" + \
            "AND T2.ZIPCODE = " + context.search_zipcode + "\n" + \
            "AND T1.ZIPCODE != " + context.search_zipcode + "\n" + \
            "ORDER BY st_distance_sphere(point(T1.LONGITUDE, T1.LATITUDE), T2.COORDS) * " + METERS_TO_MILES + " , T1.ZIPCODE ASC\n"

    try:
        result = []
        connection = pymysql.connect(mysql_dns, user=user_name, passwd=user_password, db=database_name, connect_timeout=5)
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            result_count = cursor.rowcount
            connection.close()
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: MySQL error = " + e)

    results_expected = []
    result_count_expected = 0
    for row in context.table:
        results_expected.append([row["zipcode"],row["zipcode_type"],row["city"],row["state"],row["location_type"],row["latitude"],row["longitude"],row["location"],row["decomissioned"],row["distance"]])
        result_count_expected += 1

    assert_that(result_count, equal_to(result_count_expected), 'bad result count')

    for i in range(0, result_count_expected):
        results_received = [result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7],result[i][8],result[i][9]]
        assert_that(results_received, equal_to(results_expected[i]), 'in line '+str(i+1))

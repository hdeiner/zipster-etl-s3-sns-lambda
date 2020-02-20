import sys, os, pymysql
from behave import *
from hamcrest import *

@given(u'I load the transform file "{transform_file}" into a MySQL database running on "{hostdns}" with a user of "{user_name}" and a password of "{user_password}" into the "{database_name}" database')
def step_inputfile_name(context, transform_file, hostdns, user_name, user_password, database_name):
    context.hostdns = hostdns
    context.user_name = user_name
    context.user_password = user_password
    context.database_name = database_name
    os.system('python3 ../../../main/python/lambda_etl_load/etl-load.py -s ' + transform_file + ' -r ' + hostdns + ' -u ' + user_name + ' -p ' + user_password + ' -d ' + database_name)
    pass

@when(u'I search for zipcodes within "{search_radius}" miles of "{search_zipcode}"')
def step_errorfile_name(context, search_radius, search_zipcode):
    context.search_radius = search_radius
    context.search_zipcode = search_zipcode
    pass

@then(u'the results should be')
def step_run_query(context):
    METERS_TO_MILES = "0.000621371192"
    query = "SELECT T1.ZIPCODE, T1.ZIPCODE_TYPE, T1.CITY, T1.STATE, T1.LOCATION_TYPE, CAST(T1.LATITUDE AS CHAR), CAST(T1.LONGITUDE AS CHAR), T1.LOCATION, CAST(T1.DECOMISSIONED AS CHAR), CAST(st_distance_sphere(point(T1.LONGITUDE, T1.LATITUDE), T2.COORDS) * " + METERS_TO_MILES + " AS CHAR ) AS DISTANCE" + "\n" + \
            "FROM zipster.ZIPCODES AS T1, zipster.ZIPCODES AS T2 \n" + \
            "WHERE st_distance_sphere(point(T1.LONGITUDE, T1.LATITUDE), T2.COORDS) <= " + context.search_radius + "/" + METERS_TO_MILES + "\n" + \
            "AND T2.ZIPCODE = " + context.search_zipcode + "\n" + \
            "AND T1.ZIPCODE != " + context.search_zipcode + "\n" + \
            "ORDER BY st_distance_sphere(point(T1.LONGITUDE, T1.LATITUDE), T2.COORDS) * " + METERS_TO_MILES + " , T1.ZIPCODE ASC\n"

    try:
        result = []
        connection = pymysql.connect(context.hostdns, user=context.user_name, passwd=context.user_password, db=context.database_name, connect_timeout=5)
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            result_count = cursor.rowcount
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

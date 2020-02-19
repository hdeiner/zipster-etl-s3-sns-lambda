import sys, getopt, csv, re, boto3, pytest

def main(argv):
    inputfile = ''
    outputfile = ''
    errorfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:e:",["ifile=","ofile=","efile="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-e", "--efile"):
            errorfile = arg

    if ((len(inputfile) == 0) or ((len(outputfile) == 0))):
        print_usage()
        sys.exit(2)


    process(inputfile, outputfile, errorfile)

def print_usage():
    print('usage: etl-transform.py -i <inputfile> -o <outputfile> -e <errorfile>')

def lambda_handler(event, context):
    print("etl-transform started lambda_handler")
    print("etl-transform event="+str(event))

    s3_client = boto3.client('s3')
    print("etl-transform created s3_client")

    sns_client = boto3.client('sns')
    print("etl-transform created sns_client")

    sns_topics = sns_client.list_topics()
    print("etl-transform sns_topics="+str(sns_topics))
    regex_groups = re.search((r'(\S*[\'])(\S*:)(zipster-etl-s3-sns-lambda-transform-topic)'), str(sns_topics))
    zipster_etl_s3_sns_lambda_transform_topic_arn = regex_groups.group(2)+"zipster-etl-s3-sns-lambda-transform-topic"
    print("etl-transform zipster_etl_s3_sns_lambda_transform_topic_arn="+zipster_etl_s3_sns_lambda_transform_topic_arn)

    transform_input_bucket = event['Records'][0]['s3']['bucket']['name']
    print("etl-transform transform_input_bucket="+transform_input_bucket)
    transform_input_object = event['Records'][0]['s3']['object']['key']
    print("etl-transform load_input_object="+transform_input_object)

    print("etl-transform sending zipster_etl_s3_sns_lambda_transform_topic update eMail 1 of 5 (downloading transform input)")
    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_transform_topic_arn, Subject='zipster-etl-s3-sns-lambda-transform-topic', Message='Step 1 of 5 - Downloading transform file from s3 bucket='+transform_input_bucket+' object='+transform_input_object)
    print("etl-transform downloading bucket="+transform_input_bucket+" object="+transform_input_object)
    s3_client.download_file(transform_input_bucket, transform_input_object, "/tmp/etl-transform.input")

    print("etl-transform sending zipster_etl_s3_sns_lambda_transform_topic update eMail 2 of 5 (deleting transform input)")
    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_transform_topic_arn, Subject='zipster-etl-s3-sns-lambda-transform-topic', Message='Step 2 of 5 - Deleting transform file from s3 bucket='+transform_input_bucket+' object='+transform_input_object)
    print("etl-transform deleting bucket="+transform_input_bucket+" object="+transform_input_object)
    s3_client.delete_object(Bucket=transform_input_bucket, Key=transform_input_object)

    print("etl-transform sending zipster_etl_s3_sns_lambda_transform_topic update eMail 3 of 5 (processing transform input)")
    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_transform_topic_arn, Subject='zipster-etl-s3-sns-lambda-transform-topic', Message='Step 3 of 5 - Processing the transform file')
    print("etl-transform processing")
    process("/tmp/etl-transform.input", "/tmp/etl-transform.output", "/tmp/etl-transform.error")

    print("etl-transform sending zipster_etl_s3_sns_lambda_transform_topic update eMail 4 of 5 (uploading transform errors)")
    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_transform_topic_arn, Subject='zipster-etl-s3-sns-lambda-transform-topic', Message='Step 4 of 5 - Uploading transform errors to s3 bucket=zipster-etl-s3-sns-lambda-bucket-transform-error result_object='+transform_input_object)
    print("etl-transform uploading bucket=zipster-etl-s3-sns-lambda-bucket-transform-error object="+transform_input_object)
    s3_client.upload_file("/tmp/etl-transform.error", "zipster-etl-s3-sns-lambda-bucket-transform-error", transform_input_object)

    print("etl-transform sending zipster_etl_s3_sns_lambda_transform_topic update eMail 5 of 5 (uploading load input)")
    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_transform_topic_arn, Subject='zipster-etl-s3-sns-lambda-transform-topic', Message='Step 5 of 5 - Uploading transform results to s3 bucket=zipster-etl-s3-sns-lambda-bucket-load-input result_object='+transform_input_object)
    print("etl-transform uploading bucket=zipster-etl-s3-sns-lambda-bucket-load-input object="+transform_input_object)
    s3_client.upload_file("/tmp/etl-transform.output", "zipster-etl-s3-sns-lambda-bucket-load-input", transform_input_bucket)

    print("etl-transform finished lambda_handler")

def process(inputfile, outputfile, errorfile):

    sql_file = open(outputfile, 'w')
    err_file = open(errorfile, 'w')

    lines_read = 0
    lines_processed = 0
    lines_accepted = 0
    lines_rejected = 0
    errors_encountered = 0

    with open(inputfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if lines_read == 0:
                #print('Column names are ' + str(row))
                lines_read += 1
            else:
                lines_read += 1
                errors = []
                #print('Row ' + str(lines_read) +'  = ' + str(row))
                if (len(row) != 0):
                    lines_processed += 1

                    if (not zipcodeIsValid(row[0])):
                        errors.append("'" + row[0] + "' is an invalid zipcode\n")
                    else:
                        row[0] = zipcodeTransform(row[0])

                    if (not zipcodeTypeIsValid(row[1])):
                        errors.append("'" + row[1] + "' is an invalid zipcode_type\n")

                    if (not cityIsValid(row[2])):
                        errors.append("'" + row[2] + "' is an invalid city\n")

                    if (not stateIsValid(row[3])):
                        errors.append("'" + row[3] + "' is an invalid state\n")

                    if (not locationTypeIsValid(row[4])):
                        errors.append("'" + row[4] + "' is an invalid location_type\n")

                    if (not latitudeLongitudeIsValid(row[5])):
                        errors.append("'" + row[5] + "' is an invalid latitude\n")
                    else:
                        row[5] = latitudeLongitudeTransform(row[5])

                    if (not latitudeLongitudeIsValid(row[6])):
                        errors.append("'" + row[6] + "' is an invalid longitude\n")
                    else:
                        row[6] = latitudeLongitudeTransform(row[6])

                    if (not locationIsValid(row[7])):
                        errors.append("'" + row[7] + "' is an invalid location\n")

                    if (not decommissionedIsValid(row[8])):
                        errors.append("'" + row[8] + "' is an invalid decommissioned\n")

                    if (len(errors) == 0):
                        fileWrite(sql_file, "INSERT INTO ZIPCODES (ZIPCODE, ZIPCODE_TYPE, CITY, STATE, LOCATION_TYPE, LATITUDE, LONGITUDE, LOCATION, DECOMISSIONED) VALUES(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",{});\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
                        lines_accepted += 1
                    else:
                        fileWrite(err_file, "Row " + str(lines_read) +"  = " + str(row) + "\n")
                        fileWrite(err_file, errors)
                        errors_encountered += len(errors)
                        lines_rejected += 1
                else:
                    fileWrite(err_file, 'Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                    fileWrite(err_file,'Blank row skipped\n')
                    errors_encountered += 1

        print('Lines read=' + str(lines_read) + ' processed=' + str(lines_processed) + ' accepted=' + str(lines_accepted) + ' rejected=' + str(lines_rejected) + ' errors=' + str(errors_encountered))

def fileWrite(file,lines):
    file.writelines(lines)

def zipcodeIsValid(input):
    return re.match('^\d{1,5}$', input)

def zipcodeTransform(input):
    return str(int(input)).zfill(5)

def zipcodeTypeIsValid(input):
    return re.match('^(STANDARD|PO BOX|UNIQUE){1}$', input)

def cityIsValid(input):
    return re.match('^([A-Z ]+)$', input)

def stateIsValid(input):
    return re.match('^(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|PR|AA|AE|AP)$', input)

def locationTypeIsValid(input):
    return re.match('^(PRIMARY)$', input)

def latitudeLongitudeIsValid(input):
    return re.match('^([\-]{0,1}[0-9]{1,3}[\.])([0-9]{0,2})$', input)

def latitudeLongitudeTransform(input):
    return re.search('^([\-]{0,1}[0-9]{1,3}[\.])([0-9]{0,2})$', input).group(1) + re.search('^([\-]{0,1}[0-9]{1,3}[\.])([0-9]{0,2})$', input).group(2).ljust(2,'0')

def locationIsValid(input):
    return re.match('^([A-Z\- ]+)$', input)

def decommissionedIsValid(input):
    return re.match('^(FALSE|TRUE)$', input)

# Unit Tests

def test_zipcodeIsValid():
    assert not zipcodeIsValid("0744Z")
    assert not zipcodeIsValid("074401548")
    assert zipcodeIsValid("07440")

def test_zipcodeTransform():
    assert zipcodeTransform("7440") == "07440"
    assert zipcodeTransform("0") == "00000"

def test_zipcodeTypeIsValid():
    assert not zipcodeTypeIsValid("hello")
    assert not zipcodeTypeIsValid("")
    assert not zipcodeTypeIsValid("standard")
    assert zipcodeTypeIsValid("STANDARD")
    assert zipcodeTypeIsValid("PO BOX")
    assert zipcodeTypeIsValid("UNIQUE")

def test_cityIsValid():
    assert not cityIsValid("HOME TOWN 1")
    assert not cityIsValid("Home Town")
    assert cityIsValid("HOME TOWN")

def test_stateIsValid():
    assert not stateIsValid("nj")
    assert stateIsValid("NJ")

def test_locationTypeIsValid():
    assert not locationTypeIsValid("primary")
    assert not locationTypeIsValid("SECONDARY")
    assert locationTypeIsValid("PRIMARY")

def test_longitudeIsValid():
    assert not latitudeLongitudeIsValid("LONGITUDE")
    assert not latitudeLongitudeIsValid("+100.01")
    assert latitudeLongitudeIsValid("100.01")
    assert not latitudeLongitudeIsValid("1000.01")
    assert not latitudeLongitudeIsValid(".01")
    assert latitudeLongitudeIsValid("0.01")
    assert not latitudeLongitudeIsValid("100")
    assert latitudeLongitudeIsValid("100.")
    assert latitudeLongitudeIsValid("100.0")
    assert latitudeLongitudeIsValid("100.00")
    assert not latitudeLongitudeIsValid("100.000")

def test_latitudeLongitudeTransform():
    assert latitudeLongitudeTransform("100.") == "100.00"
    assert latitudeLongitudeTransform("100.0") == "100.00"
    assert latitudeLongitudeTransform("100.00") == "100.00"

def test_locationIsValid():
    assert not locationIsValid("New York")
    assert locationIsValid("NEW YORK")
    assert locationIsValid("NEW-YORK")
    assert not locationIsValid("NEW_YORK")

def test_decommissionedIsValid():
    assert not decommissionedIsValid("true")
    assert not decommissionedIsValid("false")
    assert not decommissionedIsValid("")
    assert decommissionedIsValid("TRUE")
    assert decommissionedIsValid("FALSE")


if __name__ == "__main__":
    main(sys.argv[1:])
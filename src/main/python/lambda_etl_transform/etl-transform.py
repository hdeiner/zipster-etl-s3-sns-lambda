import sys, getopt, csv, re, boto3

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

    PATTERN_ZIPCODE        = '^\d{1,5}$'
    PATTERN_ZIPCODE_TYPE   = '^(STANDARD|PO BOX|UNIQUE){1}$'
    PATTERN_CITY           = '^([A-Z ]+)$'
    PATTERN_STATE          = '^(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|PR|AA|AE|AP)$'
    PATTERN_LOCATION_TYPE  = '^(PRIMARY)$'
    PATTERN_LATITUDE       = '^([\-]{0,1}[0-9]{1,3}[\.])([0-9]{0,2})$'
    PATTERN_LONGITUDE      = '^([\-]{0,1}[0-9]{1,3}[\.])([0-9]{0,2})$'
    PATTERN_LOCATION       = '^([A-Z\- ]+)$'
    PATTERN_DECOMMISSIONED = '^(FALSE|TRUE)$'

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
                #print('Row ' + str(lines_read) +'  = ' + str(row))
                if (len(row) != 0):
                    lines_processed += 1
                    reject = False

                    if (not re.match(PATTERN_ZIPCODE, row[0])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[0] + '\' is an invalid zipcode\n')
                        errors_encountered += 1
                        reject = True
                    else:
                        row[0] = str(int(row[0])).zfill(5)

                    if (not re.match(PATTERN_ZIPCODE_TYPE, row[1])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[1] + '\' is an invalid zipcode_type\n')
                        errors_encountered += 1
                        reject = True

                    if (not re.match(PATTERN_CITY, row[2])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[2] + '\' is an invalid city\n')
                        errors_encountered += 1
                        reject = True

                    if (not re.match(PATTERN_STATE, row[3])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[3] + '\' is an invalid state\n')
                        errors_encountered += 1
                        reject = True

                    if (not re.match(PATTERN_LOCATION_TYPE, row[4])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[4] + '\' is an invalid location_type\n')
                        errors_encountered += 1
                        reject = True

                    if (not re.match(PATTERN_LATITUDE, row[5])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[5] + '\' is an invalid latitude\n')
                        errors_encountered += 1
                        reject = True
                    else:
                        row[5] = re.search(PATTERN_LATITUDE, row[5]).group(1) + re.search(PATTERN_LATITUDE, row[5]).group(2).ljust(2,'0')

                    if (not re.match(PATTERN_LONGITUDE, row[6])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[6] + '\' is an invalid longitude\n')
                        errors_encountered += 1
                        reject = True
                    else:
                        row[6] = re.search(PATTERN_LATITUDE, row[6]).group(1) + re.search(PATTERN_LATITUDE, row[6]).group(2).ljust(2,'0')

                    if (not re.match(PATTERN_LOCATION, row[7])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[7] + '\' is an invalid location\n')
                        errors_encountered += 1
                        reject = True

                    if (not re.match(PATTERN_DECOMMISSIONED, row[8])):
                        err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                        err_file.write('\'' + row[8] + '\' is an invalid decommissioned\n')
                        errors_encountered += 1
                        reject = True

                    if (not reject):
                        sql_file.write("INSERT INTO ZIPCODES (ZIPCODE, ZIPCODE_TYPE, CITY, STATE, LOCATION_TYPE, LATITUDE, LONGITUDE, LOCATION, DECOMISSIONED) VALUES(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",{});\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
                        lines_accepted += 1
                    else:
                        lines_rejected += 1
                else:
                    err_file.write('Row ' + str(lines_read) +'  = ' + str(row) + '\n')
                    err_file.write('Blank row skipped\n')
                    errors_encountered += 1
        print('Lines read=' + str(lines_read) + ' processed=' + str(lines_processed) + ' accepted=' + str(lines_accepted) + ' rejected=' + str(lines_rejected) + ' errors=' + str(errors_encountered))

if __name__ == "__main__":
    main(sys.argv[1:])
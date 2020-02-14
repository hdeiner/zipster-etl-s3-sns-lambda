import os, sys, getopt, re, boto3, pymysql

def main(argv):
    sql_file = ''
    rds_host = ''
    username = ''
    password = ''
    db_name = ''

    try:
        opts, args = getopt.getopt(argv,"hs:r:u:p:d:",["sql_file=", "rds_host=","username=","password=", "db_name="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-s", "--sql_file"):
            sql_file = arg
        elif opt in ("-r", "--rds_host"):
            rds_host = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-d", "--db_name"):
            db_name = arg

    if ((len(sql_file) == 0) or ((len(rds_host) == 0)) or ((len(username) == 0)) or ((len(password) == 0)) or ((len(db_name) == 0))):
        print_usage()
        sys.exit(2)

    process(sql_file, rds_host, username, password, db_name)

def print_usage():
    print('usage: etl_load.py -s <sql_file> -r <rds_host> -u <username> -p <password> -d <db_name>')

def lambda_handler(event, context):
    print("etl_load started lambda_handler")
    print("etl_load event="+str(event))

    s3_client = boto3.client('s3')
    print("etl_load created s3_client")

    sns_client = boto3.client('sns')
    print("etl_load created sns_client")

    sns_topics = sns_client.list_topics()
    print("etl-load sns_topics="+str(sns_topics))
    regex_groups = re.search((r'(\S*[\'])(\S*:)(zipster-etl-s3-sns-lambda-load-topic)'), str(sns_topics))
    zipster_etl_s3_sns_lambda_load_topic_arn = regex_groups.group(2)+"zipster-etl-s3-sns-lambda-load-topic"
    print("etl-load zipster_etl_s3_sns_lambda_load_topic_arn="+zipster_etl_s3_sns_lambda_load_topic_arn)

    load_input_bucket = event['Records'][0]['s3']['bucket']['name']
    print("etl_load load_input_bucket="+load_input_bucket)
    load_input_object = event['Records'][0]['s3']['object']['key']
    print("etl_load load_input_object="+load_input_object)

    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_load_topic_arn, Subject='zipster-etl-s3-sns-lambda-load-topic', Message='Step 1 of 3 - Downloading load file from s3 bucket='+load_input_bucket+' object='+load_input_object)
    print("etl_load downloading load_input_object="+load_input_object)
    s3_client.download_file(load_input_bucket, load_input_object, "/tmp/etl_load.input")

    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_load_topic_arn, Subject='zipster-etl-s3-sns-lambda-load-topic', Message='Step 2 of 3 - Deleting load file from s3 bucket='+load_input_bucket+' object='+load_input_object)
    print("etl_load deleting load_input_object="+load_input_object)
    s3_client.delete_object(Bucket=load_input_bucket, Key=load_input_object)

    print("etl_load getting rds_host")
    rds_host = os.environ['DB_HOST']
    print("etl_load rds_host="+rds_host)

    username = "root"
    password = "password"
    db_name  = "zipster"

    sns_client.publish(TopicArn=zipster_etl_s3_sns_lambda_load_topic_arn, Subject='zipster-etl-s3-sns-lambda-load-topic', Message='Step 3 of 3 - Processing the load file')
    process("/tmp/etl_load.input", rds_host, username, password, db_name)

    print("etl-load finished lambda_handler")

def process(sql_file, rds_host, username, password, db_name):

    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        sys.exit()

    item_count = 0

    try:
        with open(sql_file, 'r') as fp:
            while True:
                line = fp.readline().strip()
                if not line:
                    break
#                print("line="+line)
                cur = conn.cursor()
                cur.execute(line)
                item_count += 1
    except:
        print("ERROR: Unexpected error with file at " + sql_file + ".")
        sys.exit()

    conn.commit()

    print("Ingested %d items" %(item_count))

if __name__ == "__main__":
    main(sys.argv[1:])
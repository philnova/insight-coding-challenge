import feature1
import feature2
import feature3
import feature4
import read_input_data

def run(input_server_log, output_hosts, output_hours, output_resources, output_blocked):

    logf = open("errors.txt", "w") # error logging

    server_log = read_input_data.read(input_server_log)

    # Implement Feature 1
    try:
        parser1 = feature1.FindMostActive(
            server_log,
            output_hosts,
            k=10)
        parser1.parse()
    except Exception as e:
        logf.write("Failed on Feature 1: {0}\n".format(str(e)))

    # Implement Feature 2
    try:
        parser2 = feature2.FindMostIntensiveResources(
            server_log,
            output_resources,
            k=10)
        parser2.parse()
    except Exception as e:
        logf.write("Failed on Feature 2: {0}\n".format(str(e)))

    # Implement Feature 3
    try:
        parser3 = feature3.FindHighestTrafficWindows(
            server_log,
            output_hours,
            k=10,
            minutes_per_bucket=60)
        parser3.parse()
    except Exception as e:
        logf.write("Failed on Feature 3: {0}\n".format(str(e)))

    # Implement Feature 4
    try:
        parser4 = feature4.FindBlockedIPs(
            server_log,
            output_blocked,
            failed_attempts = 3,
            window_seconds = 20,
            block_minutes = 5,
            failure_codes=["401"])
        parser4.parse()
    except Exception as e:
        logf.write("Failed on Feature 4: {0}\n".format(str(e)))

    logf.close()
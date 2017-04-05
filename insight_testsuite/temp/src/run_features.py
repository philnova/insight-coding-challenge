import feature1
import feature2
import feature3
import feature4
import feature5
import read_input_data

def run(input_server_log, output_hosts, output_hours, output_resources, output_blocked, output_bins=None, host_to_track=None):

    logf = open("errors.txt", "w") # error logging

    log_reader = read_input_data.FileInputReader(input_server_log)
    log_reader.read()

    # Implement Feature 1
    try:
        parser1 = feature1.FindMostActive(
            log_reader.data,
            output_hosts,
            k=10)
        parser1.parse()
    except Exception as e:
        logf.write("Failed on Feature 1: {0}\n".format(str(e)))

    # Implement Feature 2
    try:
        parser2 = feature2.FindMostIntensiveResources(
            log_reader.data,
            output_resources,
            k=10)
        parser2.parse()
    except Exception as e:
        logf.write("Failed on Feature 2: {0}\n".format(str(e)))

    # Implement Feature 3
    try:
        parser3 = feature3.FindHighestTrafficWindows(
            log_reader.data,
            output_hours,
            k=10,
            minutes_per_bucket=60)
        parser3.parse()
    except Exception as e:
        logf.write("Failed on Feature 3: {0}\n".format(str(e)))

    # Implement Feature 4
    try:
        parser4 = feature4.FindBlockedIPs(
            log_reader.data,
            output_blocked,
            failed_attempts = 3,
            window_seconds = 20,
            block_minutes = 5,
            failure_codes=["401"])
        parser4.parse()
    except Exception as e:
        logf.write("Failed on Feature 4: {0}\n".format(str(e)))

    # Implement Extra Feature
    if output_bins is not None and host_to_track is not None:
        try:
            parser5 = feature5.GetHostActivityLog(
                log_reader.data,
                output_bins,
                host_to_search = host_to_track,
                minutes_per_bin = 5)
            parser5.parse()
        except Exception as e:
            logf.write("Failed on Feature 4: {0}\n".format(str(e)))

    logf.close()

from traceback import print_stack
import logging, time, os
import utilities.custom_logger as cl


class ReportWriter:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self):
        self.fileName = 'exec_report_' + str(round(time.time() * 1000)) + '.csv'
        self.timeMeasureDir = '../time_measurements/'
        self.relativeFileName = self.timeMeasureDir + self.fileName.replace(" ", "")
        self.currentDirectory = os.path.dirname(__file__)
        self.destinationFile = os.path.join(self.currentDirectory, self.relativeFileName)
        self.destinationDirectory = os.path.join(self.currentDirectory, self.timeMeasureDir)


    def exec_report_handler(self, delta, test_function_name):
        # global report_path
        # full_path = ""
        #
        # fileName = 'exec_report_' + str(round(time.time() * 1000)) + '.csv'
        # timeMeasureDir = '../time_measurements/'
        # relativeFileName = timeMeasureDir + fileName.replace(" ", "")
        # currentDirectory = os.path.dirname(__file__)
        # destinationFile = os.path.join(currentDirectory, relativeFileName)
        # destinationDirectory = os.path.join(currentDirectory, timeMeasureDir)

        try:
            if not os.path.exists(self.destinationDirectory):
                os.makedirs(self.destinationDirectory)

            if not os.path.exists(self.destinationFile):
                with open(self.destinationFile, 'w') as full_path:
                    title = 'Execution report for RHEV build:,\n'
                    date_time = 'Date:,' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '\n\n'
                    table_titles = 'Test name,Duration in seconds'
                    full_path.writelines([title, date_time, table_titles])

                self.log.info('Execution report created in directory: ' + self.destinationFile)

            with open(self.destinationFile, 'a') as full_path:
                full_path.write('\n%s,%s' % (test_function_name, delta))

        except:
            self.log.error('### Exception Occurred while creating exec report')
            print_stack()


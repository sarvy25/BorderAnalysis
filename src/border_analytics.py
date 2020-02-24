"""
Border Crossing Analysis.
@author: Sarvenaz Memarzadeh
email: smemarza@umd.edu
       sarvenaz.me@gmail.com
"""
import math
import datetime
from argparse import ArgumentParser

def get_command_line_arguments():
  '''
  Reads and parses arguments from command line.
  '''
  arg_parser = ArgumentParser('Border Crossing Analysis')
  arg_parser.add_argument('input_path', help='Path to the input file', type=str)
  arg_parser.add_argument('output_path', help='Path to the output file', type=str)
  args = arg_parser.parse_args()
  return args


class BorderStatistics(object):
  '''
  BorderStatistics class. The class provides functions to read a csv file containing
   border crossing information, computing the total number of crossing from a specific
   border, in a specific date using a specific measure. The class also computes the
   running average of crossing from a border using a measure across dates. The output
   can be written to a csv file.
  '''

  def __init__(self, file_path):
    '''
    Initialization function.

    Args:
      file_path: A string. Path to the input file containing the crossing information.
       It is assumed that the file is in csv format separated, each column separated by
       a comma. The following columns should be present: border, date, measure, value.
       The columns can appear in any order.
    '''
    _REQUIRED_KEYS = ['border', 'date', 'measure', 'value']
    print('Reading input from {}'.format(file_path))
    with open(file_path, 'r') as file:
      self.lines = file.readlines()
    # Find the column index of each key
    header = self.lines[0].lower().rstrip()
    header = header.split(',')
    self._KEY_TO_COLUMN_IDX = {}
    for key in _REQUIRED_KEYS:
      assert (key in header), 'The input file should contain a column with header {}'.format(key)
      self._KEY_TO_COLUMN_IDX[key] = header.index(key)

  def process(self):
    '''
    Processes the input file and saves the crossing statistics in the calling object.
    '''
    print('Processing the file...')
    self._processLines()
    self._sortOutput()
    self._computeRunningAverage()
    print('All done!')

  def _processLines(self):
    '''
    Utility function to compute total number of crossings.

    The function computes the total number of crossing from a specific
     border, in a specific date using a specific measure. The computed output
     is stored in the calling object as a dictionary called stats. The dictionary key is
     the combination of border,date,measure and the dictionary value is the total number of
     crossing for that key combination.
    '''
    self.stats = {}
    for i in range(1, len(self.lines)):
      cur_line = self.lines[i]
      fields = cur_line.split(',')

      # Getting the value of the required keys
      border = fields[self._KEY_TO_COLUMN_IDX['border']]
      date = fields[self._KEY_TO_COLUMN_IDX['date']]
      measure = fields[self._KEY_TO_COLUMN_IDX['measure']]
      value = fields[self._KEY_TO_COLUMN_IDX['value']]

      key = border + ',' + date + ',' + measure
      if not key in self.stats:
        self.stats[key] = int(value)
      else:
        self.stats[key] = self.stats[key] + int(value)

  def _sortOutput(self):
    '''
    Utility function to sort the output.

    The function sorts the output first based on date, then total number of crossing, then
     measure, and finally based on border name. The sorted output is stored in the object as a list
     of tuples "called key_value_pairs". The first element in the tuple is the string of
     border,date,measure and the second element is the total number of crossings. It is assumed that
     the _processLines function is already called.
    '''
    def sort_key(x):
      '''
      Local function to be used with the python sorted function.

      It determines the order for sorting.

      Args:
        x: A tuple. The first element is the string representing border,date,measure 
         and the second element is the total number of crossings.
      '''
      [border, date, measure] = x[0].split(',')
      value = x[1]
      # Convert date to a datetime object for comparison
      # The format is mm/dd/YYYY hh:MM:SS AM/PM (Type of date is now date not string)
      date = datetime.datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
      return date, value, measure, border

    key_value_pairs = list(self.stats.items())
    self.key_value_pairs = sorted(key_value_pairs, key=sort_key)

  def _computeRunningAverage(self):
    '''
    Utility function to compute running average.

    The function computes the running average of crossing from a border using 
     a measure across dates. It is assumend that the _sortOutput function is
     already called. 
    '''
    def customRound(x):
      '''
      Custom rounding function.

      The function rounds the input. This function is reimplemented to make sure
       0.5 rounds up instead of down.

      Args:
        x: A floating number.

      Returns:
        The rounded number. 0.5 is rounded up.

      '''
      if (x % 1) >= 0.5:
        return math.ceil(x)
      else:
        return math.floor(x)

    running_stats = {}
    self.running_average_list = [] # final output of runnig average 

    for i in range(len(self.key_value_pairs)):
      cur_key_value = self.key_value_pairs[i]
      [border, _, measure] = cur_key_value[0].split(',')
      value = cur_key_value[1]

      border_measure_key = border + ',' + measure
      if not border_measure_key in running_stats:
        self.running_average_list.append(0)
        running_stats[border_measure_key] = (float(value), 1)
      else:
        pre_avg = running_stats[border_measure_key][0] 
        pre_number_months = running_stats[border_measure_key][1]

        self.running_average_list.append(customRound(pre_avg))

        # Compute runnung average 
        # (pre_value*pre_number_months +value)/ (pre_number_months+1)
        running_stats[border_measure_key] =  (pre_avg / (pre_number_months + 1) 
        * pre_number_months + value / (pre_number_months + 1), pre_number_months + 1) 

  def writeOutput(self, out_path):
    '''
    Writes output to a csv file.

    Each row represent a combination of border, date, measure, value, running average.
     each column is seperated by a comma.

    Args:
      out_path: A string representing the path to the output csv file.
    '''
    print('Writing output to {}'.format(out_path))
    with open(out_path, 'w') as file:
      # Writing header of the file
      file.write('Border,Date,Measure,Value,Average'+'\r\n')
      # Reversing lists to get descending order
      key_value_pairs = reversed(self.key_value_pairs)
      running_average_list = reversed(self.running_average_list)
      # Write rest of the output
      for key_value_pair, running_avg in zip(key_value_pairs, running_average_list):
        key = key_value_pair[0]
        value = key_value_pair[1]
        file.write(key+','+str(value)+','+str(running_avg)+'\r\n')



if __name__ == '__main__':
  command_line_arguments = get_command_line_arguments()
  borderStat = BorderStatistics(file_path=command_line_arguments.input_path)
  borderStat.process()
  borderStat.writeOutput(out_path=command_line_arguments.output_path)


<p align="center"><b>Sarvenaz Memarzadeh</b></p>
<p align="center">smemarza@umd.edu</p>

# Border Crossing Analysis

## Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Running Instructions](README.md#running_instructions)

## Problem
The Bureau of Transportation Statistics regularly makes available data on the number of vehicles, equipment, passengers and pedestrians crossing into the United States by land.

**For this challenge, we want to you to calculate the total number of times vehicles, equipment, passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month. We also want to know the running monthly average of total number of crossings for that type of crossing and border.**

## Approach
The program is implemented in Python. It is compatible with Python3.

A class called ```BorderStatistics``` is implemented which is responsible for all computations. The class provides two main functions for external use:
- ```porcess()``` which performs all computations
- ```writeOutput(file_path)``` which wirtes the result of computation to the specified output file.

The class initializer accepts a ```file_path``` argument which points to the input file. It is assumed that the input file has columns with names ```border, date, measure, value```. *However, the implementation is done in a way that the column order is not important.*

### Reading the input
Reading file is through the initialization function of the class. The argument to the initializor is a string containing the path to the input file. It is assumed that the file is in csv format and each column separated by a comma. The following columns should be present: border, date, measure, value. The columns can appear in any order.

### Computing total number of crossings
A function called ```_processLines()``` computes the total number of crossing from a specific border, in a specific date using a specific measure. The computed output is stored in the calling object as a dictionary called ```stats```. The dictionary key is the combination of border,date,measure and the dictionary value is the total number of crossing for that key combination.

### Sorting the output
The output is first sorted in ascending order, first by date, then by value, then measure, and finally by border. This is done by ```_sortOutput()``` utility function. It is assumed that the ```_processLines()``` function is first called to populate the ```stats``` dictionary. As we require to sort not only based on the keys but also based on the values of this dictionary, we first convert it to a list of tuples, called ```key_value_pairs```. To sort, the python ```sorted``` function is called. However, to customize the sort order, we pass the ```key``` argument to ```sorted``` which changes the behaviour of the comparator. The ```key``` function takes both the keys which contain ```border,date,measure``` infotrmation and the values which are the total corsssings computed.

### Computing the running average
The running average is computed by the ```_computeRunningAverage``` function. It is assumed that the ```_sortOutput``` is already called. As a result, the outputs are already sorted in the ascending order based on dates. This makes the computation of the running average easier. As now, one only needs to do a loop over the sorted list of number of crossings. To keep track of the running average, we use a dictionary. The key is ```border,measure``` and the value is a tuple of ```(avg, N_months)```. As we loop over the list of crossings, we keep updating the running average according to the following formula:
<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=avg_{t}(x)&space;=&space;\frac{avg_{t-1}(x)&space;*&space;N_{months}&space;&plus;&space;x[t]}{N_{months}&space;&plus;1}&space;=&space;avg_{t-1}(x)&space;\times&space;\frac{N_{months}}{N_{months}&space;&plus;1}&space;&plus;&space;\frac{x[t]}{N_{months}&plus;1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?avg_{t}(x)&space;=&space;\frac{avg_{t-1}(x)&space;*&space;N_{months}&space;&plus;&space;x[t]}{N_{months}&space;&plus;1}&space;=&space;avg_{t-1}(x)&space;\times&space;\frac{N_{months}}{N_{months}&space;&plus;1}&space;&plus;&space;\frac{x[t]}{N_{months}&plus;1}" title="avg_{t}(x) = \frac{avg_{t-1}(x) * N_{months} + x[t]}{N_{months} +1} = avg_{t-1}(x) \times \frac{N_{months}}{N_{months} +1} + \frac{x[t]}{N_{months}+1}" /></a>
</p>

where avg_t is the running average of crossings prior to month t, x[t] represents the number of crossings in months t, and N_months represents the number of months observed in the dataset for the corresponding ```border,measure``` combination prior to month t. The running average for each row in the output is saved in a list called ```running_average_list```.

### Writing the output file
The ```writeOutput(output_path)``` function writes the computed total number of crossings and the computed running average into a csv file specified by the ```output_path```. It is assumed that the ```_processLines()``` and ```_computeRunningAverage()``` are called prior to this function. It basically concatenates the stored information in the ```key_value_pairs``` list and the ```running_average_list``` and writes the ouput to ```output_path```, separating columns by commas.

## Running Instructions

The program expects to get two string arguments:
-input_path: A string representing the path to the input file
-output_path: A string representing the path to the output file

For ease of use, a bash script is provided in the root directory of the project ```run.sh```. By default, this scripts looks for an input file named ```Border_Crossing_Entry_Data.csv``` in the ```input``` directory and by default writes the output as ```report.csv``` in the ```output``` directory.

### Testing
The project is tested by the provided ```insight_testsuite``` for the given input/output files.
To test please run the following commands:
```
cd insight_testsuite
bash run_tests.sh
```

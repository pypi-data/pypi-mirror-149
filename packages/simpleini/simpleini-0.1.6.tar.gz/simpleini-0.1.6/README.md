This is the simplest way to interact with a single ini file to store settings. 

Attention! It is delivered together with logging to a file. You need to try to understand.

Use:

	from simpleini import SETTINGS, logging

	parsed_data = SETTINGS(<names_settings>, <required_settings>)

	# names_settings - A string with the names of the settings stored in the file. If there is no file, it will be created and the program will be completed.
	# required_settings - comma-separated list of required variables. 'all' - to check all variables


Example ini reader:

	parsed_data = SETTINGS('settings1, settings2, settings3', 'all')

	settings1 = parsed_data.settings1
	settings2 = parsed_data.settings2
	settings3 = parsed_data.settings3

Example logging:

	logging('message for log') # it will write a file to the project folder log.txt and it will add incoming information to it


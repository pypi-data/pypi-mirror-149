import time
import pandas as pd
import pyedflib as edf
from typing import List


def get_signals(file, signalname: str or List[str] or List[dict]) -> List[int or float]:
	"""
	TODO: Allow the user to insert just the list of signals and the signalheaders and check for file type
	TODO: Document/Comment the code and make it more readable
	Args:
		file: The edf file that is to be imported
		signalname: The name of the signal that is wanted, can also be a list of signals that are wanted

	Returns: list of all the signals that were requested

	"""

	signal = []
	signals, signal_headers, header = edf.highlevel.read_edf(file)

	index = 0
	if signalname == 'all':
		for eeg_dict in signal_headers:
			signal.append(signals[index])
		index += 1

	# Check if signal name is either list or string
	if type(signalname) == list:

		# Check for duplicates in the list and remove them
		signalname = __check_duplicates_and_remove(signalname)
		for name in signalname:

			for eeg_dict in signal_headers:

				# If the
				if eeg_dict['label'] == name:
					signalname.remove(eeg_dict['label'])
					s = signals[index]
					signal.append(signals[index])

				if len(signalname) <= 0:
					break
				index += 1

	elif type(signalname) == str:

		for eeg_dict in signal_headers:

			if eeg_dict['label'] == signalname:
				s = signals[index]
				signal.append(signals[index])
			index += 1

	return signal


def __check_duplicates_and_remove(signal):
	"""
	Checks for duplicates and removes them

	Args:
		signal: A list of all signal labels

	Returns: list with all duplicates removed

	"""
	setOfElems = set()
	dupl = []

	for elem in signal:

		if elem in setOfElems:
			dupl.append(elem)

		else:
			setOfElems.add(elem)

	return list(setOfElems)

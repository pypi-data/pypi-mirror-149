from random import random
from typing import List
import numpy as np


def _segment_fs(signal: List[float or int], fs: int):
	# Maybe have this in a separate file for everyone to use
	return [signal[x:x + fs] for x in range(0, len(signal), fs)]


def lower_frequency(signal: List[float or int], method: str, new_fs: int) -> List[float or int]:
	"""
	Lowers the frequency of the given signal by some given method
	Args:
		signal: List of time series signals
		method: The method how the frequency should be lowered
		new_fs: The new frequency of the signal

	Returns: List of new values corresponding to the method given

	"""
	new_signal = []
	segmented_signal = _segment_fs(signal, new_fs)
	if method.lower() == 'min':
		for index in range(0, len(segmented_signal)):
			the_lowest = min(segmented_signal[index])
			new_signal.append(the_lowest)

	elif method.lower() == 'max':
		for index in range(0, len(segmented_signal)):
			the_lowest = max(segmented_signal[index])
			new_signal.append(the_lowest)

	elif method.lower() == 'mean':
		for index in range(0, len(segmented_signal)):
			the_lowest = np.mean(segmented_signal[index])
			new_signal.append(the_lowest)

	elif method.lower() == 'median':
		for index in range(0, len(segmented_signal)):
			the_lowest = np.median(segmented_signal[index])
			new_signal.append(the_lowest)

	return new_signal


if __name__ == "__main__":
	a = [round(random()*100, 1) for _ in range(1000)]
	b = lower_frequency(a, method='mean', new_fs=100)
	print(b)
	print(len(b))

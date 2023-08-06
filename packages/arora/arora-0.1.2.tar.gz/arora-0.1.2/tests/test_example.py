# While inside project src directory
# To run test coverage from terminal: pytest --cov=arora tests
# To run without coverage from terminal: pytest tests

# Takes up too much memory for devops machine right now...
# def test_get_edf_file():
#     signal_array, pd_dataframe = get_edf(DATASET_DIRECTORY + "/slapp_openaccess/0548/0548_1.edf")
#     assert signal_array is not None
#     assert type(signal_array) == list
#     assert len(signal_array) > 0
#
#     assert pd_dataframe is not None


if __name__ == '__main__':
	# test_get_edf_file()
	do_nothing = 0

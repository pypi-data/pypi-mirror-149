import os

# The path for where the data comes from may be different in the pipeline on gitlab
# If the environment variable doesn't exist we use the default from salamander.
DATASET_DIRECTORY = os.getenv(key="CI_DATA_PATH", default="/datasets")

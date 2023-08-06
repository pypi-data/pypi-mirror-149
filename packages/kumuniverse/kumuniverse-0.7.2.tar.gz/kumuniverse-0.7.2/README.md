# <img src="./assets/karlito.png" alt="Karlito" width="50"/> KUMUniverse
Python shared library for accessing Kumu Data Team's services.

## Prerequisites
1. Python
2. Pip

## Installation
```bash
pip install -U kumuniverse
```

## Usage
```python
from kumuniverse.<module_name> import <class_or_function_name>

# MongoDB
from kumuniverse.mongodb import Mongo
```

## Features
* [MongoDB](./kumuniverse/mongodb/__init__.py)
    * Create Database
    * Create Collection
    * Get Items - get items by passing your own MongoDB [queries](https://www.tutorialspoint.com/python_data_access/python_mongodb_query.htm)
    * Insert Items - batch insert
    * Update Item
    * Remove Item
* [Unleash](./kumuniverse/unleash/__init__.py)
    * Admin
        * Create Feature Toggle
        * Get Feature Toggles
        * Get Feature Toggle by Name
        * Update Feature Toggle
        * Update Feature Variants (Add/Edit/Delete)
        * Tag Feature Toggle
        * Remove Tag Feature Toggle
        * Enable Feature Toggle
        * Disable Feature Toggle
        * Archive Feature Toggle
    * Client
        * Get Variant - given a feature toggle name
* [DynamoDB](./kumuniverse/dynamodb/__init__.py)
    * Get DDB Object
    * Put DDB Object
    * Put DDB Pyspark DataFrame
    * Put DDB Pandas DataFrame
* [MalacanangAPI](./kumuniverse/malacanang_api/__init__.py)
    * Get Variants
* [HalohaloAPI](./kumuniverse/halohalo_api/__init__.py)
    * Get User Segments
    * Update Segment
    * Remove Users from Segment
    * Segment Bulk Writer
* [Sagemaker Feature Store](./kumuniverse/sagemaker_feature_store/__init__.py)
    * Create Feature Group
    * Ingest Record/Pandas/PySpark DataFrames
    * Get Features Group List
    * Describe Feature Group
    * Get Online Features by Record Identifier (ID)
    * Get Online Features by Batch IDs
    * Get Offline Features via Athena Query
* [Logger](./kumuniverse/logger/__init__.py)
    * Instantiate Logger
    * Retrieve Session ID
    * Log Error/Warning/Info/Exception events
* [TahoAPI](./kumuniverse/taho_api/__init__.py)
    * Get Feature Toggles
* Github Action Triggers - SOON!
* Airflow DAG Triggers - SOON!


## Examples
* [MongoDB](./examples/mongodb.py)
* [Unleash](./examples/unleash.py)
* [DynamoDB](./examples/dynamodb.py)
* [MalacanangAPI](./examples/malacanang_api.py)
* [HalohaloAPI](./examples/halohalo_api.py)
* [Sagemaker Feature Store](./examples/sagemaker_feature_store.py)
* [Logger](./examples/logger.py)
* [TahoAPI](./examples/taho_api.py)


## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

## License
***2021 All Rights Reserved***

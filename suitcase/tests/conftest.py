import uuid
import pytest
from databroker import Broker
import os
import sys

if sys.version_info >= (3, 5):
    from bluesky.tests.conftest import RE, hw

AUTH = os.environ.get('MDSTESTWITHAUTH', False)

@pytest.fixture(params=[1], scope='function')
def db_all(request):
    '''Provide a function level scoped metadatastore instance talking to
    temporary database on localhost:27017 with focus on v1.
    '''
    db_name1 = "mds_testing_disposable_{}".format(str(uuid.uuid4()))
    db_name2 = "mds_testing_disposable_{}".format(str(uuid.uuid4()))

    test_config = {
        'metadatastore': {
            'module': 'databroker.headersource.mongo',
            'class': 'MDS',
            'config': {
                'host': 'localhost',
                'port': 27017,
                'database': db_name1,
                'timezone': 'US/Eastern'}
        },
        'assets': {
            'module': 'databroker.assets.mongo',
            'class': 'Registry',
            'config': {
                'host': 'localhost',
                'port': 27017,
                'database': db_name2}
        }
    }
    db = Broker.from_config(test_config)

    def delete_dm():
        print("DROPPING DB")
        db.mds._connection.drop_database(db_name1)
        db.mds._connection.drop_database(db_name2)

    request.addfinalizer(delete_dm)

    return db

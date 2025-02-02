"""
Requests are sent to the backend from this test framework. Each request should
have one and
only one  matching response.

All requests will be sent to backend as:
    {
        name: <class name>,
        data: {
            <all instance variables>
        }
    }

Backend responds with a suitable response as defined in responses.py or an
error as defined
in errors.py. See the requests for information on which response they expect.
"""


class StartTest:
    """ Request the backend to confirm to run a specific test. The backend
    should respond with RunTest if the backend wants the test to be skipped it
    must respond with SkipTest.
    """

    def __init__(self, test_name):
        self.testName = test_name


class NewDriver:
    """ Request to create a new driver instance on the backend.
    Backend should respond with a Driver response or an Error response.
    """

    def __init__(self, uri, authToken, userAgent=None, resolverRegistered=False, domainNameResolverRegistered=False,
                 connectionTimeoutMs=None):
        # Neo4j URI to connect to
        self.uri = uri
        # Authorization token used by driver when connecting to Neo4j
        self.authorizationToken = authToken
        # Optional custom user agent string
        self.userAgent = userAgent
        self.resolverRegistered = resolverRegistered
        self.domainNameResolverRegistered = domainNameResolverRegistered
        self.connectionTimeoutMs = connectionTimeoutMs


class AuthorizationToken:
    """ Not a request but used in NewDriver request
    """

    def __init__(self, scheme="none", principal="",
                 credentials="", realm="", ticket=""):
        self.scheme = scheme
        self.principal = principal
        self.credentials = credentials
        self.realm = realm
        self.ticket = ticket


class VerifyConnectivity:
    """ Request to verify connectivity on the driver
    instance corresponding to the specified driver id.
    Backend should respond with a Driver response or an Error response.
    """

    def __init__(self, driverId):
        self.driverId = driverId


class CheckMultiDBSupport:
    """ Request to check if the server or cluster the driver connects to supports multi-databases.
    Backend should respond with a MultiDBSupport response.
    """

    def __init__(self, driverId):
        self.driverId = driverId


class ResolverResolutionCompleted:
    """ Pushes the results of the resolver function resolution back to the backend.
    This must only be sent immediately after the backend requests a new address resolution
    by replying with the ResolverResolutionRequired response.
    """

    def __init__(self, requestId, addresses):
        self.requestId = requestId
        self.addresses = addresses


class DomainNameResolutionCompleted:
    """ Pushes the results of the domain name resolver function resolution back to the backend.
    This must only be sent immediately after the backend requests a new address resolution
    by replying with the DomainNameResolutionRequired response.
    """

    def __init__(self, requestId, addresses):
        self.requestId = requestId
        self.addresses = addresses


class DriverClose:
    """ Request to close the driver instance on the backend.
    Backend should respond with a Driver response representing the closed
    driver or an error response.
    """

    def __init__(self, driverId):
        # Id of driver to close on backend
        self.driverId = driverId


class NewSession:
    """ Request to create a new session instance on the backend on the driver
    instance corresponding to the specified driver id.
    Backend should respond with a Session response or an Error response.
    """

    def __init__(self, driverId, accessMode, bookmarks=None,
                 database=None, fetchSize=None):
        # Id of driver on backend that session should be created on
        self.driverId = driverId
        # Session accessmode: 'r' for read access and 'w' for write access.
        self.accessMode = accessMode
        # Array of boookmarks in the form of list of strings.
        self.bookmarks = bookmarks
        self.database = database
        self.fetchSize = fetchSize


class SessionClose:
    """ Request to close the session instance on the backend.
    Backend should respond with a Session response representing the closed
    session or an error response.
    """

    def __init__(self, sessionId):
        self.sessionId = sessionId


class SessionRun:
    """ Request to run a query on a specified session.
    Backend should respond with a Result response or an Error response.
    """

    def __init__(self, sessionId, cypher, params, txMeta=None, timeout=None):
        self.sessionId = sessionId
        self.cypher = cypher
        self.params = params
        self.txMeta = txMeta
        self.timeout = timeout


class SessionReadTransaction:
    """ Request to run a retryable read transaction.
    Backend should respond with a RetryableTry response or an Error response.
    """

    def __init__(self, sessionId, txMeta=None, timeout=None):
        self.sessionId = sessionId
        self.txMeta = txMeta
        self.timeout = timeout


class SessionWriteTransaction:
    """ Request to run a retryable write transaction.
    Backend should respond with a RetryableTry response or an Error response.
    """

    def __init__(self, sessionId, txMeta=None, timeout=None):
        self.sessionId = sessionId
        self.txMeta = txMeta
        self.timeout = timeout


class SessionBeginTransaction:
    """ Request to Begin a transaction.
    Backend should respond with a Transaction response or an Error response.
    """

    def __init__(self, sessionId, txMeta=None, timeout=None):
        self.sessionId = sessionId
        self.txMeta = txMeta
        self.timeout = timeout


class SessionLastBookmarks:
    """ Request for last bookmarks on a session.
    Backend should respond with a Bookmarks response or an Error response.
    If there are no bookmarks in the session, the backend should return a
    Bookmark with empty array.
    """

    def __init__(self, sessionId):
        self.sessionId = sessionId


class TransactionRun:
    """ Request to run a query in a specified transaction.
    Backend should respond with a Result response or an Error response.
    """

    def __init__(self, txId, cypher, params):
        self.txId = txId
        self.cypher = cypher
        self.params = params


class TransactionCommit:
    """ Request to run a query in a specified transaction.
    Backend should respond with a Result response or an Error response.
    """

    def __init__(self, txId):
        self.txId = txId


class TransactionRollback:
    """ Request to run a query in a specified transaction.
    Backend should respond with a Result response or an Error response.
    """

    def __init__(self, txId):
        self.txId = txId


class ResultNext:
    """ Request to retrieve the next record on a result living on the backend.
    Backend should respond with a Record if there is a record, an Error if an
    error occured while retrieving next record or NullRecord if there were no
    error and no record.
    """

    def __init__(self, resultId):
        self.resultId = resultId


class ResultConsume:
    """ Request to close the result and to discard all remaining records back
    in the response. Backend should respond with Summary or an Error if an error
    occured.
    """

    def __init__(self, resultId):
        self.resultId = resultId


class RetryablePositive:
    """ Request to commit the retryable transaction.
    Backend responds with either a RetryableTry response (if it failed to
    commit and wants to retry) or a RetryableDone response if committed
    succesfully or an Error response if the backend failed in an
    unretriable way.
    """

    def __init__(self, sessionId):
        self.sessionId = sessionId


class RetryableNegative:
    """ Request to rollback (or more correct NOT commit) the retryable
    transaction.
    Backend will abort retrying and respond with an Error response.
    If the backend sends an error that is generated by the test code (or in
    comparison with real driver usage, client code) the errorId should be ""
    and the backend will respond with a ClientError, if error id is not empty
    the backend will resend that error.
    """

    def __init__(self, sessionId, errorId=""):
        self.sessionId = sessionId
        self.errorId = errorId

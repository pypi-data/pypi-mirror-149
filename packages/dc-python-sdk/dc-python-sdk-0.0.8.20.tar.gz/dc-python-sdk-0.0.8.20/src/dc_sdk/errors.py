class Error(Exception):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    def __str__(self):
        return "The process was terminated because an error occurred:\n\t" + self.message


class AuthenticationError(Error):
    """DataConnector error class raised when a connector could not authenticate"""
    def __init__(self):
        pass


class BadCredentialsError(Error):
    """DataConnector error class raised when the connector is given credentials in a different format than expected"""
    def __init__(self, key_not_found=None):
        """
        :param key_not_found: the key in the credentials that the connector could not process
        """
        self.key = key_not_found

    def __str__(self):
        if self.key:
            return "The process was terminated because the key {0} could not be processed by the connector" \
                .format(self.key)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class WhitelistError(Error):
    """DataConnector error class raised when a connector cannot connect because the user did not whitelist our
    database """
    def __init__(self):
        pass


class NoObjectsFoundError(Error):
    """DataConnector error class raised when the connector returns no objects associated with the user's account"""
    def __init__(self):
        pass


class GetObjectsError(Error):
    """DataConnector error class raised when the connector cannot pull the objects associated with the user's
    account """
    def __init__(self):
        pass


class NoFieldsFoundError(Error):
    """DataConnector error class raised when the connector does not return any fields associated with the object_id"""
    def __init__(self, object_id):
        self.object_id = object_id

    def __str__(self):
        if self.object_id:
            return "The process was terminated because the object {0} did not contain any fields."\
                .format(self.object_id)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class GetFieldsError(Error):
    """DataConnector error class raised when the connector cannot pull the fields associated with the given object_id
    on the user's account """
    def __init__(self, object_id):
        self.object_id = object_id

    def __str__(self):
        if self.object_id:
            return "The process was terminated because the connector failed to pull the fields in the object " \
                   "{0}.\n\t:{1}".format(self.object_id, self.message)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class BadFieldIDError(Error):
    """DataConnector error class raised when the field_id does not belong to the given object_id"""
    def __init__(self, field_id=None, object_id=None):
        self.field_id = field_id
        self.object_id = object_id

    def __str__(self):
        if self.field_id and self.object_id:
            return "The process was terminated because the field_id ({0}) was not found in the object {1}."\
                .format(self.field_id, self.object_id)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class FilterDataTypeError(Error):
    """DataConnector error class raised when datatype of the column that is supposed to be filtered is not date or
    datetime """
    def __init__(self, datatype=None, field_to_filter=None):
        self.datatype = datatype
        self.field = field_to_filter

    def __str__(self):
        if self.datatype and self.field:
            return "The process was terminated because the datatype of {0} was invalid for filtering. Datatype: {1}"\
                .format(self.field, self.datatype)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class BadObjectIDError(Error):
    """DataConnector error class raised when the object_id is not associated with the user"""
    def __init__(self, object_id=None):
        self.object_id = object_id

    def __str__(self):
        if self.object_id:
            return "The process was terminated because the object_id ({0}) could not be found." \
                .format(self.object_id)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class UpdateMethodNotSupportedError(Error):
    """DataConnector error class raised when the chosen update method is invalid for the chosen connector"""
    def __init__(self, update_method=None, connector=None):
        self.update_method = update_method
        self.connector = connector

    def __str__(self):
        if self.update_method and self.connector:
            return "The process was terminated because the update method {0} is not supported by the {1} connector." \
                .format(self.update_method, self.connector)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class MappingError(Error):
    """DataConnector error class raised when the data cannot be mapped to the given columns"""
    def __init__(self):
        pass


class DataError(Error):
    """DataConnector error class raised when the data from the object was unable to be pulled."""
    def __init__(self):
        pass


class APIRequestError(Error):
    """DataConnector error class raised when the connector gets an error code from the API"""
    def __init__(self, error_code_returned=None):
        self.error_code = error_code_returned

    def __str__(self):
        if self.error_code:
            return "The process was terminated because the connector's API returned a {0} error".format(self.error_code)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class APITimeoutError(Error):
    """DataConnector error class raised when the API takes times out"""
    def __init__(self):
        pass


class FieldDataTypeError(Error):
    """DataConnector error class raised when the datatype of a field is not supported"""
    def __init__(self, datatype=None, field=None):
        self.datatype = datatype
        self.field = field

    def __str__(self):
        if self.datatype and self.field:
            return "The process was terminated because the datatype of {0} was invalid. Datatype: {1}" \
                .format(self.field, self.datatype)
        else:
            return "The process was terminated because an error occurred:\n\t" + self.message


class APIPermissionError(Error):
    """DataConnector error class raised when the connector cannot finish a process it lacks API permissions"""
    def __init__(self):
        pass
    
class LoadDataError(Error):
    """DataConnector error class raised when the connector cannot finish loading data"""
    def __init__(self):
        pass

class NotADestinationError(Error):
    """DataConnector error class raised when the load_data function is implemented but the connector is not a destination"""
    def __init__(self):
        pass

class NotImplementedError(Error):
    """DataConnector error class raised when the load_data function is implemented but the connector is not a destination"""
    def __init__(self):
        pass
    def __str__(self):
        return "The function was not implemented"

class NoRowsFoundError(Error):
    """DataConnector error class raised when the database returns no rows"""
    def __init__(self):
        pass

class Utils():
    def createErrorResponse(message):
        return {
            'returnedValue': {
                'message': message
            }
        }

    def createSuccessResponse(returnedValue):
        return {
            'returnedValue': returnedValue
        }

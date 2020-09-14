"""
[Get message error from form]
"""
def getErrorMessage(errors):
    # Get first error
    firstError = next(iter(errors.values()))

    return firstError[0].get('message')

from . import message
from . import util

def catch(function):
    def work():
        try:
            function()  

        except Exception as e:
            getLine = util.parseDunder(function.__code__)
            message.log('error', f'There\'s an error with {function.__name__}() on {getLine[2]}: {e}')

    return work()
import json
import jsonschema
from jsonschema import validate
from os import path, listdir
import logging


class CheckValid:
    """ Checks the conformity of the schemajson with the json file """
    def __init__(self, pathEvent, pathSchema):
        self.pathEv = pathEvent
        self.pathSch = pathSchema
        self.listSchemas = self.getSchemes()
        self.listEvents = self.getEvets()

    def getSchemes(self):
        """retrun list of schema files"""
        return listdir(self.pathSch)

    def getEvets(self):
        """retrun list of event files"""
        return listdir(self.pathEv)

    def openSchems(self):
        """opens all schemas and add dictionary"""
        schemas = dict()
        for path in self.listSchemas:
            with open(self.pathSch+path, 'r') as file:
                schemas[path] = json.load(file)
        return schemas

    def openEvents(self):
        """opens all events and add dictionary"""
        events = dict()
        for path in self.listEvents:
            with open(self.pathEv+path, 'r') as file:
                events[path] = json.load(file)
        return events

    def main(self, schema, event, evFile, schFile):
        """checking files by schemes
            writes logs with errors"""
        eventData = event['data'] # data for verification
        try:
            validate(instance=eventData, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            message = 'Файл {0} не валидный имее ошибку, необходимо посмотреть следущее утвеждение {1}'.format(evFile, err.message)
            logging.error(message)
        except jsonschema.exceptions.SchemaError as err:
            print('Ошибка в Json-схема {} убедитесь в следующем выражении'.format(shcFile), err.message)
        logging.info('Файл {} исправный'.format(evFile))


# add filemode="w" to overwrite
logging.basicConfig(filename="jsonLog.log", level=logging.INFO)


if __name__ == '__main__':
    """start"""
    verification = CheckValid("task_folder/event/", "task_folder/schema/")
    schemas = verification.openSchems()
    events = verification.openEvents()
    """select the file json for the scheme josn"""
    for shcFile, schema in schemas.items():
        for evFile, event in events.items():
            if event:
                if shcFile.startswith(event['event'][:3]):
                    verification.main(schema, event, evFile, shcFile)
            else:
                logging.error('Битый файл {}'.format(evFile))




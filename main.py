from jsonschema import validate
import os
import json

data = []

json_list = []
for root, dirs, files in os.walk("task_folder/event"):
    for filename in files:
        json_list.append("task_folder/event/" + filename)

schema_list = []
for root, dirs, files in os.walk("task_folder/schema"):
    for filename in files:
        schema_list.append("task_folder/schema/" + filename)

schema = {}
json_file = {}
errors_list = []

index = 0
for schema in schema_list:
    with open(schema, 'r') as s:
        schema_todo = json.loads(s.read())

    required = schema_todo['required']
    schema_todo['required'] = []

    for json_file in json_list:

        with open(json_file, 'r') as j:
            json_todo = json.loads(j.read())

        try:
            items_json = json_todo.keys()
        except:
            items_json = []
        for req in required:
            if req not in items_json:
                errors_list.append(f"Error - missing required {req}\n")

        data.append(f"\n\n\n_______________________________________________________________"
                    f"\n"
                    f"SCHEMA: {schema.split('/')[2]}\n"
                    f"\nJSON: {json_file.split('/')[2]}\n\n")

        data[index] = str(data[index]) + "Required errors\n\n"
        for i in range(len(errors_list)):
            data[index] = str(data[index]) + str(i) + ". " + str(errors_list[i])
        errors_list = []

        fs = ''
        fs2 = ''
        try:
            validate(instance=json_todo, schema=schema_todo)
            fs = '\nNone errors in properties'
            fs2 = ''
        except Exception as e:
            fs = "\n\nProperties problem here:"
            fs2 = str(e).split("On instance")[1].replace(" ", '')
        finally:
            data[index] = str(data[index]) + fs + fs2
            index += 1


def writer(data):
    with open("README.md", "w", newline='') as csv_file:
        for row in data:
            csv_file.write(row)


if __name__ == "__main__":
    writer(data)

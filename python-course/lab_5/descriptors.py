class CsvDescriptor:
    def __init__(self, *args):
        self.fields = args

    def __get__(self, instance, owner):
        return ','.join([str(getattr(instance, field)) for field in self.fields])


class XmlDescriptor:
    def __init__(self, tag_name, *args):
        self.tag_name = tag_name
        self.fields = args

    def __get__(self, instance, owner):
        self.tag_name = instance.__class__.__name__
        return '<{} {}/>'.format(
            self.tag_name,
            ' '.join(['{}="{}"'.format(field, getattr(instance, field)) for field in self.fields])
        )


def create_class(class_name, *fields):
    def init(self, *args):
        for field, arg in zip(fields, args):
            setattr(self, field, arg)

    def export_to_csv(*objects):
        result = ','.join([field.upper() for field in fields]) + '\n'
        for obj in objects:
            result += obj.csv + '\n'

        return result

    def export_to_xml(*objects):
        result = '<{}s>\n'.format(class_name)
        for obj in objects:
            result += '  {}\n'.format(obj.xml)
        result += '</{}s>\n'.format(class_name)

        return result

    def export(export_format, *objects):
        if export_format.lower() == 'csv':
            return export_to_csv(*objects)
        elif export_format.lower() == 'xml':
            return export_to_xml(*objects)

        raise Exception("Not supported export format.")

    return type(
        class_name,
        (),
        dict(
            __init__=init,
            csv=CsvDescriptor(*fields),
            xml=XmlDescriptor(class_name.lower(), *fields)
        )
    ), export

Person, export_persons = create_class('Person', 'name', 'birthday')

p = Person("Vlad", "26.09.1994")

print(export_persons('xml', p))

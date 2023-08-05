from networktools.library import my_random_string


class Aux:
    def __init__(self, *args, **kwargs):
        self.__type = None

    @property
    def type(self):
        return self.__type


class FactoryClass:
    __elements = {}
    __instances = {}
    __routes = {}
    __ids = []

    def __init__(self, *args, **kwargs):
        self.uin = kwargs.get('uin', 5)
        tuples = kwargs.get('tuples')
        for name, o_x in tuples:
            self.append(name, o_x)
        routes = kwargs.get('routes')
        for names, path_name in tuples:
            self.add_route(names, path_name)

    @property
    def routes(self):
        return self.__routes

    @property
    def elements(self):
        return self.__elements

    @property
    def instances(self):
        return self.__instances

    @property
    def id_instances(self):
        return self.__ids

    def append(self, name: str, object_x: object):
        self.__elements.update({name: object_x})

    def add_route(self, names: str, path_name: str):
        """
        Insert a list of names that exist on elements
        and the route where that must be ejecuted

        """
        checked_names = [
            name for name in names if name in self.__elements.keys()]
        self.__routes.update({path_name: checked_names})

    def __del__(self, name: str):
        del self.__elements[name]

    def create(self, name, *args, **kwargs):
        this_obj = self.__elements.get(name)
        instance = this_obj(*args, **kwargs)
        idi = self.set_id(self.__ids)
        self.__instances.update({idi: instance})
        return idi

    def get_instance(self, idi):
        return self.__elements.get(idi, None)

    def set_id(self, lista):
        """
        Defines a new id for stations, check if exists
        """
        ids = my_random_string(self.uin)
        while True:
            if ids not in lista:
                lista.append(ids)
                break
            else:
                ids = my_random_string(self.uin)
        return ids

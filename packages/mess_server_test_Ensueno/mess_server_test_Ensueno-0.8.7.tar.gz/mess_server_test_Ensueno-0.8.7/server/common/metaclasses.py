import dis

class AppMaker(type):
    """Universal metaclass for checking the use of sockets for TCP operation,
    the absence of methods that are invalid in the class,
    and the creation of sockets at the class level
    for the App, Client and Server classes"""
    def __init__(cls, clsname, bases, clsdict):

        cls.global_names = []
        cls.methods = []
        cls.attrs = []

        for function in clsdict:
            try:
                inst_gen = dis.get_instructions(clsdict[function])
            except TypeError:
                pass
            else:
                for i in inst_gen:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in cls.global_names:
                            cls.global_names.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in cls.attrs:
                            cls.attrs.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        # в моей структуре классов загружаемые используемые методы
                        # отслеживаются именно здесь, а не в 'LOAD_GLOBAL'
                        if i.argval not in cls.attrs:
                            cls.methods.append(i.argval)
        if clsname == 'App':
            if not ('SOCK_STREAM' in cls.global_names and 'AF_INET' in cls.global_names):
                raise TypeError('Некорректная инициализация сокета.')
        elif clsname == 'Server':
            if 'connect' in cls.methods:
                raise TypeError('Метод connect недопустим в классе Server')
        elif clsname == 'Client':
            for command in ('accept', 'listen',):
                if command in cls.methods:
                    raise TypeError(f'Метод {command} недопустим в классе Client')
            if 'socket' in cls.global_names:
                raise TypeError('Недопустимо создание сокетов на уровне классов')
        super().__init__(clsname, bases, clsdict)

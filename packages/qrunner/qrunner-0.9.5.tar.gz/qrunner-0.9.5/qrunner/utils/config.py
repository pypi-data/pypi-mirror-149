import os
import configparser


local_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(local_path)


class Config:
    def __init__(self):
        self.file_path = os.path.join(root_path, 'running', 'conf.ini')
        self.cf = configparser.ConfigParser()
        self.cf.read(self.file_path)

    def get_name(self, module, key):
        return self.cf.get(module, key)

    def set_name(self, module, key, value):
        self.cf.set(module, key, value)
        with open(self.file_path, 'w') as f:
            self.cf.write(f)

    def get(self, module, key):
        return self.get_name(module, key)

    def set(self, module, key, value):
        self.set_name(module, key, value)


conf = Config()


if __name__ == '__main__':
    print(conf.get_name('info', 'platform'))

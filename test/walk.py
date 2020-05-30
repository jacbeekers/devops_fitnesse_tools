import os


class Walk:
    def walk_through(self, item):
        self.file_counter = 0
        self.directory_counter = 0
        for root, dirs, files in os.walk(item):
            for name in files:
                self.file_counter = self.file_counter + 1
                print("File#" + str(self.file_counter) + ": " + os.path.join(root, name))
            for name in dirs:
                self.directory_counter = self.directory_counter + 1
                print("Directory#" + str(self.directory_counter) + ": " + os.path.join(root, name))
        return self.directory_counter, self.file_counter

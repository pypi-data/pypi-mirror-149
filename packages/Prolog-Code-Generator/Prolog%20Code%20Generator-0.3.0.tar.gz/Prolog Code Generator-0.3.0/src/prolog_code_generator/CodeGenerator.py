import re


class CodeGenerator:

    def __init__(self, data: list) -> None:
        """constructor of code generator class

        :param data: prolog code readed from excel file
        :type data: list
        """
        self.object_name: str = data[0][0].lower()
        self.args: list = data[0][1:]
        self.data: list = data[1:]

        self.code_header = f"top_goal(X) :- {self.object_name}(x)\n"
        self.objects = self._create_objects()

        self._check_uppercase(data)

    @staticmethod
    def _check_uppercase(data: list) -> None:
        """Check if any string in excele file is uppercase

        :param data: prolog code readed from excel file
        :type data: list
        """
        kupsko_list = [f"{element} in Column {col_in} row {row_in} is uppercase"
                       for row_in, row in enumerate(data)
                       for col_in, element in enumerate(row)
                       if re.match(r'\w*[A-Z]\w*', element)]
        if kupsko_list:
            import warnings
            KuPsKo = ",\n".join(kupsko_list)
            warnings.warn(KuPsKo)

    def _create_objects(self) -> list:
        """Create objects 

        :return: list of objects code 
        :rtype: list
        """
        objects = []
        for row in self.data:
            arg_list = []
            for index, element in enumerate(row[1:]):
                string = f"\t{self.args[index]}({element})"
                arg_list.append(string)
            arg_formated = ",\n".join(arg_list)
            objects.append(f"{self.object_name}({row[0]}) :-\n{arg_formated}.\n")
        return objects

    def generate_code(self) -> str:
        """Generate output code

        :return: output code string 
        :rtype: str
        """        """"""
        ask = "\n".join([f"{arg}(X) :- ask({arg},X)." for arg in self.args])
        multivalued = "\n".join([f"multivalued({arg})." for arg in self.args])
        objects = "\n".join(self.objects)
        return "\n\n".join([self.code_header, objects, ask, multivalued])

    @staticmethod
    def code_to_file(code: str, file_name: str = "expert") -> None:
        """export code to .pro file 

        :param code: code to export
        :type code: str
        :param file_name: filename to save, defaults to "program"
        :type file_name: str, optional  
        """
        try:
            with open(f"{file_name}.pro", "w") as file:
                file.write(code)
            print(f"file save as {file_name}.pro")
        except Exception as e:
            print(e)

    def csv_to_code(self, output_path: str):
        outpt_code_str = self.generate_code()
        self.code_to_file(outpt_code_str, output_path)

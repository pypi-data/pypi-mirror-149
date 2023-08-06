class FileInfo(object):
    """
    文件信息
    """
    file_type = ""
    file_id = ""
    file_name = ""

    def __init__(self, file_type, file_id, file_name):
        """
        文件信息
        :param file_type: 文件类型
        :param file_id: 文件ID
        :param file_name: 文件名称
        """
        self.file_type = file_type
        self.file_id = file_id
        self.file_name = file_name

    def obj_to_dict(self):
        return {
            "file_type": self.file_type,
            "file_id": self.file_id,
            "file_name": self.file_name
        }


class DBChangelogModel():
    
     def __init__(
         self,
         key : str,
         author : str,
         pre: str,
         changes: any,
         rollback: any,
         comment: any,
     ):
        self.key = key
        self.author = author
        self.pre = pre
        self.changes = changes
        self.rollback = rollback,
        self.comment = comment
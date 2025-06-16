class IssueRecord:
    def __init__(self, student_id, book_id, issue_date, return_date=None):
        self.student_id = student_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.return_date = return_date

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "book_id": self.book_id,
            "issue_date": self.issue_date,
            "return_date": self.return_date
        }
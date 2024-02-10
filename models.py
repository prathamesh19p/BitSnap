from flask_sqlalchemy import SQLAlchemy
from config import HASH_LEN

db = SQLAlchemy()


class Url(db.Model):
    """Model representing shortened URLs."""

    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(HASH_LEN), unique=True, nullable=False)
    original_url = db.Column(db.Text(), unique=True, nullable=False)
    visited_times = db.Column(db.Integer, default=0)

    def __repr__(self):
        """Return a string representation of the Url object."""
        return f"<Url hash={self.hash}, original_url={self.original_url}, visited_times={self.visited_times}>"

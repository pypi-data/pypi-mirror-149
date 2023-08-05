from clld.db.meta import Base
from clld.db.meta import PolymorphicBaseMixin
from clld.db.models import IdNameDescriptionMixin
from clld.db.models import Sentence
from clld.db.models.common import Contribution
from clld.db.models.common import HasSourceMixin
from clld.db.models.common import Language
from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_corpus_plugin.interfaces import IText
from clld_corpus_plugin.interfaces import IWordform


@implementer(IText)
class Text(Base, IdNameDescriptionMixin):
    pk = Column(Integer, primary_key=True)
    text_type = Column(Unicode())
    text_metadata = Column(JSON)


@implementer(IWordform)
class Wordform(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="wordforms")

    meaning = Column(String)
    segmented = Column(String)


class TextSentence(Base, PolymorphicBaseMixin):
    __table_args__ = (UniqueConstraint("text_pk", "sentence_pk"),)

    text_pk = Column(Integer, ForeignKey("text.pk"), nullable=False)
    sentence_pk = Column(Integer, ForeignKey("sentence.pk"), nullable=False)
    text = relationship(Text, innerjoin=True, backref="sentences", order_by=Sentence.id)
    sentence = relationship(Sentence, innerjoin=True, backref="text_assocs")
    part_no = Column(Integer)


class SentenceSlice(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"))
    sentence_pk = Column(Integer, ForeignKey("sentence.pk"))
    form = relationship(Wordform, backref="sentences")
    sentence = relationship(Sentence, backref="forms")
    index = Column(Integer)

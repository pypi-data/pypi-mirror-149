from clld.db.meta import Base
from clld.db.meta import PolymorphicBaseMixin
from clld.db.models.common import Contribution
from clld.db.models.common import HasSourceMixin
from clld.db.models.common import IdNameDescriptionMixin
from clld.db.models.common import Language
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_morphology_plugin.interfaces import IMeaning
from clld_morphology_plugin.interfaces import IMorph
from clld_morphology_plugin.interfaces import IMorphset
from clld_morphology_plugin.interfaces import IWordform


@implementer(IMeaning)
class Meaning(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    pass


@implementer(IMorphset)
class Morpheme(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="morphemes")
    meaning = Column(String)


@implementer(IMorph)
class Morph(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (
        UniqueConstraint("language_pk", "id"),
        UniqueConstraint("morpheme_pk", "id"),
    )

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)
    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"), nullable=False)
    morpheme = relationship(Morpheme, innerjoin=True, backref="allomorphs")


@implementer(IWordform)
class Wordform(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="wordforms")

    meaning = Column(String)
    segmented = Column(String)
    # meaning = relationship(Meaning, innerjoin=True, backref="wordforms")
    # meaning_pk = Column(Integer, ForeignKey("meaning.pk"))


class FormSlice(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"))
    morph_pk = Column(Integer, ForeignKey("morph.pk"))
    form = relationship(Wordform, backref="morphs")
    morph = relationship(Morph, backref="forms")
    index = Column(Integer)

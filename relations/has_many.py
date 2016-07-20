from base import Base

class HasMany(Base):
   def __get__(self, obj, objtype):
    result = super(HasMany, self).__get__(obj, objtype)
    return result or []

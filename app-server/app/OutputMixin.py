# THIS CLASS IS CREATED TO STANDARDIZE TABLE CONTENT
# EX: ROW -> to_json   >>OR<<    ROW -> to_dict

class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def iter(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None, exclude=()):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
        	for attr, column
            in self.mapper.c.items()
            if column.key not in exclude}
        if rel:
        for attr, relation in self.mapper.relationships.items():
        # Avoid recursive loop between two tables.
    if backref == relation.table:
    continue
    value = getattr(self, attr)
    if value is None:
    res[relation.key] = None
    elif isinstance(value.class, DeclarativeMeta):
    res[relation.key] = value.to_dict(backref=self.table)
    else:
    res[relation.key] = [i.to_dict(backref=self.table)
                  for i in value]
    return res

    def to_json(self, rel=None, exclude=()):
    def extended_encoder(x):
    if isinstance(x, datetime):
    return x.isoformat()
    if isinstance(x, UUID):
    return str(x)
    if rel is None:
    rel = self.RELATIONSHIPS_TO_DICT
    return json.dumps(self.to_dict(rel, exclude=exclude),
    default=extended_encoder)

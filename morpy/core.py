# -*- coding: utf-8 -*-
###############################################################################
# Name: core.py
# Purpose: The core concepts of the MoRP meta-meta model
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013-2014 Igor R. Dejanović <igor DOT dejanovic AT gmail>
# License: MIT License
###############################################################################

from uuid import uuid4
from morpy.const import UUID_MODEL, MORP


class MoRPObject(object):
    '''
    Infrastructure object. It is not a part of MoRP language but
    gives support for meta-modeling.

    Each non-abstract element of MoRP language must, directly or
    indirectly inherits this class.

    Each MoRP object is uniquely identified by UUID identifier.

    Attribute:
        meta (MoRPObject): An object that defines this one.
        uuid (UUID): Unique identifier of this object in the MoRP repository.
    '''
    def __init__(self, meta, uuid=None):

        self._meta = meta

        if not uuid:
            self._uuid = str(uuid4())
        else:
            self._uuid = uuid

        # Register this metaobject by its UUID in the MoRP workspace.
        from morpy import Workspace
        Workspace().by_uuid[self._uuid] = self

    def __str__(self):
        # Special case for Model
        if self._meta == self:
            return "{Model}"

        if hasattr(self, "name"):
            return "{%s(%s)}" % (self.name, self._meta)
        else:
            return "{instof(%s)}" % self._meta

    def __repr__(self):
        return str(self)

    @property
    def meta(self):
        return self._meta

    @property
    def uuid(self):
        return self._uuid


class MoRPContainer(list):
    '''
    List specialization used for containing and querying of MoRP objects.
    '''

    def by_meta(self, meta):
        '''
        Return MoRPContainer filtered by given meta object.
        Using fluent interface pattern.
        Args:
            meta(MoRPObject)
        '''
        if isinstance(meta, str):
            return MoRPContainer(filter(lambda o: hasattr(o.meta, 'name') \
                                        and o.meta.name == meta, self))
        else:
            return MoRPContainer(filter(lambda o: o.meta == meta, self))

    def filter(self, predicate):
        '''
        Return MoRPContainer whose elements returns True if passed to the
        predicate. Using fluent interface pattern.
        Args:
            predicate (callable): Filter predicate.
        '''
        return MoRPContainer(filter(predicate, self))


class ModelContainer(MoRPObject):
    '''
    Superclass for all MoRP objects that can contain Model instances.
    E.g. Mogram or Model. At the same time it is a factory for models
    and API for querying and finding models inside container.
    '''
    def __init__(self, **kwargs):
        super(ModelContainer, self).__init__(**kwargs)
        self.contents = MoRPContainer()

    def create_model(self, name, abstract=False):
        """
        Create model inside this container.
        Args:
            name(string): The name of the model.
            abstract(bool): Is this model abstract?
        """
        model = Model(name, self, abstract)
        self.contents.append(model)
        return model

    def get_by_name(self, name):
        return self.contents.get()

    def get_by_uuid(self, uuid):
        '''
        Return contained model with the given uuid.
        '''
        for model in self.contents:
            if model.uuid == uuid:
                return model
            # Do depth-first search down the containment tree.
            inner_model = model.get_by_uuid(uuid)
            if inner_model is not None:
                return inner_model

    def add_model(self, model):
        '''
        Adds model to the collection of contained models.
        Connects model to this instance as its owner.
        Args:
            model(Model)
        '''
        # If model already has an owner remove it from current owner.
        if model.owner:
            model.owner.remove_model(model)

        self.contents.append(model)
        model.owner = self

    def remove_model(self, model):
        '''
        Removes model from the collection of models. Disconnects model
        from the owner.
        Args:
            model(Model)
        '''
        self.contents.remove(model)
        model.owner = None

    def __iter__(self):
        '''
        Iteration over contained models.
        '''
        return iter(self.contents)

    def __contains__(self, model):
        '''
        Checks if model is present in this container. Used for "in" operator.
        Args:
            model (string or Model): Name of a model or model.
        '''
        if isinstance(model, str):
            return bool([x for x in self.contents if x.name == model])
        else:
            return model in self.contents


class NamedElement(MoRPObject):
    '''
    Element of the MoRP language that has 'name' Property.
    '''
    def __init__(self, name, **kwargs):
        self.name = name
        super(NamedElement, self).__init__(**kwargs)


class Multiplicity(MoRPObject):
    '''
    Element of the MoRP language that has multiplicity.
    '''
    def __init__(self, lower_bound=1, upper_bound=1, **kwargs):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super(Multiplicity, self).__init__(**kwargs)


class Model(NamedElement, ModelContainer):
    '''
    Model is the main concept of MoRP meta-language.
    It defines other concepts including itself.
    It is a factory for its properties and references.
    Each model is a linguistic instance of the Model, i.e. its meta link
    is connected to the Model.
    MoRP models are mapped to python object which are instances of this class.

    Attributes:
        owner (Model): A model instance this model is a child of.
        abstract(bool): Is this model instance abstract. An abstract
            instance cannot have instances itself, i.e. meta links cannot
            reference abstract model.
        super_models (list of Model): A list of models this model inherits
            from.
        properties (list of Property): A list of properties for this model.
        references (list of Reference): A list of references for this model.
    '''
    def __init__(self, name, owner=None, abstract=False, super_models=None,
                 properties=None, references=None, **kwargs):
        '''
        Constructs a Model instance.
        '''

        # Special case. Model conforms to itself.
        if kwargs.get('uuid') == UUID_MODEL:
            meta = self
        else:
            from morpy import Workspace
            meta = Workspace().model

        super(Model, self).__init__(name=name, meta=meta, **kwargs)

        self.owner = None
        self.abstract = abstract

        if owner:
            owner.add_model(self)

        self.super_models = []
        if super_models:
            for super_model in super_models:
                self.add_super_model(super_model)
        self.inherited_models = []

        self.properties = properties or []
        self.references = references or []

    def get_top_level_model(self):
        '''
        Returns model at the top of the owner hierarchy.
        '''
        top_level = self.owner
        while top_level and top_level.owner:
            top_level = top_level.owner
        return top_level

    def create_reference(self, name, type, containment=False, opposite=None,  # @ReservedAssignment @IgnorePep8
                         **kwargs):  # @IgnorePep8
        reference = Reference(name, type, self, containment, **kwargs)
        self.references.append(reference)
        return reference

    def create_property(self, name, type, **kwargs):  # @ReservedAssignment
        prop = Property(name, type, self, **kwargs)
        self.properties.append(prop)
        return prop

    def add_super_model(self, super_model):
        '''
        Adds given model to the collection of super models for this model
        instance.
        Args:
            super_model(Model)
        '''
        self.super_models.append(super_model)
        super_model.inherited_models.append(self)

    def remove_super_model(self, super_model):
        '''
        Removes given model from the collection of super models for this
        model instance.
        Args:
            super_model(Model)
        '''
        if super_model in self.super_models:
            self.super_models.remove(super_model)
            super_model.inherited_models.remove(self)


class Property(Multiplicity, NamedElement):
    '''
    Properties belong to the Model instances.
    Attributes:
        type (PrimitiveType): An ontological instance of the PrimitiveType
            which represents the type of the property.
        owner(Model): An ontological instance of the Model which designates
                        an owner of this property.
    '''
    def __init__(self, name, type, owner, **kwargs):  # @ReservedAssignment
        from morpy import Workspace
        super(Property, self).__init__(meta=Workspace().prop, name=name,
                                       **kwargs)
        self.type = type
        self.owner = owner


class Reference(Multiplicity, NamedElement):
    '''
    Reference refer to other model instances.
    Attributes:
        type (Model): An ontological Model instance this reference points to.
        owner(Model): An ontological instance of the Model that owns this
            reference.
        containment(Boolean): Does this reference have a containment semantics.
        opposite(Model): The other side of the reference (for bidirectional
            references).
    '''
    def __init__(self, name, type, owner, containment=False, opposite=None,  # @ReservedAssignment @IgnorePep8
                 **kwargs):  # @IgnorePep8
        from morpy import Workspace
        super(Reference, self).__init__(meta=Workspace().reference, name=name,
                                        **kwargs)
        self.type = type
        self.owner = owner
        self.containment = containment
        self.opposite = opposite
        if opposite:
            opposite.opposite = self


class ModelInst(MoRPObject):
    '''
    Instance of MoRP model.
    '''

    def _by_name(self, name):
        pass

    def __getattr__(self, name):
        '''
        Get an attribute or reference by name.
        '''
        return self._by_name(name)

    def __setattr__(self, name, value):
        '''
        '''
#         self._by_name(name) = value


class ReferenceInst(MoRPObject):
    '''
    Instance of MoRP reference.
    '''

    def _from(self):
        pass

    def _to(self):
        pass


class Language(NamedElement):
    '''
    Represents a MoRP language.

    Attributes:
        name(string):
        abstract_syntax(Mogram): A language abstract syntax given in the MoRP
            language.
        concrete_syntaxes(list of Mogram): Defines concrete syntaxes in the
            form of editor configuration mograms.
        generators(list of Mogram): Defines a language semantics in the form of
                generator configuration mograms.
    '''

    def __init__(self, name, abssyn_uuid=None, **kwargs):
        from morpy import Workspace
        super(Language, self).__init__(name=name, meta=Workspace().model,
                                       **kwargs)

        # Special case. If this instance represents MoRP language its
        # abstract syntax is defined in this language.
        # This must be specified in this way because MoRP language is
        # not defined at this point yet.
        if name == 'MoRP':
            abssyn_language = self
        else:
            # Currently the only language for abstract syntax definition
            # is MoRP
            abssyn_language = Workspace().morp

        self.abstract_syntax = Mogram(name, conforms_to=abssyn_language,
                                      language=self, uuid=abssyn_uuid)
        self.concrete_syntaxes = []
        self.generators = []


class Mogram(NamedElement, ModelContainer):
    '''
    Represents a mogram given in some language.

    Attributes:
        name (string): A name of this mogram.
        conforms_to (Mogram): An abstract syntax of the language this mogram
            conforms to.
        language (Language): If this mogram is part of some language
            definition this reference will contain instance of containin
            Language.
    '''
    def __init__(self, name, conforms_to, language=None, **kwargs):
        from morpy import Workspace
        super(Mogram, self).__init__(name=name, meta=Workspace().model,
                                     **kwargs)

        self.contents = []
        if not conforms_to and name == MORP:
            # MoRP abstract syntax conforms to itself.
            self.conforms_to = self
        else:
            self.conforms_to = conforms_to
        self.language = language

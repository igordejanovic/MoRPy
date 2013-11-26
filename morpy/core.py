# -*- coding: utf-8 -*-
###############################################################################
# Name: core.py
# Purpose: The core concepts of the MoRP meta-meta model
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
###############################################################################

from uuid import uuid4
from morpy.const import UUID_REFERENCE, UUID_PROPERTY, UUID_MODEL

class MoRPObject(object):
    '''
    Infrastructure object. It is not a part of MoRP language but
    gives support for meta-modeling.
    
    Each non-abstract element of MoRP language must, directly or
    indirectly inherit this class.
    
    Each MoRP object is uniquely identified by UUID identifier. 
    
    Attribute:
        meta (MoRPObject): An object that defines this one.
        uuid (UUID): Unique identifier of this object in the MoRP repository.
    '''
    def __init__(self, meta, uuid=None):
        
        # Special case for MoRP Model instantiation
        if not meta:
            self._meta = self
        else:
            self._meta = meta
        
        if not uuid:
            self._uuid = str(uuid4())
        else:
            self._uuid = uuid
            
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
    
# Note:  Linguistic instances of the Property concepts are 
#        directly mapped to Python type instances.    

       
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

    
class Model(NamedElement):
    '''
    Model is the main concept of MoRP meta-language.
    It defines other concepts including itself.
    Each model is a linguistic instance of the Model, i.e. its meta link 
    is connected to Model.
    MoRP models are mapped to python object which are instances of this class.
    
    Attributes:
        owner (Model): A model instance this model is child of.
        abstract(bool): Is this model instance abstract. Abstract instance cannot 
                    have instances itself, i.e. meta links cannot reference abstract model.
        super_models (list of Model): A list of models this model inherits from.
        properties (list of Property): A list of properties for this model.
        references (list of Reference): A list of references for this model.
    '''
    def __init__(self, name, owner=None, abstract=False, super_models=None,
                 properties=None, references=None, **kwargs):
        '''
        Constructs a Model instance.
        '''
        from morpy import repository
        
        # Special case. Model conforms to itself.
        if kwargs.get('uuid') == UUID_MODEL:
            meta = self
        else:
            meta = repository.model
            
        super(Model, self).__init__(name=name, meta=meta, **kwargs)

        self.owner = None
        self.abstract = abstract

        self.inner_models = []
        if owner:
            owner.add_inner_model(self)
        
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
    
    def get_model_by_uuid(self, uuid):
        '''
        Returns inner model with the given uuid.
        '''
        for inner_model in self.inner_models:
            if inner_model.uuid == uuid:
                return inner_model
        
    def create_reference(self, name, _type, containment=False, opposite=None, **kwargs):
        reference = Reference(name, _type, self, containment, **kwargs)
        self.references.append(reference)
        return reference
    
    def create_property(self, name, _type, **kwargs):
        prop = Property(name, _type, self, **kwargs)
        self.properties.append(prop)
        return prop
    
    def add_super_model(self, super_model):
        '''
        Adds given model to the collection of super models for this model instance.
        Args:
            super_model(Model)
        '''
        self.super_models.append(super_model)
        super_model.inherited_models.append(self)
        
    def remove_super_model(self, super_model):
        '''
        Removes given model from the collection of super models for this model instance.
        Args:
            super_model(Model)
        '''
        if super_model in self.super_models:
            self.super_models.remove(super_model)
            super_model.inherited_models.remove(self)

    def add_inner_model(self, inner_model):
        '''
        Adds inner model to the collection of inner models. Connects inner model to this instance as its owner.
        Args:
            inner_model(Model)
        '''
        # If inner model already has an owner remove it from owners inner models collection.
        if inner_model.owner:
            inner_model.owner.remove_inner_model(inner_model)
        
        self.inner_models.append(inner_model)
        inner_model.owner = self
        
    def remove_inner_model(self, inner_model):
        '''
        Removes inner model from the collection of inner models. Disconnects inner model from the owner.
        Args:
            inner_model(Model)
        '''
        self.inner_models.remove(inner_model)
        inner_model.owner = None
        
    def __iter__(self):
        '''
        Iteration over model returns inner models
        '''    
        return iter(self.inner_models)
    
    
class Property(Multiplicity, NamedElement):
    '''
    Properties belong to the Model instances.
    Attributes:
        _type (PrimitiveType): An ontological instance of the PrimitiveType which
                    represents the type of the property.
        owner(Model): An ontological instance of the Model which designates
                        an owner of this property.
    '''
    def __init__(self, name, _type, owner, **kwargs):
        from morpy import repository
        super(Property, self).__init__(meta=repository.property, name=name, **kwargs)
        self._type = type
        self.owner = owner
    
    
class Reference(Multiplicity, NamedElement):
    '''
    Reference refer to other model instances.
    Attributes:
        _type (Model): An ontological Model instance this reference points to.
        owner(Model): An ontological instance of the Model that owns this reference.
        containment(Boolean): Does this reference have a containment semantics.
        opposite(Model): The other side of the reference (for bidirectional references).
    '''
    def __init__(self, name, _type, owner, containment=False, opposite=None, **kwargs):
        from morpy import repository
        super(Reference, self).__init__(meta=repository.reference, name=name, **kwargs)
        self._type = _type
        self.owner = owner
        self.containment = containment
        self.opposite = opposite
        if opposite:
            opposite.opposite = self



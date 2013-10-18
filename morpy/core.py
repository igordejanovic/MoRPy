# -*- coding: utf-8 -*-
###############################################################################
# Name: core.py
# Purpose: The core concepts of the MoRP meta-meta model
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
###############################################################################

from uuid import uuid4
from morpy.const import UUID_REFERENCE

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

       
class NamedElement(object):
    '''
    Element of the MoRP language that has 'name' Property.
    '''
    def __init__(self, name, **kwargs):
        self.name = name
        super(NamedElement, self).__init__(**kwargs)
        
        
class Multiplicity(object):
    '''
    Element of the MoRP language that has multiplicity.
    '''
    def __init__(self, lower_bound=0, upper_bound=1, **kwargs):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super(Multiplicity, self).__init__(**kwargs)

    
class Model(NamedElement, MoRPObject):
    '''
    Model is the main concept of MoRP meta-language.
    It defines other concepts including itself.
    Each model is a linguistic instance of the Model, i.e. its meta link 
    is connected to Model.
    MoRP models are mapped to python object which are instances of this class.
    
    Attributes:
        parent_model (Model): A model instance this model is child of.
        super_models (list of Model): A list of models this model inherits from.
        properties (list of Property): A list of properties for this model.
        references (list of Reference): A list of references for this model.
    '''
    def __init__(self, meta, name, parent_model=None, super_models=None,
                 properties=None, references=None, **kwargs):
        '''
        Constructs a Model instance.
        '''
        super(Model, self).__init__(name=name, meta=meta, **kwargs)

        self.parent_model = parent_model
        self.child_models = []
        if parent_model:
            parent_model.add_child_model(self)
        
        self.super_models = []
        if super_models:
            for super_model in super_models:
                self.add_super_model(super_model)
        self.sub_models = []
        
        self.properties = properties or []
        self.references = references or []
        
    def get_top_level_model(self):
        '''
        Returns model at the top of the parent chain.
        ''' 
        top_level = self.parent_model
        while top_level and top_level.parent_model:
            top_level = top_level.parent_model
        return top_level
    
    def get_model_by_uuid(self, uuid):
        '''
        Returns child model with the given uuid.
        '''
        for child_model in self.child_models:
            if child_model.uuid == uuid:
                return child_model
        
    def create_reference(self, name, _type, containment=False, opposite=None, **kwargs):
        morp = self.get_top_level_model()
        reference_meta = morp.get_model_by_uuid(UUID_REFERENCE)
        reference = Reference(reference_meta, name, _type, self, containment, **kwargs)
        self.references.append(reference)
        return reference
    
    def create_property(self):
        pass
    
    def add_super_model(self, super_model):
        '''
        Adds given model to the collection of super models for this model instance.
        Args:
            super_model(Model)
        '''
        self.super_models.append(super_model)
        super_model.sub_models.append(self)
        
    def remove_super_model(self, super_model):
        '''
        Removes given model from the collection of super models for this model instance.
        Args:
            super_model(Model)
        '''
        if super_model in self.super_models:
            self.super_models.remove(super_model)
            super_model.sub_models.remove(self)

    def add_child_model(self, child_model):
        '''
        Adds child model to the collection of child models. Connects child model to the parent.
        Args:
            child_model(Model)
        '''
        self.child_models.append(child_model)
        child_model.parent_model = self
        
    def remove_child_model(self, child_model):
        '''
        Removes child model from the collection of child models. Disconnects child model from the parent.
        Args:
            child_model(Model)
        '''
        self.child_models.remove(child_model)
        child_model.parent_model = None
        
    
class Property(Multiplicity, NamedElement, MoRPObject):
    '''
    Properties belong to the Model instances.
    Attributes:
        _type (PrimitiveType): An ontological instance of the PrimitiveType which
                    represents the type of the property.
        owner(Model): An ontological instance of the Model which designates
                        an owner of this property.
    '''
    def __init__(self, meta, name, _type, owner, **kwargs):
        super(Property, self).__init__(meta=meta, name=name, **kwargs)
        self._type = type
        self.owner = owner
    
    
class Reference(Multiplicity, NamedElement, MoRPObject):
    '''
    Reference refer to other model instances.
    Attributes:
        _type (Model): An ontological Model instance this reference points to.
        owner(Model): An ontological instance of the Model that owns this reference.
        containment(Boolean): Does this reference have a containment semantics.
        opposite(Model): The other side of the reference (for bidirectional references).
    '''
    def __init__(self, meta, name, _type, owner, containment=False, opposite=None, **kwargs):
        super(Reference, self).__init__(meta=meta, name=name, **kwargs)
        self._type = _type
        self.owner = owner
        self.containment = containment
        self.opposite = opposite
        
        
class PrimitiveType(MoRPObject):
    '''
    Abstract model that represents MoRP primitive types.
    '''
        
class String(PrimitiveType):
    pass

class Integer(PrimitiveType):
    pass

class Boolean(PrimitiveType):
    pass

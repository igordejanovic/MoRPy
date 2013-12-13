#-*- coding: utf-8 -*-
#######################################################################
# Name: morpy
# Purpose: Workspace is a singleton class that holds all MoRP objects
# 
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#######################################################################

from morpy.const import *
from morpy.exceptions import LanguageExists, MogramExists
from morpy.core import Language, Mogram

def singleton(cls):
    '''
    Class decorator for Singleton pattern implementation.
    See http://www.python.org/dev/peps/pep-0318/#examples
    '''
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

def initialise_morp(func):
    '''
    Decorator for Workspace properties that will lazily call 
    MoRP language initialization on property access if initialization is
    not yet started.
    '''
    def _decorator(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.create_MoRP()
        return func(self, *args, **kwargs)
    return _decorator


@singleton
class Workspace(object):
    '''
    Singleton instance representing a container for all MoRP objects.
    '''
    
    def __init__(self):
        '''
        Singleton implementation.
        Instance is obtained in code using standard class instantiation syntax.
        '''
        # Language definitions
        self.languages = {}
        
        # Free mograms. E.g., mograms that are not part of language definition
        self.mograms = {}
        
        # MoRP objects by UUID
        self.by_uuid = {}
        
    def __iter__(self):
        return iter(self.languages.values())
    
    def __contains__(self, lang):
        '''
        Checks if lang is in this workspace.
        Args:
            lang(string or Language)
        '''
        if isinstance(lang, str):
            return lang in self.languages
        else:
            return lang in self.languages.values()
        
    @initialise_morp    
    def create_language(self, name):
        '''
        Creates language in this workspace.
        Args:
            name(string): Name of the language.
        '''
        if name in self.languages:
            raise LanguageExists(name)
        language = Language(name)
        self.languages[name] = language
        return language
    
    @initialise_morp    
    def create_mogram(self, name, conforms_to):
        '''
        Creates mogram in this workspace.
        Args:
            language(Language): Name of the mogram.
            conforms_to(Language): A language this mogram conforms to. 
        '''
        if name in self.mograms:
            raise MogramExists(name)
        mogram = Mogram(name, conforms_to=conforms_to)
        self.mograms[mogram] = mogram
        return mogram    
    
    def create_MoRP(self):
        '''
        Creates MoRP language in this workspace.
        Workspace should always have a MoRP language as it is a language to 
        define abstract syntaxes of all other languages.
        '''
        from morpy.core import Model, Reference
        
        # We define Models first. 
        # Model model is the top of "meta" hierarchy (everything is model)
        # so it must be defined first.
        model = Model(name=MODEL, uuid=UUID_MODEL)
        # Caching model model for easy access
        self._model = model
        
        _property = Model(PROPERTY, uuid=UUID_PROPERTY)
        # Caching property model for easy access
        self._property = _property
        
        reference = Model(REFERENCE, uuid=UUID_REFERENCE)
        # Caching reference model for easy access
        self._reference = reference
        
        named_element = Model(NAMED_ELEMENT, abstract=True, uuid=UUID_NAMED_ELEMENT)
        multiplicity = Model(MULTIPLICITY, abstract=True, uuid=UUID_MULTIPLICITY)
        
        ptypes = Model(PRIMITIVE_TYPES, uuid=UUID_PRIMITIVE_TYPES)
        ptypes_primitive_type = Model(PRIMITIVE_TYPES_PRIMITIVE_TYPE, abstract=True, owner=ptypes, \
                                      uuid=UUID_PRIMITIVE_TYPES_PRIMITIVE_TYPE)
        ptypes_primitive_type_string = Model(PRIMITIVE_TYPES_STRING, \
                                             owner=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                             uuid=UUID_PRIMITIVE_TYPES_STRING)
        ptypes_primitive_type_integer = Model(PRIMITIVE_TYPES_INTEGER, \
                                              owner=ptypes, \
                                              super_models=[ptypes_primitive_type], \
                                              uuid=UUID_PRIMITIVE_TYPES_INTEGER)
        ptypes_primitive_type_boolean = Model(PRIMITIVE_TYPES_BOOLEAN, \
                                              owner=ptypes, \
                                              super_models=[ptypes_primitive_type], \
                                              uuid=UUID_PRIMITIVE_TYPES_BOOLEAN)

        language = Model(name=LANGUAGE, uuid=UUID_LANGUAGE)
        mogram = Model(name=MOGRAM, uuid=UUID_MOGRAM)
        

        # Model properties and references

        # NamedElement
        named_element.create_property(NAMED_ELEMENT_NAME,
                           type=ptypes_primitive_type_string,
                           uuid=UUID_NAMED_ELEMENT_NAME)
        
        # Multiplicity
        multiplicity.create_property(MULTIPLICITY_LOWER_BOUND,
                            ptypes_primitive_type_integer, uuid=UUID_MULTIPLICITY_LOWER_BOUND)
        multiplicity.create_property(MULTIPLICITY_UPPER_BOUND,
                            ptypes_primitive_type_integer, uuid=UUID_MULTIPLICITY_UPPER_BOUND)
        
        # Model
        model.create_property(MODEL_ABSTRACT,
                              ptypes_primitive_type_boolean, uuid=UUID_MODEL_ABSTRACT)
        model_references = model.create_reference(MODEL_REFERENCES, reference, containment=True, \
                                                  lower_bound=0, upper_bound=-1, uuid=UUID_MODEL_REFERENCES)
        model_properties = model.create_reference(MODEL_PROPERTIES, property, containment=True,  \
                                                  lower_bound=0, upper_bound=-1, uuid=UUID_MODEL_PROPERTIES)
        model_super_models = model.create_reference(MODEL_SUPER_MODELS, model, \
                                                  lower_bound=0, upper_bound=-1, uuid=UUID_MODEL_SUPER_MODELS)
        model.create_reference(MODEL_INHERITED_MODELS, model, \
                              lower_bound=0, upper_bound=-1, opposite=model_super_models, \
                              uuid=UUID_MODEL_INHERITED_MODELS)
        model_owner = model.create_reference(MODEL_OWNER, model, lower_bound=0, uuid=UUID_MODEL_OWNER)
        model.create_reference(MODEL_INNER_MODELS, model, containment=True, \
                              lower_bound=0, upper_bound=-1, opposite=model_owner, \
                              uuid=UUID_MODEL_INNER_MODELS)
        
        # Reference
        reference.create_property(REFERENCE_CONTAINMENT, 
                              ptypes_primitive_type_boolean, uuid=UUID_REFERENCE_CONTAINMENT)
        reference.create_reference(REFERENCE_TYPE, model, uuid=UUID_REFERENCE_TYPE)
        reference.create_reference(REFERENCE_OWNER, model,
                                opposite=model_references, uuid=UUID_REFERENCE_OWNER)
        reference.create_reference(REFERENCE_OPPOSITE, reference,
                                lower_bound=0, uuid=UUID_REFERENCE_TYPE)
        reference.add_super_model(named_element)
        reference.add_super_model(multiplicity)
        
        # Property
        _property.create_reference(PROPERTY_TYPE, ptypes_primitive_type)
        _property.create_reference(PROPERTY_OWNER, model, opposite=model_properties)
        _property.add_super_model(named_element)
        _property.add_super_model(multiplicity)
        
        # Language
        language.create_reference(LANGUAGE_ABSTRACT_SYNTAX, type=mogram,\
                                  containment=True, uuid=UUID_LANGUAGE_ABSTRACT_SYNTAX)
        language.create_reference(LANGUAGE_GENERATOR_CONFS, type=mogram,\
                                  containment=True, lower_bound=0, upper_bound=-1,\
                                  uuid=UUID_LANGUAGE_GENERATOR_CONFS)
        language.create_reference(LANGUAGE_EDITOR_CONFS, type=mogram,\
                                  containment=True, lower_bound=0, upper_bound=-1,\
                                  uuid=UUID_LANGUAGE_EDITOR_CONFS)
        language.add_super_model(named_element)

        # Mogram
        mogram.create_reference(MOGRAM_CONFORMS_TO, type=language, uuid=UUID_MOGRAM_CONFORMS_TO)
        mogram.create_reference(MOGRAM_CONTENTS, type=model, containment=True,
                                lower_bound=0, upper_bound=-1, uuid=UUID_MOGRAM_CONTENTS)
        # TODO: Think about multiple containment opposite semantics. Owner may be only one, but which one is opposite.
        mogram.create_reference(MOGRAM_OWNER, type=language, lower_bound=0, uuid=UUID_MOGRAM_OWNER)
        mogram.add_super_model(named_element)

        # MoRP language
        morp_language = Language(name=MORP, uuid=UUID_MORP_LANGUAGE)
        morp_language.abstract_syntax.contents.extend([mogram, language, model, _property, reference, \
                             named_element, multiplicity, ptypes])
        
        self._morp_language = morp_language
        self._morp = morp_language.abstract_syntax
    
    @property
    @initialise_morp    
    def morp(self):
        '''
        Returns MoRP mogram (i.e. its abstract syntax).
        '''
        return self._morp
    
    @property
    @initialise_morp
    def morp_language(self):
        return self._morp_language
    
    @property
    @initialise_morp
    def model(self):
        '''
        Returns Model MoRP object.
        '''
        return self._model
    
    @property
    @initialise_morp
    def prop(self):
        '''
        Returns Property MoRP object.
        '''
        return self._property
    
    @property
    @initialise_morp
    def reference(self):
        '''
        Returns Reference MoRP object.
        '''
        return self._reference
    
    @initialise_morp    
    def get_by_uuid(self, uuid):
        '''
        Returns MoRP object registered under given UUID.
        '''
        return self.by_uuid[uuid]

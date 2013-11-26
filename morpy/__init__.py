from morpy.const import *
from morpy.language import Language, Mogram


class MoRPRepository(object):
    
    
    def __init__(self):
        # Language definitions
        self.languages = {}
        
        # Free mograms. E.g., mograms that are not part of language definition
        self.mograms = {}
    
    def create_MoRP(self):
        '''
        Initializes MoRP repository. Creates MoRP instance.
        '''
        from morpy.core import Model, Reference
        
        # Model instances. Mode is the top of "meta" hierarchy so it must be defined first.
        model = Model(name=MODEL, uuid=UUID_MODEL)
        self.model = model
        
        _property = Model(PROPERTY, uuid=UUID_PROPERTY)
        self.property = _property # Property cache
        reference = Model(REFERENCE, uuid=UUID_REFERENCE)
        self.reference = reference # Reference cache
        named_element = Model(NAMED_ELEMENT, abstract=True, uuid=UUID_NAMED_ELEMENT)
        multiplicity = Model(MULTIPLICITY, abstract=True, uuid=UUID_MULTIPLICITY)
        
        language = Model(name=LANGUAGE, uuid=UUID_LANGUAGE)
        mogram = Model(name=MOGRAM, uuid=UUID_MOGRAM)
        
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

        # Model properties and references
        
        # NamedElement
        named_element.create_property(NAMED_ELEMENT_NAME,
                           ptypes_primitive_type_string, uuid=UUID_NAMED_ELEMENT_NAME)
        
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
        language.create_reference(LANGUAGE_ABSTRACT_SYNTAX, _type=mogram, containment=True, uuid=UUID_LANGUAGE_ABSTRACT_SYNTAX)
        language.create_reference(LANGUAGE_GENERATOR_CONFS, _type=mogram, containment=True, \
                                  lower_bound=0, upper_bound=-1, uuid=UUID_LANGUAGE_GENERATOR_CONFS)
        language.create_reference(LANGUAGE_EDITOR_CONFS, _type=mogram, containment=True, \
                                  lower_bound=0, upper_bound=-1, uuid=UUID_LANGUAGE_EDITOR_CONFS)
        language.add_super_model(named_element)

        # Mogram
        mogram.create_reference(MOGRAM_CONFORMS_TO, _type=language, uuid=UUID_MOGRAM_CONFORMS_TO)
        mogram.create_reference(MOGRAM_CONTENTS, _type=model, containment=True,
                                lower_bound=0, upper_bound=-1, uuid=UUID_MOGRAM_CONTENTS)
        # TODO: Think about multiple containment opposite semantics. Owner may be only one, but which one is opposite.
        mogram.create_reference(MOGRAM_OWNER, _type=language, lower_bound=0, uuid=UUID_MOGRAM_OWNER)
        mogram.add_super_model(named_element)

        # MoRP language
        morp_language = Language(name=MORP, uuid=UUID_MORP_LANGUAGE)
        morp_language.abstract_syntax.contents.extend([mogram, language, model, _property, reference, \
                             named_element, multiplicity, ptypes])
        
        self._morp_language = morp_language
        self._morp = morp_language.abstract_syntax
        
    @property
    def morp(self):
        # Lazy initialization
        if not hasattr(self, '_morp'):
            self.create_MoRP()
        return self._morp
    
    @property
    def morp_language(self):
        # Lazy initialization
        if not hasattr(self, '_morp_language'):
            self.create_MoRP()
        return self._morp_language
    
        
repository = MoRPRepository()
    
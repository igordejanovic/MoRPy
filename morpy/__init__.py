from morpy.core import Model, Reference
from morpy.const import *


class MoRPRepository(object):
    
    def create_MoRP(self):
        '''
        Initializes MoRP repository. Creates MoRP instance.
        '''
        # Model instances. This model is the top of "meta" hierarchy so it must be defined first.
        model = Model(meta=None, name=MODEL, uuid=UUID_MODEL)
        
        # Top level model for MoRP meta-language
        morp = Model(model, MORP, uuid=UUID_MORP)
        self._morp = morp
        morp.add_inner_model(model)
        
        _property = Model(model, PROPERTY, owner=morp, uuid=UUID_PROPERTY)
        reference = Model(model, REFERENCE, owner=morp, uuid=UUID_REFERENCE)
        named_element = Model(model, NAMED_ELEMENT, abstract=True, owner=morp, uuid=UUID_NAMED_ELEMENT)
        multiplicity = Model(model, MULTIPLICITY, abstract=True, owner=morp, uuid=UUID_MULTIPLICITY)
        ptypes = Model(model, PRIMITIVE_TYPES, owner=morp, uuid=UUID_PRIMITIVE_TYPES)
        ptypes_primitive_type = Model(model, PRIMITIVE_TYPES_PRIMITIVE_TYPE, abstract=True, owner=ptypes, \
                                      uuid=UUID_PRIMITIVE_TYPES_PRIMITIVE_TYPE)
        ptypes_primitive_type_string = Model(model, PRIMITIVE_TYPES_STRING, \
                                             owner=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                             uuid=UUID_PRIMITIVE_TYPES_STRING)
        ptypes_primitive_type_integer = Model(model, PRIMITIVE_TYPES_INTEGER, \
                                             owner=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                              uuid=UUID_PRIMITIVE_TYPES_INTEGER)
        ptypes_primitive_type_boolean = Model(model, PRIMITIVE_TYPES_BOOLEAN, \
                                             owner=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                              uuid=UUID_PRIMITIVE_TYPES_BOOLEAN)
        
        # NamedElement model
        named_element.create_property(NAMED_ELEMENT_NAME,
                           ptypes_primitive_type_string, uuid=UUID_NAMED_ELEMENT_NAME)
        
        # Multiplicity model
        multiplicity.create_property(MULTIPLICITY_LOWER_BOUND,
                            ptypes_primitive_type_integer, uuid=UUID_MULTIPLICITY_LOWER_BOUND)
        multiplicity.create_property(MULTIPLICITY_UPPER_BOUND,
                            ptypes_primitive_type_integer, uuid=UUID_MULTIPLICITY_UPPER_BOUND)
        
        # Model model
        model.create_property(MODEL_ABSTRACT,
                              ptypes_primitive_type_boolean, uuid=UUID_MODEL_ABSTRACT)
        model_references = model.create_reference(MODEL_REFERENCES, reference, containment=True, \
                                                  lower_bound=0, upper_bound=-1, uuid=UUID_MODEL_REFERENCES)
        model_properties = model.create_reference(MODEL_PROPERTIES, property, containment=True)
        model_super_models = model.create_reference(MODEL_SUPER_MODELS, model, \
                                                  lower_bound=0, upper_bound=-1, uuid=UUID_MODEL_SUPER_MODELS)
        model.create_reference(MODEL_INHERITED_MODELS, model, \
                              lower_bound=0, upper_bound=-1, opposite=model_super_models, \
                              uuid=UUID_MODEL_INHERITED_MODELS)
        model_owner = model.create_reference(MODEL_OWNER, model, uuid=UUID_MODEL_OWNER)
        model.create_reference(MODEL_INNER_MODELS, model, containment=True, \
                              lower_bound=0, upper_bound=-1, opposite=model_owner, \
                              uuid=UUID_MODEL_INNER_MODELS)
        model.super_models.append(named_element)
        
        # Reference model
        reference.create_property(REFERENCE_CONTAINMENT, 
                              ptypes_primitive_type_boolean, uuid=UUID_REFERENCE_CONTAINMENT)
        reference.create_reference(REFERENCE_TYPE, model, uuid=UUID_REFERENCE_TYPE)
        reference.create_reference(REFERENCE_OWNER, model,
                                opposite=model_references, uuid=UUID_REFERENCE_OWNER)
        reference.create_reference(REFERENCE_OPPOSITE, reference,
                                lower_bound=0, uuid=UUID_REFERENCE_TYPE)
        reference.super_models.extend([named_element, multiplicity])
        
        
        # Property model
        _property.create_reference(PROPERTY_TYPE, model)
        _property.create_reference(PROPERTY_OWNER, model, opposite=model_properties)
        _property.super_models.extend([named_element, multiplicity])
        
    @property
    def morp(self):
        # Lazy initialization
        if not hasattr(self, '_morp'):
            self.create_MoRP()
        return self._morp
        
repository = MoRPRepository()
    
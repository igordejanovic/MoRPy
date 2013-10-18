from morpy.core import Model, Reference
from morpy.const import *


class MoRPRepository(object):
    

    def get_MoRP(self):
        '''
        Creates MoRP instance.
        '''
        
        # Model instances. This model is the top of "meta" hierarchy so it must be defined first.
        model = Model(meta=None, name="Model", uuid=UUID_MODEL)
        
        # Top level model for MoRP meta-language
        morp = Model(model, "MoRP", uuid=UUID_MORP)
        morp.add_child_model(model)
        
        property = Model(model, "Property", parent_model=morp, uuid=UUID_PROPERTY)
        reference = Model(model, "Reference", parent_model=morp, uuid=UUID_REFERENCE)
        named_element = Model(model, "NamedElement", parent_model=morp, uuid=UUID_NAMED_ELEMENT)
        multiplicity = Model(model, "Multiplicity", parent_model=morp, uuid=UUID_MULTIPLICITY)
        ptypes = Model(model, "PrimitiveTypes", parent_model=morp, uuid=UUID_PRIMITIVE_TYPES)
        ptypes_primitive_type = Model(model, "PrimitiveType", \
                                      uuid=UUID_PRIMITIVE_TYPES_PRIMITIVE_TYPE)
        ptypes_primitive_type_string = Model(model, "String", \
                                             parent_model=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                             uuid=UUID_PRIMITIVE_TYPES_STRING)
        ptypes_primitive_type_integer = Model(model, "Integer", \
                                             parent_model=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                              uuid=UUID_PRIMITIVE_TYPES_INTEGER)
        ptypes_primitive_type_boolean = Model(model, "Boolean", \
                                             parent_model=ptypes, \
                                             super_models=[ptypes_primitive_type], \
                                              uuid=UUID_PRIMITIVE_TYPES_BOOLEAN)
        
        # Model Model
        # Model.references
        model_references = model.create_reference("references", reference, containment=True, \
                                                  upper_bound=-1, uuid=UUID_MODEL_REFERENCES)
        model_super_models = model.create_reference("super_models", model, \
                                                  upper_bound=-1, uuid=UUID_MODEL_SUPER_MODELS)
        model_inherited_models = model.create_reference("inherited_models", model, \
                                                  upper_bound=-1, opposite=model_super_models, \
                                                  uuid=UUID_MODEL_INHERITED_MODELS)
        model_owner = model.create_reference("owner", model, uuid=UUID_MODEL_OWNER)
        model_inner_models = model.create_reference("inner_models", model, containment=True, \
                                                  upper_bound=-1, opposite=model_owner, \
                                                  uuid=UUID_MODEL_INNER_MODELS)
        
        # Reference.type
        reference_type = model.create_reference("type", model, uuid=UUID_REFERENCE_TYPE)
        
        
        model.super_models.append(named_element)
        
        
        
        property.super_models.append(named_element)
        
        return morp
        
        
repository = MoRPRepository()
    
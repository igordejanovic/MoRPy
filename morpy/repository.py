"""
"""


class AbstractRepository(object):
    """
    Models repository for MoRP graphs.
    In the same time represents a factory for MoRP objects.
    """
    def create_model(self):
        pass

    def create_model_inst(self):
        pass

    def create_reference(self):
        pass

    def create_reference_inst(self):
        pass

    def create_property(self):
        pass

    def remove(self, obj):
        pass


    # Inheriting classes should implement following methods


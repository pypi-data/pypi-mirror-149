# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



class PetrelObjectStoreBase(dict):
    """Base class of read-only collections storing Petrel objects by their path.
    When iterated over, the objects are returned, not their pathss (unlike a standard
    Python dictionary which returns the keys).
    """

    def __init__(self, petrelconnection):
        self._petrelconnection = petrelconnection
        self._objects = self._query_objects(petrelconnection)

    def _query_objects(self, petrelconnection):
        # Virtual method to be implemented in sub class
        return {}

    def get_petrel_objects(self, objects_info, find_object_by_guid_func):        
        objects = {}
        for guid, path in objects_info.items():
            obj = find_object_by_guid_func(guid)

            if path in objects.keys():
                # duplicate paths!
                existing = objects[path]
                # create or append to a list of petrel objects
                if isinstance(existing, list):
                    existing.append(obj)
                else:
                    objects[path] = [existing, obj]
            else:
                # unique path
                objects[path] = obj
        return objects

    def __getitem__(self, key):
        try:
            return self._objects[key]   
        except KeyError:
            self._objects = self._query_objects(self._petrelconnection)
            return self._objects[key] 

    def __setitem__(self, key, value):
        raise Exception("This collection is read-only")

    def __len__(self):
        return len(self._objects)

    def __iter__(self):
        # This is not dict-like behaviour!
        return iter(self._objects.values())

    def keys(self):
        """The paths of the Petrel objects

        Returns:
            A list of the paths of the Petrel objects
        """
        return self._objects.keys()

    def values(self):
        """The Petrel objects

        Returns:
            A list of the Petrel objects"""
        return self._objects.values()

    def items(self):
        """The (`path`, `Petrel object`) pairs available.  If multiple objects
        have the same path, a list of Petrel objects is returned.

        Returns:
            A list of (`path`, `objects`) tuples (pairs) available

        """
        return self._objects.items()

    def __str__(self):
        return str(self._objects)

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

class Properties(PetrelObjectStoreBase):
    """A read-only collection of GridProperty objects.
    """
    
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_grid_properties(), 
            lambda guid: petrelconnection._get_grid_property_by_guid(guid)
        )

class DiscreteProperties(PetrelObjectStoreBase):
    """A read-only collection of GridDiscreteProperty objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_grid_properties(discrete = True), 
            lambda guid: petrelconnection._get_grid_property_by_guid(guid, discrete = True)
        )

class Grids(PetrelObjectStoreBase):
    """A read-only collection of Grid objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_grids(), 
            lambda guid: petrelconnection._get_grid_by_guid(guid)
        )
        

class SeismicCubes(PetrelObjectStoreBase):
    """A read-only collection of Seismic Cube objects.
    """
    
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_seismic_cubes(), 
            lambda guid: petrelconnection._get_seismic_cube_by_guid(guid)
        )

class HorizonProperties(PetrelObjectStoreBase):
    """A collection of HorizonProperty objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_horizon_properties(), 
            lambda guid: petrelconnection._get_horizon_property_by_guid(guid)
        )

class PropertyCollections(PetrelObjectStoreBase):
    """A collection of PropertyCollection objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_property_collections(), 
            lambda guid: petrelconnection._get_property_collection_by_guid(guid)
        )

class HorizonInterpretation3Ds(PetrelObjectStoreBase):
    """ A collection of HorizonInterpretation3D objects.
    """
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_horizon_interpretation_3ds(), 
            lambda guid: petrelconnection._get_horizon_interpretation_3d_by_guid(guid)
        )

class HorizonInterpretations(PetrelObjectStoreBase):
    """ A collection of HorizonInterpretation3D objects.
    """
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_horizon_interpretations(), 
            lambda guid: petrelconnection._get_horizon_interpretation_by_guid(guid)
        )

class Seismic2Ds(PetrelObjectStoreBase):
    """ A collection of Seismic2D objects.
    """
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_seismic_2ds(), 
            lambda guid: petrelconnection._get_seismic_2d_by_guid(guid)
        )

class Surfaces(PetrelObjectStoreBase):
    """A read-only collection of Surface objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_surfaces(), 
            lambda guid: petrelconnection._get_surface_by_guid(guid)
        )

class SurfaceAttributes(PetrelObjectStoreBase):
    """A read-only collection of SurfaceaAttribute objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_surface_attributes(), 
            lambda guid: petrelconnection._get_surface_attribute_by_guid(guid)
        )

class SurfaceDiscreteAttributes(PetrelObjectStoreBase):
    """A read-only collection of SurfaceaDiscreteAttribute objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_surface_attributes(discrete = True), 
            lambda guid: petrelconnection._get_surface_attribute_by_guid(guid, discrete = True)
        )

class WellLogs(PetrelObjectStoreBase):
    """A read-only collection of WelllLog objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_well_logs(), 
            lambda guid: petrelconnection._get_well_log_by_guid(guid)
        )

class DiscreteWellLogs(PetrelObjectStoreBase):
    """A read-only collection of DiscreteWelllLog objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_well_logs(discrete = True), 
            lambda guid: petrelconnection._get_well_log_by_guid(guid, discrete = True)
        )

class GlobalWellLogs(PetrelObjectStoreBase):
    """A read-only collection GlobalWelllLog objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_global_well_logs(), 
            lambda guid: petrelconnection._get_global_well_log_by_guid(guid)
        )

class DiscreteGlobalWellLogs(PetrelObjectStoreBase):
    """A read-only collection of DiscreteWelllLog objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_global_well_logs(discrete = True), 
            lambda guid: petrelconnection._get_global_well_log_by_guid(guid, discrete = True)
        )

class Wells(PetrelObjectStoreBase):
    """A read-only collection of Well objects.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_wells(), 
            lambda guid: petrelconnection._get_well_by_guid(guid)
        )

class PointSets(PetrelObjectStoreBase):
    """A read-only collection of PointSet objects.

    ** The implementation of point sets is in a preliminary state. Handling large sets may
        fail or be slow. We are working on improving this.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_pointsets(), 
            lambda guid: petrelconnection._get_pointset_by_guid(guid)
        )

class PolylineSets(PetrelObjectStoreBase):
    """A read-only collection of PolylineSets objects.

    ** The implementation of polyline sets is in a preliminary state. Handling large sets may
        fail or be slow. We are working on improving this.
    """

    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_polylinesets(), 
            lambda guid: petrelconnection._get_polylineset_by_guid(guid)
        )

class Wavelets(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_wavelets(), 
            lambda guid: petrelconnection._get_wavelet_by_guid(guid)
        )

class Workflows(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_workflows(), 
            lambda guid: petrelconnection._get_workflow_by_guid(guid)
        )

class ReferenceVariables(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_reference_variables(), 
            lambda guid: petrelconnection._get_reference_variable_by_guid(guid)
        )

class XyzWellSurveys(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_xyz_well_surveys(),
            lambda guid: petrelconnection._get_xyz_well_survey_by_guid(guid)
        )

class XytvdWellSurveys(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_xytvd_well_surveys(),
            lambda guid: petrelconnection._get_xytvd_well_survey_by_guid(guid)
        )

class DxdytvdWellSurveys(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_dxdytvd_well_surveys(),
            lambda guid: petrelconnection._get_dxdytvd_well_survey_by_guid(guid)
        )

class MdinclazimWellSurveys(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_mdinclazim_well_surveys(),
            lambda guid: petrelconnection._get_mdinclazim_well_survey_by_guid(guid)
        )

class ExplicitWellSurveys(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_explicit_well_surveys(),
            lambda guid: petrelconnection._get_explicit_well_survey_by_guid(guid)
        )

class WellSurveys(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        well_surveys = {}
        well_surveys.update(
            self.get_petrel_objects(
                petrelconnection._find_xyz_well_surveys(), 
                lambda guid: petrelconnection._get_xyz_well_survey_by_guid(guid)
            )
        )
        well_surveys.update(
            self.get_petrel_objects(
                petrelconnection._find_xytvd_well_surveys(), 
                lambda guid: petrelconnection._get_xytvd_well_survey_by_guid(guid)
            )
        )
        well_surveys.update(
            self.get_petrel_objects(
                petrelconnection._find_dxdytvd_well_surveys(), 
                lambda guid: petrelconnection._get_dxdytvd_well_survey_by_guid(guid)
            )
        )
        well_surveys.update(
            self.get_petrel_objects(
                petrelconnection._find_mdinclazim_well_surveys(), 
                lambda guid: petrelconnection._get_mdinclazim_well_survey_by_guid(guid)
            )
        )
        well_surveys.update(
            self.get_petrel_objects(
                petrelconnection._find_explicit_well_surveys(), 
                lambda guid: petrelconnection._get_explicit_well_survey_by_guid(guid)
            )
        )
        return well_surveys

class ObservedDataObjects(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_observed_data(),
            lambda guid: petrelconnection._get_observed_data_by_guid(guid)
        )

class ObservedDataSets(PetrelObjectStoreBase):
    def _query_objects(self, petrelconnection):
        petrelconnection._opened_test()
        return self.get_petrel_objects(
            petrelconnection._find_observed_data_sets(),
            lambda guid: petrelconnection._get_observed_data_set_by_guid(guid)
        )
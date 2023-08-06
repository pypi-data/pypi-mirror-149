# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import io
import os
import sys
from cegalprizm.pythontool.test.hub.petreltestcase import PetreltestUnitCase
from cegalprizm.pythontool import PetrelConnection


class PythonToolTestProject2ScriptsTest(PetreltestUnitCase):
    _project: str = fr'{os.environ["home"]}/Documents\PetrelUnitTestFramework\1\PythonToolTestProject2\PythonToolTestProject2.pet'
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)



    def test_GrpcConnection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            a = petrellink.ping()
            b = petrellink.ping()
            print(b-a)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grpc_connection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionWellsWelllogsPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            #41128 Well and well logs in subfolder #41175 Global well logs folder in the path #41132 Global well log folders in path
            
            well = petrellink.wells['Input/Wells/Subfolder/Well_Good 2']
            print(well.path)
            
            welllog = petrellink.well_logs['Input/Wells/Subfolder/Well_Good 2/Well logs/Density logs/RHOB']
            print(welllog.path)
            
            globalwelllog = petrellink.global_well_logs['Input/Wells/Global well logs/Density logs/RHOB']
            print(globalwelllog.path)
            
            discreteglobalwelllog = petrellink.discrete_global_well_logs['Input/Wells/Global well logs/Density logs/Copy of Facies']
            print(discreteglobalwelllog.path)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_wells_welllogs_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionPointsetsPolylinesetsPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            #41136 Objects inside folder in seismic survey
            
            #3D
            pointset2 = petrellink.pointsets['Input/Seismic/Ardmore/Seismic3D/Under 3D seismic/Points 1 2']
            polylineset2 = petrellink.polylinesets['Input/Seismic/Ardmore/Seismic3D/Under 3D seismic/Polygon 2']
            
            print(pointset2.path)
            print(polylineset2.path)
            
            
            #2D Not implemented for now
            #pointset3 = petrellink.pointsets['Input/Seismic/Survey 1/Seismic2D/Under 2D seismic/Points 1 3']
            #polylineset3 = petrellink.polylinesets['Input/Seismic/Survey 1/Seismic2D/Under 2D seismic/Polygon 3']
            
            #print(pointset3.path)
            #print(polylineset3.path)
            
            #41133 Pointsets inside subfolder
            pointset1 = petrellink.pointsets['Input/Geometry/Subfolder/Points 1 1']
            print(pointset1.path)
            
            #41134 Polylinesets inside subfolder
            polylineset1 = petrellink.polylinesets['Input/Geometry/Subfolder/Polygon 1']
            print(polylineset1.path)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_pointsets_polylinesets_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionSurfaceSurfaceattributesPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            #41136 Objects inside folder in seismic survey
            
            #3D
            surface2 = petrellink.surfaces['Input/Seismic/Ardmore/Seismic3D/Under 3D seismic/BCU 2']
            print(surface2.path)
            #2D Not implemented for now
            #surface3 = petrellink.surfaces['Input/Seismic/Survey 1/Seismic2D/Under 2D seismic/BCU 3']
            #print(surface3.path)
            
            
            #41124 Surface attribute under subfolder
            surfaceattribute = petrellink.surface_attributes['Input/TWT Surface/Subfolder/BCU 1/TWT']
            discretesurfaceattribute = petrellink.surface_discrete_attributes['Input/TWT Surface/Subfolder/BCU 1/Facies']
            print(surfaceattribute.path)
            print(discretesurfaceattribute.path)
            
            #41123 Surface under subfolder
            surface1 = petrellink.surfaces['Input/TWT Surface/Subfolder/BCU 1']
            print(surface1.path)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_surface_surfaceattributes_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGridsGridpropertiesPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            #41183 'Models' included in the path
            model = petrellink.grids['Models/Structural grids/Model_Good']
            gridproperty = petrellink.grid_properties['Models/Structural grids/Model_Good/Properties/Rho']
            discretegridproperty = petrellink.discrete_grid_properties['Models/Structural grids/Model_Good/Properties/Facies']
            
            print(model.path)
            print(gridproperty.path)
            print(discretegridproperty.path)
            
            #41452 Grid property subfolders in the path
            gridproperty = petrellink.grid_properties['Models/Structural grids/Model_Good/Properties/Subfolder/Vs']
            discretegridproperty = petrellink.discrete_grid_properties['Models/Structural grids/Model_Good/Properties/Subfolder/Layers']
            
            print(gridproperty.path)
            print(discretegridproperty.path)
            
            gridproperty = petrellink.grid_properties['Models/Structural grids/Model_Good/Properties/Subfolder/Sub subfolder/Vp']
            discretegridproperty = petrellink.discrete_grid_properties['Models/Structural grids/Model_Good/Properties/Subfolder/Sub subfolder/Facies']
            
            print(gridproperty.path)
            print(discretegridproperty.path)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_grids_gridproperties_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionHorizonHorizonpropertiesPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            #41137 Horizon and horizon properties inside subfolder
            horizon1 = petrellink.horizon_interpretation_3ds['Input/Seismic/Interpretation folder 1/Subfolder/BCU 1/Ardmore 1']
            horizon2 = petrellink.horizon_interpretation_3ds['Input/Interpretation folder 2/Subfolder/BCU 1/Ardmore 1']
            horizon3 = petrellink.horizon_interpretation_3ds['Input/Interpretation folder 2/BCU/Ardmore']
            
            
            horizonproperty1 = petrellink.horizon_properties['Input/Seismic/Interpretation folder 1/Subfolder/BCU 1/Ardmore 1/TWT']
            horizonproperty2 = petrellink.horizon_properties['Input/Interpretation folder 2/Subfolder/BCU 1/Ardmore 1/TWT']
            horizonproperty3 = petrellink.horizon_properties['Input/Interpretation folder 2/BCU/Ardmore/TWT']
            
            horizon_interp1 = petrellink.horizon_interpretations['Input/Seismic/Interpretation folder 1/BCU']
            horizon_interp2 = petrellink.horizon_interpretations['Input/Interpretation folder 2/Subfolder/BCU 1']
            horizon_interp3 = petrellink.horizon_interpretations['Input/Interpretation folder 2/BCU']
            
            
            print(horizon1.path)
            print(horizon2.path)
            print(horizon3.path)
            
            print(horizonproperty1.path)
            print(horizonproperty2.path)
            print(horizonproperty3.path)
            
            print(horizon_interp1.path)
            print(horizon_interp2.path)
            print(horizon_interp3.path)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_horizon_horizonproperties_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionSeismic3dSeismic2dPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            #41144 2D seismic under subfolder
            seis2D = petrellink.seismic_lines['Input/Seismic/Survey 1/Subfolder/Seismic2D 1']
            print(seis2D.path)
            
            
            #41191 Virtual seismic cubes
            virtualcroppedvolume = petrellink.seismic_cubes['Input/Seismic/Ardmore/Seismic3D/Seismic3D [Crop] 1']
            virtualattributevolume = petrellink.seismic_cubes['Input/Seismic/Ardmore/Seismic3D/Seismic3D [PhaseShift]']
            virtualcalculatorvolume = petrellink.seismic_cubes['Input/Seismic/Ardmore/Seismic3D/NewSeis']
            print(virtualcroppedvolume.path)
            print(virtualattributevolume.path)
            print(virtualcalculatorvolume.path)
            
            
            
            #41110 Seismic cubes in subfolder
            seis3D1 = petrellink.seismic_cubes['Input/Seismic/Ardmore/Subfolder/Seismic3D 1']
            print(seis3D1.path)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_seismic3D_seismic2D_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionPropertycollectionsPaths(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            for i in sorted(petrellink.property_collections.keys()):
                print(i)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_propertycollections_paths_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGetpetrelobjectsbyguidsPythontooltestproject2(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            data_types = []
            
            data_types.append([item for path, item in sorted(list(petrellink.discrete_global_well_logs.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.discrete_grid_properties.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.discrete_grid_properties.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.discrete_surface_attributes.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.discrete_well_logs.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.global_well_logs.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.grid_properties.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.grids.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.horizon_interpretation_3ds.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.horizon_interpretations.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.horizon_properties.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.observed_data_sets.items()))])
            for odset in [item for path, item in sorted(list(petrellink.observed_data_sets.items()))]:
                data_types.append([od for od in sorted(list(odset.observed_data), key=lambda od: str(od))])
            data_types.append([item for path, item in sorted(list(petrellink.pointsets.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.polylinesets.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.grid_properties.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.property_collections.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.seismic_2ds.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.seismic_cubes.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.seismic_lines.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.surface_attributes.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.surface_discrete_attributes.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.surfaces.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.wavelets.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.well_logs.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.well_surveys.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.wells.items()))])
            data_types.append([item for path, item in sorted(list(petrellink.workflows.items()))])
            
            for data_type in data_types:
                for item in data_type:
                    obj = petrellink.get_petrelobjects_by_guids([item.droid])[0]
                    if (obj == None):
                        print("NoGuid:", item)
                    else:
                        print(item.droid == obj.droid and item.path == obj.path, item)
            
            #Invalid string returns None
            print(petrellink.get_petrelobjects_by_guids(["invalidstring"])[0], "invalidstring")
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_getpetrelobjectsbyguids_pythontooltestproject2_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGetpetrelobjectsbyguidsBoolError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            try:
                petrellink.get_petrelobjects_by_guids([True])
                print("failed")
            except Exception as e:
                print("ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_getpetrelobjectsbyguids_bool_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGetpetrelobjectsbyguidsIntError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            try:
                petrellink.get_petrelobjects_by_guids([2022])
                print("failed")
            except Exception as e:
                print("ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_getpetrelobjectsbyguids_int_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGetpetrelobjectsbyguidsNolistError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            try:
                petrellink.get_petrelobjects_by_guids(list(petrellink.wells.values())[0].droid)
                print("failed")
            except Exception as e:
                print("ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_getpetrelobjectsbyguids_nolist_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dClippedCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            seismic3d = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D_int8')
            seismic3d_copy = seismic3d.clone('Seismic3D_int8_copy', copy_values = False)
            import numpy as np
            chunk = seismic3d_copy.all()
            orig_arr = chunk.as_array()
            half_arr = np.ones_like(orig_arr)*0.5
            chunk.set(half_arr)
            set_arr = chunk.as_array()
            diff = np.sum((half_arr-set_arr)**2.0)**0.5
            print("{:1.0f}".format(np.sum(diff)))
            print(seismic3d_copy.retrieve_stats().get('Volume value format'))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_clipped_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        grid = petrellink._get_grid('Models/Structural grids/Model_Good')
        grid.readonly = True
        try:
            history_df = grid.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        prop.readonly = False
        try:
            history_df = prop.retrieve_history()
            first_row = history_df.iloc[0, :]
            print(first_row)
            
            old_value = prop.chunk((9,9),(10,10),(12,12)).as_array()
            prop.chunk((9,9),(10,10),(12,12)).set(1)
            prop.chunk((9,9),(10,10),(12,12)).set(old_value)
            
            history_df = prop.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        welllog = petrellink._get_global_well_log('Input/Wells/Global well logs/GR')
        welllog.readonly = False
        try:
            history_df = welllog.retrieve_history()
            print(history_df)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllog_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogdiscreteRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        welllog = petrellink._get_global_well_log('Input/Wells/Global well logs/Facies', discrete = True)
        welllog.readonly = False
        try:
            history_df = welllog.retrieve_history()
            print(history_df)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllogdiscrete_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        prop.readonly = False
        try:
            history_df = prop.retrieve_history()
            first_row = history_df.iloc[0, :]
            print(first_row)
            
            old_value = prop.chunk((9,9),(10,10),(12,12)).as_array()
            prop.chunk((9,9),(10,10),(12,12)).set(1)
            prop.chunk((9,9),(10,10),(12,12)).set(old_value)
            
            history_df = prop.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizoninterpretation3dRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        hor = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU/Ardmore')
        hor.readonly = False
        try:
            history_df = hor.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizoninterpretation3D_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        cube = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        cube.readonly = False
        try:
            history_df = cube.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            
            old_value = cube.chunk((9,9),(10,10),(12,12)).as_array()
            cube.chunk((9,9),(10,10),(12,12)).set(1)
            cube.chunk((9,9),(10,10),(12,12)).set(old_value)
            
            history_df = cube.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        line = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        line.readonly = False
        try:
            history_df = line.retrieve_history()
            first_row = history_df.iloc[0, :]
            print(first_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        surface = petrellink._get_surface('Input/TWT Surface/BCU')
        surface.readonly = False
        try:
            history_df = surface.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        surface_cont = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        surface_cont.readonly = False
        try:
            history_df = surface_cont.retrieve_history()
            print(history_df)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        surface_disc = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        surface_disc.readonly = False
        try:
            history_df = surface_disc.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        welllog = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vp')
        welllog.readonly = False
        try:
            history_df = welllog.retrieve_history()
            first_row = history_df.iloc[0, :]
            print(first_row)
            old_value_md = welllog.samples.at(5750).md
            old_value_value = welllog.samples.at(5750).value
            welllog.set_values([5750],[100])
            welllog.set_values([old_value_md],[old_value_value])
            history_df = welllog.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        welllog = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        welllog.readonly = False
        try:
            history_df = welllog.retrieve_history()
            first_row = history_df.iloc[0, :]
            print(first_row)
            old_value_md = welllog.samples.at(5750).md
            old_value_value = welllog.samples.at(5750).value
            welllog.set_values([5750],[100])
            welllog.set_values([old_value_md],[old_value_value])
            history_df = welllog.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        pointset = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        pointset.readonly = False
        try:
            history_df = pointset.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            df = pointset.as_dataframe()
            pointset.set_values(df)
            history_df = pointset.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        polylineset = petrellink._get_polylineset('Input/Geometry/Polygon')
        polylineset.readonly = False
        try:
            history_df = polylineset.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            positions = polylineset.get_positions(0)
            polylineset.set_positions(0, positions[0], positions[1], positions[2])
            history_df = polylineset.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetCloneRootOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            p1 = petrellink.polylinesets['Input/Polygon 0']
            p2 = p1.clone("polygon 0_clone", copy_values = False)
            print(p2)
            p3 = p1.clone("polygon 0_clone with values", copy_values = True)
            print(p3)
            p4 = p2.clone("polygon 0_clone_clone", copy_values = False)
            print(p4)
            #p5 = p2.clone("polygon 0_clone_clone with values", copy_values = True) #Bug 42482
            #print(p5)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_clone_root_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WaveletBasic(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_wavelet('Input/Wavelet 1')
        var.readonly = False
        try:
            def format_arr(arr):
                return "\n".join(["{:.2f}".format(v) for v in arr])
            
            def format_float(f):
                return "{:.2f}".format(f)
            
            orig_amps = var.amplitudes
            print(format_arr(orig_amps[0:50:5]))
            orig_sample_count = var.sample_count
            print(orig_sample_count)
            orig_sampling_interval = var.sampling_interval
            print(format_float(orig_sampling_interval))
            orig_sampling_start = var.sampling_start
            print(format_float(orig_sampling_start))
            orig_sample_points = var.sample_points
            print(format_arr(orig_sample_points[0:50:5]))
            print(var.time_unit_symbol)
            df = var.as_dataframe()
            df.describe()
            var.set(orig_amps[0:50:5])
            print(format_arr(var.amplitudes))
            print(format_arr(var.sample_points))
            print(var.sample_count)
            print(format_float(var.sampling_interval))
            print(format_float(var.sampling_start))
            var.set(orig_amps[0:50:5], 10.0)
            print(format_arr(var.amplitudes))
            print(format_arr(var.sample_points))
            print(var.sample_count) 
            print(format_float(var.sampling_interval)) 
            print(format_float(var.sampling_start))
            var.set(orig_amps[0:50:5], 5.0, 2.5)
            print(format_arr(var.amplitudes))
            print(format_arr(var.sample_points))
            print(var.sample_count) 
            print(format_float(var.sampling_interval))
            print(format_float(var.sampling_start))
            var.set(orig_amps, orig_sampling_start, orig_sampling_interval)
            print(format_arr(var.amplitudes[0:50:5]))
            print(format_arr(var.sample_points[0:50:5]))
            print(var.sample_count)
            print(format_float(var.sampling_interval))
            print(format_float(var.sampling_start))
            print(var.retrieve_stats())
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wavelet_basic_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WaveletCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        wavelet = petrellink._get_wavelet('Input/Wavelet 1')
        wavelet.readonly = False
        try:
            print(wavelet.path)
            print(wavelet.droid)
            
            
            new_wavelet_no_copy = wavelet.clone("new_property_no_copy_clone", copy_values=False)
            new_wavelet_do_copy = wavelet.clone("new_property_do_copy_clone", copy_values=True)
            
            not_copied_values = new_wavelet_no_copy.amplitudes
            copied_values = new_wavelet_do_copy.amplitudes
            orig_values = wavelet.amplitudes
            
            for i in [i*5 for i in range(5)]:
                    print("{:.2f}, {:.2f}".format(orig_values[i], copied_values[i]))
            
            print(not_copied_values)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wavelet_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WaveletRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        wavelet = petrellink._get_wavelet('Input/Wavelet 1')
        wavelet.readonly = False
        try:
            history_df = wavelet.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            old_amplitudes = wavelet.amplitudes
            modified_amplitudes = wavelet.amplitudes
            modified_amplitudes[0] = 1
            wavelet.set(modified_amplitudes)
            wavelet.set(old_amplitudes)
            history_df = wavelet.retrieve_history()
            last_row = history_df.iloc[-1, -1]
            print(last_row)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wavelet_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WaveletSetter(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_wavelet('Input/Wavelet 1')
        var.readonly = False
        try:
            def format_arr(arr):
                return "\n".join(["{:.2f}".format(v) for v in arr])
            
            def format_float(f):
                return "{:.2f}".format(f)
            
            orig_amps = var.amplitudes
            print(format_arr(orig_amps[0:50:5]))
            orig_sample_count = var.sample_count
            print(orig_sample_count)
            orig_sampling_interval = var.sampling_interval
            print(format_float(orig_sampling_interval))
            orig_sampling_start = var.sampling_start
            print(format_float(orig_sampling_start))
            orig_sample_points = var.sample_points
            print(format_arr(orig_sample_points[0:50:5]))
            print(var.time_unit_symbol)
            df = var.as_dataframe()
            df.describe()
            var.amplitudes = orig_amps[0:50:5]
            print(format_arr(var.amplitudes))
            print(format_arr(var.sample_points))
            print(var.sample_count)
            print(format_float(var.sampling_interval))
            print(format_float(var.sampling_start))
            var.sampling_start = 10.0
            print(format_arr(var.amplitudes))
            print(format_arr(var.sample_points))
            print(var.sample_count) 
            print(format_float(var.sampling_interval)) 
            print(format_float(var.sampling_start))
            var.sampling_start = 5.0
            var.sampling_interval = 2.5
            print(format_arr(var.amplitudes))
            print(format_arr(var.sample_points))
            print(var.sample_count) 
            print(format_float(var.sampling_interval))
            print(format_float(var.sampling_start))
            var.amplitudes = orig_amps
            var.sampling_start = orig_sampling_start
            var.sampling_interval = orig_sampling_interval
            print(format_arr(var.amplitudes[0:50:5]))
            print(format_arr(var.sample_points[0:50:5]))
            print(var.sample_count)
            print(format_float(var.sampling_interval))
            print(format_float(var.sampling_start))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wavelet_setter_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetClear(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            poly = petrellink.polylinesets["Input/Geometry/Polygon"]
            polyclone = poly.clone("Poly clone clear", True)
            polyclone.clear()
            print([v for v in polyclone.polylines])
            polyclone_noval = poly.clone("Poly clone clear noval", False)
            polyclone_noval.clear()
            print([v for v in polyclone_noval.polylines])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_clear_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetEmptyClone(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            polygon = petrellink.polylinesets["Input/Geometry/Polygon"]
            poly = polygon.clone("New Empt test polygon", False)    #this poly has no attributes
            poly.clone('Some other enmpty polygon', True)     #here the exception is raised
            print(poly)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_empty_clone_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Workflows(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            # Get workflow:
            copy_to_wf = petrellink.workflows['Workflows/copy_to']
            
            # Get reference variables:
            copy_to_input = copy_to_wf.input["input_var"]
            copy_to_output = copy_to_wf.output["output_var"]
            
            # Get some target object
            ps = petrellink.pointsets['Input/Geometry/Points 1']
            
            # Run workflow with arguments
            result = copy_to_wf.run({copy_to_input: ps, "$name":"NameFromRunWithArgs"})
            
            # Get target of output reference variable
            output_target = result[copy_to_output]
            
            # Print the two generated python objects:
            print(output_target)
            
            shift_down_wf = petrellink.workflows['Workflows/shift_down']
            shift_down_input = shift_down_wf.input["input_var"]
            shift_down_output = shift_down_wf.output["output_var"]
            
            make_thickness_map_wf = petrellink.workflows['Workflows/make_thickness_map']
            make_thickness_map_input_top = make_thickness_map_wf.input["input_top"]
            make_thickness_map_input_base = make_thickness_map_wf.input["input_base"]
            make_thickness_map_output = make_thickness_map_wf.output['output_map']
            
            # Put together
            def copy_object(o, name):
                result = copy_to_wf.run({copy_to_input: o, "$name":name})
                return result[copy_to_output]
            
            def shift_down(o):
                result = shift_down_wf.run({shift_down_input: o})
                return result[shift_down_output]
            
            def make_thickness_map(top, base):
                result = make_thickness_map_wf.run({make_thickness_map_input_top: top, make_thickness_map_input_base: base})
                return result[make_thickness_map_output]
            
            def complete_job(ps):
                top = copy_object(ps, "top")
                base = copy_object(ps, "base")
                base_shifted = shift_down(base)
                return make_thickness_map(top, base)
            
            sur = petrellink.surfaces['Input/TWT Surface/BCU']
            print(complete_job(sur))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\workflows_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_ObserveddataBasic(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_observed_data_set('Input/Wells/Well_Good/Observed')
        var.readonly = True
        try:
            
            # Print observed data from observed data sets
            for od in var.observed_data:
                print(od)
            
            #check type of var.observed_data
            print(type(var.observed_data))
            
            # Select an observed data from the set
            observed_data = var.observed_data[3]
            
            # Basics
            parent_set = observed_data.observed_data_set
            print(parent_set)
            print(observed_data.petrel_name)
            print(observed_data.unit_symbol)
            
            # Observed data as dataframe
            df = observed_data.as_dataframe()
            print(df.shape[0]) # 2 - Date and type of obsereved data
            print(df.shape[1] == len(parent_set.dates))
            
            # Get values
            orig_values = observed_data.values
            len_orig_values = len(orig_values)
            print(len_orig_values)
            print(orig_values[0])
            print(orig_values[len_orig_values-1])
            
            # Set values
            new_values = [123]*len_orig_values
            observed_data.set_values(new_values)
            after_new_values = observed_data.values
            len_new_values = len(after_new_values)
            print(len_new_values)
            print(after_new_values[0])
            print(after_new_values[len_new_values-1])
            
            # Reset
            observed_data.set_values(orig_values)
            after_reset = observed_data.values
            len_after_reset = len(after_reset)
            print(len_after_reset)
            print(after_reset[0])
            print(after_reset[len_after_reset-1])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\observeddata_basic_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_ObserveddatasetBasic(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_observed_data_set('Input/Wells/Well_Good/Observed')
        var.readonly = True
        try:
            print(var.petrel_name)
            print(var.well)
            
            df = var.as_dataframe()
            
            for col in df.columns:
                print(col)
            
            ods = var.observed_data
            for od in ods:
                print(od)
            
            len_ods = len(ods)
            num_cols = df.shape[1] - 1 # Subtract Date column in df
            print(len_ods == num_cols)
            
            num_rows = df.shape[0] # num rows
            num_dates = len(var.dates)
            print(num_rows == num_dates)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\observeddataset_basic_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_ObserveddatasetAppendRow(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_observed_data_set('Input/Wells/Well_Good/Observed')
        var.readonly = True
        try:
            orig_dates = var.dates
            len_before_append = len(orig_dates)
            last_date = orig_dates[len_before_append-1]
            print(len_before_append)
            print(orig_dates[0])
            print(last_date)
            
            import datetime
            next_date = last_date + datetime.timedelta(days=31)
            print('Append')
            print(next_date) # Next date to append
            
            ods = var.observed_data
            new_vals = [55]*len(ods)
            var.append_row(next_date, ods, new_vals) # Append new data with observed data order and new values
            
            dates_after_append = var.dates
            len_dates_after_append = len(dates_after_append)
            print(len_dates_after_append)
            print(dates_after_append[0]) # First date
            print(dates_after_append[len_dates_after_append-1]) # New last date
            
            # TODO: Have not found a way to remove the appended data yet = Reset. Ocean API is not helpful. Please add if you can find a way to do it
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\observeddataset_append_row_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_ObserveddatasetAddobserveddata(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_observed_data_set('Input/Wells/Well_Good/Observed')
        var.readonly = True
        try:
            ods = var.observed_data
            print(len(ods))
            
            data_for_add = [12]*len(var.dates)
            selected_id = petrellink.predefined_global_observed_data['Water injection rate']
            added = var.add_observed_data(selected_id, data_for_add)
            print(added)
            
            print(len(var.observed_data))
            
            # Reset
            delete_workflow = petrellink.workflows['Workflows/New folder/delete_object']
            object = delete_workflow.input['object']
            result = delete_workflow.run({object: added})
            
            ods = var.observed_data
            print(len(ods))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\observeddataset_addobserveddata_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalobserveddataPredefined(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            predefined_dict = petrellink.predefined_global_observed_data.items()
            print(type(predefined_dict))
            print(len(predefined_dict) > 0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalobserveddata_predefined_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellObserveddatasets(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well('Input/Wells/Well_Good')
        var.readonly = False
        try:
            for ods in var.observed_data_sets:
                print(ods)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\well_observeddatasets_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))

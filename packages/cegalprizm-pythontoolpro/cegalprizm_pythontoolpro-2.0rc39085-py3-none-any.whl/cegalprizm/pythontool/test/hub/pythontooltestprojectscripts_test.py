# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import io
import os
import sys
from cegalprizm.pythontool.test.hub.petreltestcase import PetreltestUnitCase
from cegalprizm.pythontool import PetrelConnection


class PythonToolTestProjectScriptsTest(PetreltestUnitCase):
    _project: str = fr'{os.environ["home"]}/Documents\PetrelUnitTestFramework\1\PythonToolTestProject\PythonToolTestProject.pet'
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)



    def test_HorizonParents(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        horizon_interpretation = petrellink._get_horizon_interpretation('Input/Seismic/Interpretation folder 1/BCU')
        horizon_interpretation.readonly = False
        horizon_interpretation_3d = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU/Ardmore')
        horizon_interpretation_3d.readonly = False
        try:
            horizon_attribute = horizon_interpretation_3d.horizon_property_3ds[1]
            
            if horizon_attribute.horizon_interpretation_3d.petrel_name != horizon_interpretation_3d.petrel_name:
                print(f"{horizon_attribute.horizon_interpretation_3d.petrel_name} != {horizon_interpretation_3d.petrel_name}")
                print(False)
            if horizon_interpretation_3d.horizon_interpretation.petrel_name != horizon_interpretation.petrel_name:
                print(f"{horizon_interpretation_3d.horizon_interpretation.petrel_name} != {horizon_interpretation.petrel_name}")
                print(False)
            if horizon_attribute.horizon_interpretation_3d.petrel_name == horizon_interpretation_3d.petrel_name and horizon_interpretation_3d.horizon_interpretation.petrel_name == horizon_interpretation.petrel_name:
                print(True)
            else:
                print(False)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizon_parents_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




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




    def test_WelllogdiscreteAsDataframe(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        facies = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        facies.readonly = False
        try:
            facies_values = facies.as_dataframe()
            print(facies_values.iloc[7500:7505,3:7])
            
            import copy
            old = copy.deepcopy(facies.samples)
            
            facies.set_values([], [])
            
            print(facies.as_dataframe().iloc[7500:7505,3:7])
            
            facies.samples = old
            facies_values = facies.as_dataframe()
            print(facies_values.iloc[7500:7505,3:7])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_as_dataframe_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteSamplesCount(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        var.readonly = False
        try:
            print(len(var.samples))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_samples_count_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteSetEmpty(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        var.readonly = False
        try:
            import copy
            old = copy.deepcopy(var.samples)
            try:
                var.set_values([], [])
                print(len(var.samples))
            finally:
                var.samples = old
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_set_empty_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteWell(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        facies = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        facies.readonly = False
        try:
            print(facies.well)
            print(facies.global_well_log)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_well_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteSamplesValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        var.readonly = False
        try:
            print(var.samples[7400:7402])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_samples_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteSamplesValues2017(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)
        var.readonly = False
        try:
            print(var.samples[7400:7402])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_samples_values_2017_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteChunkError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Layers', discrete = True)
        prop.readonly = False
        try:
            try:
                prop.chunk((70,200),(40,45),(150,155))
            except Exception as err:
                print(err)
                print('---')
                
            try:
                prop.chunk((150,160),(40,45),(150,900))
            except Exception as err:
                print(err)
                print('---')
                
            try:
                prop.chunk((70,60),(40,45),(150,155))
            except Exception as err:
                print(err)
                print('---')
                
            try:
                prop.chunk((70,202),(40,45),(150,155))
            except Exception as err:
                print(err)
                print('---')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_chunk_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteChunkSetDf(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Crazy/Properties/Facies', discrete = True)
        prop.readonly = False
        try:
            print(prop.readonly)
            
            chunk = prop.chunk((10,15),(50,55),(500,505))
            df_to_reset_values = chunk.as_dataframe()
            
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = 2
            
            #set with df - correct input
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().iloc[100:103])
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().iloc[100:103])
            
            #Try set non-integer values -should raise ValueError
            df.loc[:,'Value_new'] = 2.05
            try:
                chunk.set(df, 'Value_new')
            except ValueError as err:
                print(err)
            print(chunk.as_dataframe().iloc[100:103])
            
            df.loc[:,'Value_new'] = 2
            
            
            #rename columns in df
            column_names = ["X", "J", "K", "Value1", "Value_new"]
            zip_iterator = zip(df.columns.to_list(), column_names)
            a_dictionary = dict(zip_iterator)
            
            df.rename(columns=a_dictionary, inplace = True)
            
            #set with df - incorrect input - no default 'Value' column in df
            print(df.columns.to_list())
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
                
            #set with df - incorrect input - no specified column 'Col'
            print(df.columns.to_list())
            try:
                chunk.set(df, 'Col')
            except Exception as err:
                print(err)
                
            #rename columns
            column_names = ["X", "Y", "Z", "Value", "Value_new"]
            zip_iterator = zip(df.columns.to_list(), column_names)
            a_dictionary = dict(zip_iterator)
            
            df.rename(columns=a_dictionary, inplace = True)
            
            #set with df - correct input but no columns I, J, K in df
            print(df.columns.to_list())
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
            #rename columns
            column_names = ["i", "j", "k", "Value", "Value_new"]
            zip_iterator = zip(df.columns.to_list(), column_names)
            a_dictionary = dict(zip_iterator)
            
            df.rename(columns=a_dictionary, inplace = True)
            
            df_backup = df
            df.drop(labels=df.index[0], inplace = True)
            
            #set with df - incorrect input - no. of rows
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
            df = df_backup
            df.drop(labels=df.index[-1], inplace = True)
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
                
            df = df_backup
            df.drop(labels=df.index[-100], inplace = True)
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
            chunk.set(df_to_reset_values)
            print(chunk.as_dataframe().iloc[100:103])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_chunk_set_df_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteLayer(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            
            original_vals = var.layer(5).as_array()
            
            #Sets the layer value to '1
            for (i,j,k,val) in var.layer(5).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                if i == 0:
                    break
            
            var.layer(5).set(1)
            
            
            for (i,j,k,val) in var.layer(5).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                if i == 0:
                    break
            
            # reset the value
            var.layer(5).set(original_vals)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_layer_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridCoordsextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #prints the world co-ordinates of the Grid
            print(var.coords_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_coordsextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridExtent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #Prints the number of cells in i, j, k directions
            
            print((var.extent.i))
            print((var.extent.j))
            print((var.extent.k))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_extent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridGridvertices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #prints the values are the 8 vertices of the cell, by importing Grid "Vertices"
            from cegalprizm.pythontool import vertices
            
            verts = var.vertices(1,1,1)
            print((len(verts)))
            
            print ('\n'.join([str(v) for v in verts]))
            
            
            #---OR---
            #for index in range(length):
                #print verts[index]
                
            #print verts[vertices.BaseSouthWest]
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_gridvertices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridIndicesValueError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #ValueErrorException is thrown when position is not in the grid
            print(var.indices(38130, 6223703, -8853))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_indices_value_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridIsundefFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #Returns False is the cell is undefined at the given indices
            print(var.is_undef_cell(1,1,1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_isundef_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridPetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridPosition(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            # The position of the cell center in world co-ordinates is printed
            print(var.position(1, 1, 1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_position_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridPositionValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #ValueError is thrown if (i,j,k) is outside the grid
            print(var.position(-1, 1, 1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_position_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            stats = var.retrieve_stats()
            
            print('\n', stats['X Min'])
            print('\n', stats['Y Max'])
            print('\n', stats['Elevation depth [ft] Delta'])
            print('\n', stats['Number of properties'])
            print('\n', stats['Total number of grid cells'])
            print('\n', stats['Number of geological layers'])
            print('\n', stats['Total number of 2D nodes'])
            print('\n', stats['Rotation angle'])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridVertices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #Prints the position at the 8 verticies of a cell at given (i,j,k)
            print([str(v) for v in var.vertices(1,1,1)])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_vertices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridVerticesunchecked(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #Returns the position of the vertices of the cell
            print([str(v) for v in var.vertices_unchecked(1,1,1)])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_verticesunchecked_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridVerticesuncheckedValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #ValueError if the cell is outside the grid
            print(var.vertices_unchecked(1,1,-1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_verticesunchecked_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridVerticesValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #ValueError is output when the cell vertices does not exist
            print(var.vertices(1,1,-1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_vertices_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridIndices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            #Returns the Indices of the cell at the given (x,y,z) co-ordinates
            print(var.indices(483310, 6225090, -8852))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_indices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridProperties(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid('Models/Structural grids/Model_Good')
        var.readonly = True
        try:
            print(len(var.properties))
            for sur in var.properties:
                print(sur)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grid_properties_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyChunkSetDf(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        prop.readonly = False
        try:
            print(prop.readonly)
            
            chunk = prop.chunk((10,15),(50,55),(500,505))
            df_to_reset_values = chunk.as_dataframe()
            
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = df.loc[:,'Value'] * 2
            
            #set with df - correct input
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().iloc[100:103])
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().iloc[100:103])
            
            #rename columns in df
            column_names = ["X", "J", "K", "Value1", "Value_new"]
            zip_iterator = zip(df.columns.to_list(), column_names)
            a_dictionary = dict(zip_iterator)
            
            df.rename(columns=a_dictionary, inplace = True)
            
            #set with df - incorrect input - no default 'Value' column in df
            print(df.columns.to_list())
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
                
            #set with df - incorrect input - no specified column 'Col'
            print(df.columns.to_list())
            try:
                chunk.set(df, 'Col')
            except Exception as err:
                print(err)
                
            #rename columns
            column_names = ["X", "Y", "Z", "Value", "Value_new"]
            zip_iterator = zip(df.columns.to_list(), column_names)
            a_dictionary = dict(zip_iterator)
            
            df.rename(columns=a_dictionary, inplace = True)
            
            #set with df - correct input but no columns I, J, K in df
            print(df.columns.to_list())
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
            #rename columns
            column_names = ["i", "j", "k", "Value", "Value_new"]
            zip_iterator = zip(df.columns.to_list(), column_names)
            a_dictionary = dict(zip_iterator)
            
            df.rename(columns=a_dictionary, inplace = True)
            
            df_backup = df
            df.drop(labels=df.index[0], inplace = True)
            
            #set with df - incorrect input - no. of rows
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
            df = df_backup
            df.drop(labels=df.index[-1], inplace = True)
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
                
            df = df_backup
            df.drop(labels=df.index[-100], inplace = True)
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
            chunk.set(df_to_reset_values)
            print(chunk.as_dataframe().iloc[100:103])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_df_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyChunkSetDfReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        prop.readonly = True
        try:
            print(prop.readonly)
            chunk = prop.chunk((10,15),(50,55),(500,505))
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = df.loc[:,'Value'] * 2
            
            #set with df - correct input on readonly chunk
            print(df.columns.to_list())
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_df_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyChunkError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        prop.readonly = False
        try:
            try:
                prop.chunk((70,200),(40,45),(150,155))
            except Exception as err:
                print(err)
                print('---')
                
            try:
                prop.chunk((150,160),(40,45),(150,900))
            except Exception as err:
                print(err)
                print('---')
                
            try:
                prop.chunk((70,60),(40,45),(150,155))
            except Exception as err:
                print(err)
                print('---')
                
            try:
                prop.chunk((70,202),(40,45),(150,155))
            except Exception as err:
                print(err)
                print('---')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyColumns(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            original_column_00 = var.column(0, 0).as_array()
            original_column_01 = var.column(0, 1).as_array()
            original_column_10 = var.column(1, 0).as_array()
            original_column_11 = var.column(1, 1).as_array()
            
            #sets the value to 0 for islice = 0 & 1, can see the change in 3D window
            for col in var.columns(irange=list(range(0, 2)), jrange=None):
                col.set(0)
                    
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
            
            for (i,j,k, val) in var.column(1,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                
            for (i,j,k, val) in var.column(2,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
            
            # Reset values
            var.column(0, 0).set(original_column_00)
            var.column(0, 1).set(original_column_01)
            var.column(1, 0).set(original_column_10)
            var.column(1, 1).set(original_column_11)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_columns_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyColumnsvalueerrorIrange(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #ValueError is thrown if i-index of slice is inavlid
            for col in var.columns(irange=list(range(-1, 1)), jrange=list(range(0,1))):
                col.set(0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_columnsvalueerror_irange_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyColumnsvalueerrorJrange(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #ValueError is thrown if jrange index is not valid
            for col in var.columns(irange=list(range(0, 1)), jrange=list(range(-1,1))):
                col.set(0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_columnsvalueerror_jrange_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyColumnvalueerrorI(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #ValueError is thrown if i-index is not valid
            for (i,j,k, val) in var.column(-1,0).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_columnvalueerror_i_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyColumnvalueerrorJ(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #ValueError is thrown if j-index is not valid
            for (i,j,k, val) in var.column(0,-1).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_columnvalueerror_j_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyHassameparent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        var_1 = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var_1.readonly = False
        try:
            #Returns True if the two properties have same parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_hassameparent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyHassameparentFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        var_1 = petrellink._get_grid_property('Models/Structural grids/Model_Crazy/Properties/Por')
        var_1.readonly = False
        try:
            #Prints False if the objects have different parents
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_hassameparent_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyHassameparentValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        var_1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var_1.readonly = False
        try:
            #ValueError is thrown when ModelProperty > Vp is compared with Seismic 3D for same parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_hassameparent_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyIsundefvalueFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #Returns False if the number is not "NAN"
            #[0, 0, 0] == 2147483647]
            
            with var.column(0,0).values() as vals:
                vals[0] = 55
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k==0:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                    print(var.is_undef_value(val))
                    break;
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_isundefvalue_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyIsundefvalueTrue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #returns True is the value is 'nan'
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 10:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                    print(var.is_undef_value(val))
                    break;
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_isundefvalue_true_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyLayer(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        var.readonly = False
        try:
            #changes the layer value, can see the changes in 3D window
            for (i,j,k, val) in var.layer(5).enumerate():
                if i == 0:
                    oldval = val
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                    break;
                
            var.layer(5).set(0.11)
                
            for (i,j,k, val) in var.layer(5).enumerate():
                if i == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                    break;
            
            # reset so next test doesn't break
            var.layer(5).set(oldval)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyLayers(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #sets the K-slice cells to zero, can see the top layer change in 3D window
            
            originals = []
            for layer in var.layers(list(range(0,1))):
                originals.append(layer.as_array())
                layer.set(0)
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
            
            # Reset values
            ii = 0
            for layer in var.layers(list(range(0,1))):
                layer.set(originals[i])
                i += 1
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layers_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyLayersvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #ValueError is thrown if k-index is not valid
            for layer in var.layers(list(range(-1,1))):
                layer.set(0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layersvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyLayervalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #ValueError is thrown if k-index is invalid
            var.layer(-5).set(0.11)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layervalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyObjectextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #prints the extent of the slice
            print(var.column(0,0).object_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_objectextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyParentcollection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            print(var.parent_collection)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_parentcollection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyParentgrid(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            print(var.grid)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_parentgrid_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyPetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            #prints the petrel name of the parent
            print(var.grid.petrel_name)
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = True
        try:
            #cannot update a Grid property when 'Read only' is checked
            with var.column(0,0).values() as vals:
                vals[0] = 1.23 
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertySetundefvalue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        var.readonly = False
        try:
            
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 0:
                    oldval = val
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val)) #Expected is [0, 0, 0] == 0] why??
                    print(var.is_undef_value(val))
                    break;
             
             #Reset the value to 'undef value'       
            with var.column(0,0).values() as vals:
                vals[0] = var.undef_value
            
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                    print(var.is_undef_value(val))
                    break;
            
            #reset the value back so following test can pass
            with var.column(0,0).values() as vals:
                vals[0] = oldval
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_setundefvalue_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertySliceclone(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            #trutned object as same values as the original slice
            
            for (i, j, k, val) in var.column(5,5).enumerate():
                if  k ==0:
                    print("[{0} {1} {2}] => {3:.6f}".format(i, j, k, val))
                    break;
                    
            for (i, j, k, val) in var.column(6,5).enumerate():
                if  k ==0:
                    oldval = val
                    print("[{0} {1} {2}] => {3:.6f}".format(i, j, k, val))
                    break;
            
            average_layer = var.column(5,5).clone()
            var.column(6,5).set(average_layer)
            
            for (i, j, k, val) in var.column(6,5).enumerate():
                if  k ==0:
                    print("[{0} {1} {2}] => {3:.6f}".format(i, j, k, val))
                    break;
            
            
            var.column(6,5).set(oldval)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_sliceclone_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertySlicedisconnectedTrue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            #Prints True if the Slice is disconnected
            #[0 1 1] => 0.121630; [0 1 2] => 0.151024...[0 1 3] => 0.136327 because (0.121630+0.151024)/2=0.136327
            
            print(var.layer(3).disconnected)
            for (i, j, k, val) in var.layer(1).enumerate():
                if j == 1:
                    print("[%d %d %d] => %f" % (i, j, k, val))
                    break;
            
            for (i, j, k, val) in var.layer(2).enumerate():
                if j == 1:
                    print("[%d %d %d] => %f" % (i, j, k, val))
                    break;
            
            sum_layer = var.layer(1) + var.layer(2)
            average_layer = sum_layer / 2.0
            var.layer(3).set(average_layer)
            
            for (i, j, k, val) in var.layer(3).enumerate():
                if  j ==1:
                    print("[%d %d %d] => %f" % (i, j, k, val))
                    break;
            
            print(average_layer.disconnected)
            print(var.layer(3).disconnected)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_slicedisconnected_true_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyUnitsymbol(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #reutns the Units for the Model property
            print(var.unit_symbol)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_unitsymbol_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyUpdaterawvalues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        var.readonly = False
        try:
            #update the cell value at a given i,j,k
            original = var.column(0,0).as_array()
            
            with var.column(0,0).values() as vals:
                vals[0] = 1.23  
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                if k == 0:
                    break
            
            # Reset values
            var.column(0,0).set(original)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_updaterawvalues_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyUpscaledcellsComplete(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        var.readonly = False
        try:
            try:
                is_oop
            except NameError:
                is_oop = False
            
            if is_oop:
                from cegalprizm.pythontool.primitives import Indices
            
            old_upscaled_cells = var.upscaled_cells
            
            print(len(var.upscaled_cells)) # 2942 for Vs [U]
            var.upscaled_cells = [Indices(1,1,1), Indices(2,2,2)]
            print(len(var.upscaled_cells)) # 2
            print(var.upscaled_cells[1].k) # 2
            var.upscaled_cells = None
            print(len(var.upscaled_cells)) # 0
            
            #restore for next test
            var.upscaled_cells = old_upscaled_cells
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_upscaledcells_complete_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteArithmeticforbidden(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #Arithmetic on discrete slices is forbidden
            try:
                var.layer(1).set(var.layer(1)+2)
                print(False)
            except ValueError as v:
                print("Arithmetic operations are not allowed for chunks of discrete values" in str(v))
                
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_arithmeticforbidden_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteColumns(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            original_vals = dict()
            
            for i in range(0, 2):
                for j in range(0, 1):
                    original_vals[i, j] = var.column(i, j).as_array()
            
            #Values are set in the given irange & jrange
            for col in var.columns(irange=list(range(0, 2)), jrange=list(range(0,1))):
                col.set(0)
                
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
            
            for (i,j,k, val) in var.column(1,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                
            for (i,j,k, val) in var.column(2,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
            
            for i in range(0, 2):
                for j in range(0, 1):
                    var.column(i, j).set(original_vals[i, j])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_columns_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteColumnsvalueerrorIrange(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown when i-index is invalid
            for col in var.columns(irange=list(range(-1, 1)), jrange=None):
                col.set(0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_columnsvalueerror_irange_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteColumnsvalueerrorJrange(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown when j-index is invalid
            for col in var.columns(irange=list(range(0, 1)), jrange=list(range(-1,1))):
                col.set(0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_columnsvalueerror_jrange_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteColumnvalueerrorI(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown if i-index is invalid
            for (i,j,k, val) in var.column(-1,0).enumerate():
                if k == 0 or k==1:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_columnvalueerror_i_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteColumnvalueerrorJ(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown when j-index is invalid
            for (i,j,k, val) in var.column(0,-1).enumerate():
                if k == 0 or k==1:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_columnvalueerror_j_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteDiscretecode(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #Discrete code is changed from 'Fine sand' to 'Sand sand'. This does not affect the Petrel object
            var.discrete_codes[1] = "Sand sand"
            print(var.discrete_codes)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_discretecode_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteHassameparent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        var_1 = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Layers', discrete = True)
        var_1.readonly = False
        try:
            #Prints True if the objects have same parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_hassameparent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteHassameparentFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        var_1 = petrellink._get_grid_property('Models/Structural grids/Model_Crazy/Properties/Facies', discrete = True)
        var_1.readonly = False
        try:
            #Prints False if the objects have different parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_hassameparent_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteHassameparentValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        var_1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var_1.readonly = False
        try:
            #ValueError is thrown when DiscreteGridProperty is compared with Seismic 3D
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_hassameparent_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteIsundef(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #Returns False if the value is not a 'nan' for Discrete Model property
            for (i,j,k, val) in var.column(0,0).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                if k == 0:
                    print(var.is_undef_value(val))
                    break;
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_isundef_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteIsundefvalueFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            original_vals = var.column(0, 0).as_array()
            
            #Prints False because the value is set to a non-undef value for Discrete property
            with var.column(0,0).values() as vals:
                vals[0] = 55
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k==0:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                    print(var.is_undef_value(val))
                    break;
            
            var.column(0, 0).set(original_vals)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_isundefvalue_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteIsundefvalueTrue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #Returns False if the value is not a 'nan' or 'MAX_INT'=2147483647 for Discrete Model property
            for (i,j,k, val) in var.column(1,1).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val)) #value returned 241400000 hence failing
                if k == 0:
                    print(var.is_undef_value(val))
                    break;
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_isundefvalue_true_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteLayers(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            original_vals = dict()
            
            for k in range(2, 3):
                original_vals[k] = var.layer(0).as_array()
            
            #Cells in layers 2 and 3 are all set to 66, can see the change in 3D Window
            for layer in var.layers(krange=(2,3)):
                layer.set(66)
                
            for (i,j,k, val) in var.column(78,53).enumerate():
                if k==1 or k==2 or k==3 or k==4:
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                    
            for k in range(2, 3):
                var.layer(0).set(original_vals[k])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_layers_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteLayersvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown if k-index is invalid
            for layer in var.layers(list(range(-1,1))):
                layer.set(0)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_layersvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteLayervalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown when k-index is invalid
            var.layer(-5).set(1)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_layervalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteParentcollection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            print(var.parent_collection)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_parentcollection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteParentgrid(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            print(var.grid)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_parentgrid_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscretePetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #prints Petrel name
            print(var.petrel_name)
            print(var.grid.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = True
        try:
            #Cannot overwrite the values when 'Read only' is checked on
            with var.column(0,0).values() as vals :
                vals[0] = 111
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = True
        try:
            print(var.retrieve_stats()['Max'])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteSetundefvalue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #First set the value to a 'not undef' value
            with var.column(0,0).values() as vals:
                original_val = vals[0]
                vals[0] = int(1) 
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if (not var.is_undef_value(val)):
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val) + " value is not undef")
                    break
            
            #set the value to an 'undef' value 
            with var.column(0,0).values() as vals:
                vals[0] = var.undef_value
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if (var.is_undef_value(val)):
                    print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val) + " value is undef")
                    break
            
            with var.column(0,0).values() as vals:
                vals[0] = original_val
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_setundefvalue_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteUnitsymbol(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #print None for Facies - a discrete Grid Property template
            print(var.unit_symbol)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_unitsymbol_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteUpdaterawvalues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            #update the cell value at a given i,j,k for a Discrete Grid proeprty
            with var.column(0,0).values() as vals:
                original_val = vals[0]
                vals[0] = 1.23  
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                print("[{0}, {1}, {2}] == {3}]".format(i,j,k,val))
                if k == 0:
                    break;
            
            with var.column(0,0).values() as vals:
                vals[0] = original_val
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_updaterawvalues_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizoninterpretation3d(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU/Ardmore')
        var.readonly = False
        try:
            try:
                is_oop
            except NameError:
                is_oop = False
            
            ok = True
            if var.sample_count != 120908:
                ok = False
                print("var.sample_count != 120908\n")
                print(var.sample_count)
            if str(var) != "HorizonInterpretation3D(petrel_name=\"Ardmore\")":
                ok = False
                print("str(var) != \"HorizonInterpretation3D(petrel_name=\"Ardmore\")\"")
            if var.unit_symbol != "ms":
                ok = False
                print("var.unit_symbol != \"ms\"")
            if int(var.position(20, 30).x) != 486458:
                ok = False
                print("int(var.position(20, 30).x) != 486458\n")
                print(int(var.position(20, 30).x))
            if var.indices(486288.6570124189, 6223608.341706959).i != 30:
                ok = False
                print("var.indices(486288.6570124189, 6223608.341706959).i != 30")
                print(var.indices(486288.6570124189, 6223608.341706959).i)
            
            chunk_0 = var.chunk((4,5), (4, 5))
            data = chunk_0.as_array().flat
            data_vec = [v for v in data]
            if 4 != len(data_vec):
                ok = False
                print("4 != len(data_vec)")
            if [int(v) for v in data_vec] != [-2654, -2654, -2654, -2655]:
                ok = False
                print("[int(v) for v in data_vec] != [-2654, -2654, -2654, -2655]\n")
                print([int(v) for v in data_vec])
            chunk_1 = var.chunk((4,4), (4,4))
            chunk_1.set(42)
            chunk_2 = var.chunk((4,5), (4, 5))
            new_data_vec = [int(v) for v in chunk_2.as_array().flat]
            if [int(v) for v in new_data_vec] != [42, -2654, -2654, -2655]:
                ok = False
                print("[int(v) for v in new_data_vec] != [42, -2654, -2654, -2655]")
                print([int(v) for v in new_data_vec])
            chunk_1.set(data_vec[0])
            
            var_prp = var.horizon_property_3ds[1]
            if is_oop:
                var_prp.readonly = False
            if str(var_prp) != "HorizonProperty3D(petrel_name=\"Autotracker: Confidence\")":
                ok = False
                print("str(var_prp) != \"HorizonProperty3D(petrel_name=\"Autotracker: Confidence\")\"\n")
                print(str(var_prp))
            if int(var_prp.position(20, 30).x) != 486458:
                ok = False
                print("int(var_prp.position(20, 30).x) != 486458\n")
                print(int(var_prp.position(20, 30).x))
            if var_prp.indices(486288.6570124189, 6223608.341706959).i != 30:
                ok = False
                print("var_prp.indices(486288.6570124189, 6223608.341706959).i != 30\n")
                print(var_prp.indices(486288.6570124189, 6223608.341706959).i)
            
            chunk_prp_0 = var_prp.chunk((4,5), (4, 5))
            data_prp = chunk_prp_0.as_array().flat
            data_prp_vec = [v for v in data_prp]
            if 4 != len(data_prp_vec):
                ok = False
                print("4 != len(data_prp_vec)")
            if [int(v) for v in data_prp_vec] != [0, 0, 0, 0]:
                ok = False
                print("[int(v) for v in data_prp_vec] != [0, 0, 0, 0]\n")
                print([int(v) for v in data_prp_vec])
            chunk_prp_1 = var_prp.chunk((4,4), (4,4))
            chunk_prp_1.set(42)
            chunk_prp_2 = var_prp.chunk((4,5), (4, 5))
            new_data_vec = [int(v) for v in chunk_prp_2.as_array().flat]
            if [int(v) for v in new_data_vec] != [42, 0, 0, 0]:
                ok = False
                print("[int(v) for v in new_data_vec] != [42, 0, 0, 0]\n")
                print([int(v) for v in new_data_vec])
            chunk_prp_1.set(data_prp_vec[0])
            print(ok)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizoninterpretation3D_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizoninterpretation(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        hi = petrellink._get_horizon_interpretation('Input/Seismic/Interpretation folder 1/BCU')
        hi.readonly = False
        try:
            print(hi)
            print([v for v in hi.horizon_interpretation_3ds])
            print([v.horizon_interpretation for v in hi.horizon_interpretation_3ds])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizoninterpretation_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_HorizoninterpretationClone(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            hi = petrellink._get_horizon_interpretation('Input/Seismic/Interpretation folder 1/BCU')
            try:
                hi_clone = hi.clone('BCU_copy', copy_values = True)
            except Exception as e:
                hi_clone = petrellink._get_horizon_interpretation('Input/Seismic/Interpretation folder 1/BCU_copy')
            
            print(hi_clone)
            
            print([v for v in hi.horizon_interpretation_3ds])
            print([v.horizon_interpretation for v in hi.horizon_interpretation_3ds])
            print([v for v in hi_clone.horizon_interpretation_3ds])
            print([v.horizon_interpretation for v in hi_clone.horizon_interpretation_3ds])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizoninterpretation_clone_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogAsDataframe(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        vp = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vp')
        vp.readonly = False
        try:
            vp_values = vp.as_dataframe()
            print(vp_values.iloc[500:505,3:7])
            
            import copy
            old = copy.deepcopy(vp.samples)
            vp.set_values([], [])
            
            print(vp.as_dataframe().iloc[500:505,3:7])
            
            vp.samples = old
            vp_values = vp.as_dataframe()
            print(vp_values.iloc[500:505,3:7])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_as_dataframe_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesAt(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            print(var.samples.at(5812).value)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_at_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesSetValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            import copy
            old = copy.deepcopy(var.samples)
            try:
                var.set_values([1, 2, 3], [1.1, 2.2, 3.3])
                print(len(var.samples))
                print("{:.4f}".format(var.samples.at(2).value))
            finally:
                var.samples = old
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_set_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesSetValuesEmpty(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            import copy
            old = copy.deepcopy(var.samples)
            try:
                var.set_values([], [])
                print(len(var.samples))
            finally:
                var.samples = old
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_set_values_empty_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesSetWritable(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            old = var.samples.at(5812).value
            try:
                var.samples.at(5812).value = 123
                for s in var.samples[200:202]:
                    print(s.value)
            finally:
                var.samples.at(5812).value = old
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_set_writable_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesCount(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            print(len(var.samples))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_count_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesTransferInBulk(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        vs = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        vs.readonly = False
        vp = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vp')
        vp.readonly = False
        try:
            # record values as we're futzing with them
            a_vs = vs.samples.at(5812).value
            a_vp = vp.samples.at(5812).value
            import copy
            old = copy.deepcopy(vp.samples)
            try:
                vp.samples = vs.samples
                print(vp.samples.at(5812).value == a_vs)
            finally:
                vp.samples = old
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_transfer_in_bulk_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            print('[' + ', '.join([str(sample) for sample in var.samples[200:202]]) + ']')
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSamplesValues2017(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
        var.readonly = False
        try:
            print(var.samples[200:202])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_samples_values_2017_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogNavigation(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            from datetime import datetime
            
            start = datetime.now()
            
            for well in petrellink.wells:
                for log in well.logs:
                    print(log)
            
            print(datetime.now() - start)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_navigation_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogSetvalues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        vp = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vp')
        vp.readonly = False
        try:
            vp_values = vp.as_dataframe()
            
            print(vp_values.iloc[500:505,3:7])
            
            md = vp_values["MD"].values
            vp_log_values = vp_values["Value"].values
            vp_log_values_new = vp_log_values * 1.55
            
            vp.set_values(md,vp_log_values_new)
            print(vp.as_dataframe().iloc[500:505,3:7])
            
            vp.set_values(md,vp_log_values)
            print(vp.as_dataframe().iloc[500:505,3:7])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_setvalues_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellLogsDataframeColumnsOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        well = petrellink._get_well('Input/Wells/Well_Good')
        well.readonly = False
        try:
            global_logs = list(petrellink.global_well_logs)
            discrete_global_logs = list(petrellink.discrete_global_well_logs)
            
            all_logs = global_logs + discrete_global_logs
            logs = well.logs_dataframe(all_logs)
            i = 0
            
            for k, v in logs.iteritems():
                if k.endswith('_copy'):
                    logs = logs.drop(k, axis = 1)
            
            for k, v in logs.iteritems():
                if k.startswith('Copy of '):
                    logs = logs.drop(k, axis = 1)
            
            for c in logs.columns.sort_values():
                print(i, c)
                i += 1
            
            seismic3d = petrellink.seismic_cubes['Input/Seismic/Ardmore/Seismic3D']
            all_logs.append(seismic3d)
                
            try:
                logs = well.logs_dataframe(all_logs)
            except ValueError as err:
                print(err)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\well_logs_dataframe_columns_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellLogsDataframeSizeOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        well = petrellink._get_well('Input/Wells/Well_Good')
        well.readonly = False
        try:
            global_logs = list(petrellink.global_well_logs)
            discrete_global_logs = list(petrellink.discrete_global_well_logs)
            
            all_logs = global_logs + discrete_global_logs
            logs = well.logs_dataframe(all_logs)
            
            for k, v in logs.iteritems():
                if k.endswith('_copy'):
                    logs = logs.drop(k, axis = 1)
            
            for k, v in logs.iteritems():
                if k.startswith('Copy of '):
                    logs = logs.drop(k, axis = 1)
            
            print(logs.shape)
            
            for c in logs.columns.sort_values():
                i = len(logs[c])
                print(i, c)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\well_logs_dataframe_size_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellLogsDataframeValuesOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        well = petrellink._get_well('Input/Wells/Well_Good')
        well.readonly = False
        try:
            global_logs = list(petrellink.global_well_logs)
            discrete_global_logs = list(petrellink.discrete_global_well_logs)
            
            all_logs = global_logs + discrete_global_logs
            logs = well.logs_dataframe(all_logs)
            
            for k, v in logs.iteritems():
                if k.endswith('_copy'):
                    logs = logs.drop(k, axis = 1)
            
            for k, v in logs.iteritems():
                if k.startswith('Copy of '):
                    logs = logs.drop(k, axis = 1)
            
            sorted_logs = logs.sort_index(axis=1)
            
            import numpy as np
            for colName, colVals in sorted_logs.iteritems():
                value = colVals[18795]
                if isinstance(value, (int, np.int64, np.int32, str)):
                    print(colName, '=', value)
                else:
                    print(colName, '=', '{:.2f}'.format(value))
            
            print('')
                    
            logs = well.logs_dataframe(all_logs, discrete_data_as='value')
            
            for k, v in logs.iteritems():
                if k.endswith('_copy'):
                    logs = logs.drop(k, axis = 1)
            
            for k, v in logs.iteritems():
                if k.startswith('Copy of '):
                    logs = logs.drop(k, axis = 1)
            
            sorted_logs = logs.sort_index(axis=1)
            
            import numpy as np
            for colName, colVals in sorted_logs.iteritems():
                value = colVals[18795]
                if isinstance(value, (int, np.int64, np.int32, str)):
                    print(colName, '=', value)
                else:
                    print(colName, '=', '{:.2f}'.format(value))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\well_logs_dataframe_values_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelbridgeDiscretegridpropertiesOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            # Prints all the discerete ModelProperties in the project
            for (guid, prop) in sorted(list(petrellink.discrete_grid_properties.items()), key=lambda pair: pair[1].petrel_name):
                if not prop.petrel_name.endswith('_copy'):
                    print("* => {0}".format(prop.petrel_name))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelbridge_discretegridproperties_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelbridgeGridkeyvalueOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            myprop = petrellink.grids
            for (path, value) in sorted(list(myprop.items()), key = lambda p: str(p[1])):
                s = path
                if not value.path.endswith('_copy'):
                    print("[{0}=={1}]".format(s, value))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelbridge_gridkeyvalue_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelbridgeGridPathOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            # Paths to all grids
            grids = petrellink.grids
            
            for (guid, grid) in sorted(list(grids.items()), key = lambda p: p[1].path):
                print(grid.path)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelbridge_grid_path_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelbridgeGridpropertyKeyvalueOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            no_copies = { k: v for k, v in petrellink.grid_properties.items() if not k.endswith('_copy')}
            paths = sorted(no_copies)
            print("\n".join([f"{path}=={no_copies[path]}" for path in paths]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelbridge_gridproperty_keyvalue_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelbridgeGridpropertyPathOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            # Paths to all grid properties
            myprop = petrellink.grid_properties
            
            for (guid, value) in sorted(list(myprop.items()), key = lambda p: p[1].path):
                if not value.path.endswith('_copy'):
                    print(value.path)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelbridge_gridproperty_path_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelbridgeGridOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            # prints all the grids
            for (name, prop) in sorted(list(petrellink.grids.items()), key = lambda p: p[1].petrel_name):
                print("* => {0}".format(prop.petrel_name))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelbridge_grid_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionMakeConnection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            from cegalprizm.pythontool import  make_connection
            import numpy as np
            import pandas as pd
            
            with make_connection() as p:
                    pd.set_option("display.max_columns", 7)
                    print(p.a_project_is_active())
                    print(p.get_current_project_name())
                    
                    #checking writing from and to Petrel
                    GR = p.well_logs['Input/Wells/Well_Good/Well logs/GR']
                    GR_clone = GR.clone('Copy of GR', True)
                    
                    df = GR_clone.as_dataframe()
                    print(df.head())
                    
                    MD_to_reset = np.array(df["MD"])
            
                    df["MD"] = df["MD"] + 10
                    GR_clone.set_values(np.array(df["MD"]),np.array(df["Value"]))
                    df_clone_after_set_values = GR_clone.as_dataframe()
                    print(df_clone_after_set_values.head())
            
                    GR_clone.set_values(MD_to_reset,np.array(df["Value"]))
                    print(GR_clone.as_dataframe().head())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_make_connection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionAProjectIsActiveOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            print(petrellink.a_project_is_active())
            print(petrellink.get_current_project_name())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_a_project_is_active_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGetpetrelobjectsbyguidsPythontooltestproject(self):
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
                    if isinstance(item, list):
                        obj = item[0]
                    else:
                        obj = item
                    p_obj = petrellink.get_petrelobjects_by_guids([obj.droid])[0]
                    if (p_obj == None):
                        print("NoGuid:", obj)
                    else:
                        print(obj.droid == p_obj.droid and obj.path == p_obj.path, obj)
            
            #Invalid string returns None
            print(petrellink.get_petrelobjects_by_guids(["invalidstring"])[0], "invalidstring")
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_getpetrelobjectsbyguids_pythontooltestproject_expected.txt', 'r') as f:
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




    def test_PetrelconnectionOpenDeprecation(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            import warnings
            warnings.filterwarnings("error", category=DeprecationWarning)
            try:
                petrellink.open()
                print("failed")
            except Exception as e:
                print("ok")
            warnings.resetwarnings()
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_open_deprecation_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionGetprojectstorageunits(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            for k, v in sorted(list(petrellink.get_petrel_project_units().items())):
                print(k, v)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_getprojectstorageunits_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelobjectDroid(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            print(petrellink.discrete_global_well_logs['Input/Wells/Global well logs/Facies'].droid)
            print(petrellink.discrete_grid_properties['Models/Structural grids/Model_NoData/Properties/Facies'].droid)
            print(petrellink.discrete_grid_properties['Models/Structural grids/Model_NoData/Properties/Facies'].droid)
            print(petrellink.discrete_surface_attributes['Input/TWT Surface/BCU/Facies'].droid)
            print(petrellink.discrete_well_logs['Input/Wells/Well_Good/Well logs/Facies'].droid)
            print(petrellink.global_well_logs['Input/Wells/Global well logs/LambdaRho'].droid)
            print(petrellink.grid_properties['Models/Structural grids/Model_Good/Properties/AI'].droid)
            print(petrellink.grids['Models/Structural grids/Model_NoProperties'].droid)
            print(petrellink.horizon_interpretation_3ds['Input/Seismic/Interpretation folder 1/BCU/Ardmore'].droid)
            print(petrellink.horizon_properties['Input/Seismic/Interpretation folder 1/BCU/Ardmore/TWT'].droid)
            print(petrellink.pointsets['Input/Geometry/Points empty'].droid)
            print(petrellink.polylinesets['Input/Geometry/Polygon'].droid)
            print(petrellink.grid_properties['Models/Structural grids/Model_NoData/Properties/Rho'].droid)
            print(petrellink.property_collections['Models/Structural grids/Model_NoProperties/Properties'].droid)
            print(petrellink.seismic_2ds['Input/Seismic/Survey 1/Seismic2D'].droid)
            print(petrellink.seismic_cubes['Input/Seismic/Survey 2/Tiny3D'].droid)
            print(petrellink.seismic_lines['Input/Seismic/Survey 1/Seismic2D'].droid)
            print(petrellink.surface_attributes['Input/TWT Surface/BCU/TWT'].droid)
            print(petrellink.surface_discrete_attributes['Input/TWT Surface/BCU/Facies'].droid)
            print(petrellink.surfaces['Input/TWT Surface/BCU'].droid)
            print(petrellink.well_logs['Input/Wells/Well_Good/Well logs/Vp_K'].droid)
            print(petrellink.wells['Input/Wells/Well_Good'].droid)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelobject_droid_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelobjectTemplate(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            print('Input/Wells/Global well logs/Facies', ":", petrellink.discrete_global_well_logs['Input/Wells/Global well logs/Facies'].template)
            print('Models/Structural grids/Model_NoData/Properties/Facies', ":",petrellink.discrete_grid_properties['Models/Structural grids/Model_NoData/Properties/Facies'].template)
            print('Models/Structural grids/Model_NoData/Properties/Facies', ":", petrellink.discrete_grid_properties['Models/Structural grids/Model_NoData/Properties/Facies'].template)
            print('Input/TWT Surface/BCU/Facies', ":", petrellink.discrete_surface_attributes['Input/TWT Surface/BCU/Facies'].template)
            print('Input/Wells/Well_Good/Well logs/Facies', ":", petrellink.discrete_well_logs['Input/Wells/Well_Good/Well logs/Facies'].template)
            print('Input/Wells/Global well logs/LambdaRho', ":", petrellink.global_well_logs['Input/Wells/Global well logs/LambdaRho'].template)
            print('Models/Structural grids/Model_Good/Properties/AI', ":", petrellink.grid_properties['Models/Structural grids/Model_Good/Properties/AI'].template)
            print('Models/Structural grids/Model_NoProperties', ":", petrellink.grids['Models/Structural grids/Model_NoProperties'].template)
            print('Input/Seismic/Interpretation folder 1/BCU', ":", petrellink.horizon_interpretations['Input/Seismic/Interpretation folder 1/BCU'].template)
            print('Input/Seismic/Interpretation folder 1/BCU/Ardmore', ":", petrellink.horizon_interpretation_3ds['Input/Seismic/Interpretation folder 1/BCU/Ardmore'].template)
            print('Input/Seismic/Interpretation folder 1/BCU/Ardmore/TWT', ":", petrellink.horizon_properties['Input/Seismic/Interpretation folder 1/BCU/Ardmore/TWT'].template)
            print('Input/Geometry/Points empty', ":", petrellink.pointsets['Input/Geometry/Points empty'].template)
            print('Input/Geometry/Polygon', ":", petrellink.polylinesets['Input/Geometry/Polygon'].template)
            print('Models/Structural grids/Model_NoData/Properties/Rho', ":", petrellink.grid_properties['Models/Structural grids/Model_NoData/Properties/Rho'].template)
            print('Models/Structural grids/Model_NoProperties/Properties', ":", petrellink.property_collections['Models/Structural grids/Model_NoProperties/Properties'].template)
            print('Input/Seismic/Survey 1/Seismic2D', ":", petrellink.seismic_2ds['Input/Seismic/Survey 1/Seismic2D'].template)
            print('Input/Seismic/Survey 2/Tiny3D', ":", petrellink.seismic_cubes['Input/Seismic/Survey 2/Tiny3D'].template)
            print('Input/Seismic/Survey 1/Seismic2D', ":", petrellink.seismic_lines['Input/Seismic/Survey 1/Seismic2D'].template)
            print('Input/TWT Surface/BCU/TWT', ":", petrellink.surface_attributes['Input/TWT Surface/BCU/TWT'].template)
            print('Input/TWT Surface/BCU/Facies', ":", petrellink.surface_discrete_attributes['Input/TWT Surface/BCU/Facies'].template)
            print('Input/TWT Surface/BCU', ":", petrellink.surfaces['Input/TWT Surface/BCU'].template)
            print('Input/Wells/Well_Good/Well logs/Vp_K', ":", petrellink.well_logs['Input/Wells/Well_Good/Well logs/Vp_K'].template)
            print('Input/Wells/Well_Good', ":", petrellink.wells['Input/Wells/Well_Good'].template)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelobject_template_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAddPointNoAttributes(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points no attributes')
        var.readonly = False
        try:
            from cegalprizm.pythontool.primitives import Point
            
            var.add_point(Point(50.0,50.0,915.0))
            print("{} {} {}".format(var[3].x, var[3].y, var[3].z))
            var.delete_point(Point(50.0,50.0,915.0))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_add_point_no_attributes_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAddPointWithAttributes(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            from cegalprizm.pythontool.primitives import Point
            
            var.add_point(Point(50.0,50.0,915.0))
            print("{} {} {}".format(var[10].x, var[10].y, var[10].z))
            var.delete_point(Point(50.0,50.0,915.0))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_add_point_with_attributes_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetComplete(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points empty')
        var.readonly = False
        try:
            from cegalprizm.pythontool.primitives import Point
            
            print(var.petrel_name)
            old_points = list(var.points)
            var.add_point(Point(1.0, 2.0, 914.40))
            print(len(var.points))
            print(var.points[0].x)
            var.add_point(Point(6, 7, 8))
            print(len(var.points))
            print(var.points[1].x)
            var.points = [Point(1,2,3), Point(4,5,6), Point(7,8,9)]
            print(len(var.points))
            print(var.points[2].x)
            var.delete_point(Point(4,5,6))
            print(len(var.points))
            print(var.points[1].x)
            
            var.points = old_points
            
            #print("restoring")
            #print(len(var.points))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_complete_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetCompleteReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1')
        var.readonly = True
        try:
            try:
                var.add_point(Point(6, 7, 8))
            except:
                print("caught")
            
            try:
                var.points = [Point(1,2,3), Point(4,5,6), Point(7,8,9)]
            except:
                print("caught")
            
            try:
                var.delete_point(var.points[0])
            except:
                print("caught")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_complete_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAsDataframe(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            print(var.petrel_name)
            print()
            print('Columns')
            df = var.as_dataframe()
            
            data_types = df.dtypes
            for i, name in enumerate(df.columns):
                if name.endswith('_new'):
                    continue
                print(name, ':', data_types[i])
            
            print()
            print('Row 3')
            for i, name in enumerate(df.columns):
                if name.endswith('_new'):
                    continue
                print(df[name][3])
            
            print()
            print('Column TestString (2):')
            for v in df['TestString (2)'].values:
                print(v)
            
            print()
            print('Size:', df.size)
            
            print()
            df = var.as_dataframe()
            print(df.index.values)
            # Expects [0 1 2 3 4 5 6 7 8 9]
            
            df = var.as_dataframe(indices = [2, 5, 6, 9])
            print(df.index.values)
            # Expects [2 5 6 9]
            
            df = var.as_dataframe(start = 2, end = 7, step = 2)
            print(df.index.values)
            # Expects [2 4 6]
            
            df = var.as_dataframe(start = 7, step = 2)
            
            print(df.index.values)
            # Expects [7 9]
            
            df = var.as_dataframe(end = 5, step = 3)
            print(df.index.values)
            # Expects [0 3]
            
            df = var.as_dataframe(end = 5)
            print(df.index.values)
            # Expects [0 1 2 3 4 5]
            
            df = var.as_dataframe(start = 5)
            print(df.index.values)
            # Expects [5 6 7 8 9]
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_as_dataframe_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetCache(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Seismic_pointset')
        var.readonly = False
        try:
            # var = petrellink.pointsets['Input/Geometry/Seismic_pointset']
            import time
            from cegalprizm.pythontool.primitives import Point
            for i in [0, 103, 104, 105, 1000, 1000+103, 1000+104, 1000+105, 2000, 2000+103, 2000+104, 2000+105]:
                start = time.time()
                point = var.points[i]
                x = point.x
                y = point.y
                z = point.z
                end = time.time()
                #print("Index: {:>4}, time: {:.2f}, x: {:.1f}, y: {:.1f}, z: {:.1f}".format(i, end-start, x, y, z))
                print("Index: {:>4}, x: {:.1f}, y: {:.1f}, z: {:.1f}".format(i, x, y, z))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_cache_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAsDataframeSpatialRange(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            print(var.petrel_name)
            df0 = var.as_dataframe()
            print('Index:', df0.index.values)
            print('index\tx\ty\tz')
            [print('%d\t%.2f\t%.2f\t%.2f' % (i, df0.x[i], df0.y[i], df0.z[i]))
                for i in range(len(df0.index))]
            
            print()
            
            # Compares filtering on server and client
            xrange = (28.9999, 6000)
            print('xrange:', xrange)
            df_x_server_filtered = var.as_dataframe(x_range = xrange)
            print('Server x-filtered:', df_x_server_filtered.index.values)
            
            b = [x >= xrange[0] and x < xrange[1] for x in df0.x]
            df_x_client_filtered = df0[b]
            print('Client x-filtered:', df_x_client_filtered.index.values)
            ok = list(df_x_server_filtered.index.values) == list(df_x_client_filtered.index.values)
            print('X filtering passed:', ok)
            
            print()
            
            yrange = (3.0, 2000.0)
            print('yrange:', yrange)
            df_y_server_filtered = var.as_dataframe(y_range = yrange)
            print('Server y-filtered:', df_y_server_filtered.index.values)
            
            b = [y >= yrange[0] and y < yrange[1] for y in df0.y]
            df_y_client_filtered = df0[b]
            print('Client y-filtered:', df_y_client_filtered.index.values)
            ok = list(df_y_server_filtered.index.values) == list(df_y_client_filtered.index.values)
            print('Y filtering passed:', ok)
            
            print()
            
            zrange = (-2000.0, -200)
            print('zrange:', zrange)
            df_z_server_filtered = var.as_dataframe(z_range = zrange)
            print('Server z-filtered:', df_z_server_filtered.index.values)
            b = [z >= zrange[0] and z < zrange[1] for z in df0.z]
            df_z_client_filtered = df0[b]
            print('Client z-filtered:', df_z_client_filtered.index.values)
            ok = list(df_z_server_filtered.index.values) == list(df_z_client_filtered.index.values)
            print('Z filtering passed:', ok)
            
            xyz_intersection = set(df_x_client_filtered.index.values)\
                .intersection(set(df_y_client_filtered.index.values))\
                .intersection(set(df_z_client_filtered.index.values))
            xyz_intersection = list(xyz_intersection)
            xyz_intersection.sort()
            
            df_xyz_filtered = var.as_dataframe(x_range = xrange, y_range = yrange, z_range = zrange)
            ok = xyz_intersection == list(df_xyz_filtered.index.values)
            
            print()
            print('With all filters:', df_xyz_filtered.index.values)
            print('Intersection of separate results:', xyz_intersection)
            print('XYZ-filtering ok:', ok)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_as_dataframe_spatial_range_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAsDataframeMaxPoints(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            print(var.petrel_name)
            df0 = var.as_dataframe(x_range = [10, 20000])
            print(df0.index.values)
            
            df1 = var.as_dataframe(x_range = [10, 20000], max_points=3)
            print(df1.index.values)
            
            df2 = var.as_dataframe(start = 4, max_points = 3)
            print(df2.index.values)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_as_dataframe_max_points_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAsDataframeNoproperties(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points empty')
        var.readonly = False
        var_1 = petrellink._get_pointset('Input/Geometry/Points no attributes')
        var_1.readonly = False
        try:
            print(var.as_dataframe())
            print('')
            print(var_1.as_dataframe())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_as_dataframe_noproperties_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetSetValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Seismic_pointset')
        var.readonly = False
        try:
            print(var.petrel_name)
            df = var.as_dataframe()
            print()
            print('Number of rows:', len(df['x']))
            
            original_values = list(df['TWT auto'])
            
            df['TWT auto'] = df['TWT auto'] * 2
            var.set_values(df)
            
            df2 = var.as_dataframe()
            
            doubled = df2['TWT auto']
            ok = True
            for i in range(0, len(original_values)):
                ok = True and (abs(original_values[i] * 2 - doubled[i])) < 0.0001
            
            print()
            print('Even indexed values doubled:', ok)
            
            # Reset to original values
            df['TWT auto'] = original_values
            var.set_values(df)
            
            df3 = var.as_dataframe(indices = [0])
            print('Reset ok: ', abs(df3['TWT auto'][0] - original_values[0]) < 0.0001)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_set_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetAttributesInfo(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Seismic_pointset')
        var.readonly = False
        try:
            print(var.petrel_name)
            
            info = var._attributes_info()
            keys = list(info.keys())
            keys.sort()
            
            for key in keys:
                print('Unit:', key, '-', info[key]['Unit'])
                print('Template:', key, '-', info[key]['Template'])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_attributes_info_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetSetValuesCreate(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            print(var.petrel_name)
            
            df = var.as_dataframe()
            original_df = var.as_dataframe()
            info = var._attributes_info()
            
            new_names = []
            for name in df.columns:
                if name in ['x', 'y', 'z'] or name.endswith('_new'):
                    continue
            
                data_type = info[name]['Data type']
                if data_type in ['String', 'DateTime']:
                    continue
            
                name_new = name + '_new'
                
                if data_type == "Boolean":
                    df[name_new] = df[name]
                else:
                    df[name_new] = 10 * df[name]
                
                new_names.append(name_new)
            
            print()
            
            var.set_values(df, create = new_names)
            
            df2 = var.as_dataframe()
            info2 = var._attributes_info()
            
            for name_new in df2.columns:
                if not name_new.endswith('_new'):
                    continue
                name = name_new.split('_')[0]
                print(name, '-', name_new)
            
                print('\t', info2[name]['Type'], '-', info2[name_new]['Type'])
                print('\t', info2[name]['Template'], '-', info2[name_new]['Template'])
                print('\t', info2[name]['Data type'], '-', info2[name_new]['Data type'])
                print('\t', info2[name]['Unit'], '-', info2[name_new]['Unit'])
                
                try:
                    s = '%.2f %.2f' % (df2[name][3], df2[name_new][3])
                    print('\t', s)
                except:
                    print('\t', df2[name][3], df2[name_new][3])
            
            
            # after reset - pointset will contain the original attributes AND the "_new" attributes
            var.set_values(original_df)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_set_values_create_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Seismic_pointset')
        var.readonly = False
        try:
            print(var.petrel_name)
            
            with var.values(indices = [100, 200, 300]) as df:
                original_value = df.loc[100, 'TWT auto']
                print('Original value: ', original_value)
                df.loc[100, 'TWT auto'] = 2 * original_value
                print('Changed value: ', df.loc[100, 'TWT auto'])
            
            with var.values(indices = [100, 200, 300]) as df:
                print(df.index.values)
                print('Changed value: ', df.loc[100, 'TWT auto'])
                df.loc[100, 'TWT auto'] = original_value
            
            with var.values(start = 100, end = 300, step = 100) as df:
                print(df.index.values)
                print('Changed value: ', df.loc[100, 'TWT auto'])
                df.loc[100, 'TWT auto'] = original_value
            
            df = var.as_dataframe(start = 100, step = 10, end = 150)
            print(df)
            
            with var.values(start = 100, step = 10, x_range = [400_000, 500_000], y_range = [0, 10_000_000], z_range = [-3199, 0], max_points = 4) as df:
                print(df.index.values)
            
            with var.values(start = 100, x_range = [0, 100]) as df:
                # Expects empty dataframe
                print(df.index.values)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetpropertyComplete(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1')
        var.readonly = False
        try:
            from datetime import datetime
            
            def is_almost(val, target):
                return True if abs(val - target) < 0.001 else False
            
            old_df = var.as_dataframe()
            
            ok = True
            if len(var.points) != 1:
                ok = False
                print("len(var.points) != 1\n")
            if len(list(var.as_dataframe())) != 15:
                ok = False
                print("len(list(var.as_dataframe())) != 15, actually {}\n".format(len(list(var.as_dataframe()))))
            
            if not is_almost(var.as_dataframe()["x"][0], 1.0):
                ok = False
                print("not is_almost(p0.x, 1.0)\n")
                print(var.as_dataframe()["x"][0])
            if not is_almost(var.as_dataframe()["y"][0], 2.0):
                ok = False
                print("not is_almost(p0.y, 2.0)\n")
                print(var.as_dataframe()["y"][0])
            if not is_almost(var.as_dataframe()["z"][0], 914.40):
                ok = False
                print("not is_almost(p0.z, 914.40)\n")
                print(var.as_dataframe()["z"][0])
            if not is_almost(var.as_dataframe()["TWT auto"][0], -914.40):
                ok = False
                print("not is_almost(p0.value, -914.40)\n")
                print(var.as_dataframe()["TWT auto"][0])
            
            with var.values() as df:
                df["TWT auto"][0] = 42.0
            if not is_almost(var.as_dataframe()["TWT auto"][0], 42.0):
                ok = False
                print("not is_almost(p0.value, 42.0)\n")
                print(var.as_dataframe()["TWT auto"][0])
            with var.values() as df:
                df["TWT auto"][0] = old_df["TWT auto"][0]
            
            
            with var.values() as df:
                df["TWT auto"][0] = 13.37
            if not is_almost(var.as_dataframe()["TWT auto"][0], 13.37):
                ok = False
                print("not is_almost(p0.value, 13.37)\n")
                print(var.as_dataframe()["TWT auto"][0])
            with var.values() as df:
                df["TWT auto"][0] = old_df["TWT auto"][0]
            
            
            with var.values() as df:
                if not is_almost(df["Dip angle"][0], 45.00):
                    ok = False
                    print(df["Dip angle"][0])
                df["Dip angle"][0] = 42.00
            with var.values() as df:
                if not is_almost(df["Dip angle"][0], 42.00):
                    ok = False
                    print(df["Dip angle"][0])
                df["Dip angle"][0] = old_df["Dip angle"][0]
            
            
            with var.values() as df:
                if not is_almost(df["Continuous"][0], 4.20):
                    ok = False
                    print(df["Continuous"][0])
                df["Continuous"][0] = 42.00
            with var.values() as df:
                if not is_almost(df["Continuous"][0], 42.00):
                    ok = False
                    print(df["Continuous"][0])
                df["Continuous"][0] = old_df["Continuous"][0]
            
            with var.values() as df:
                if not str(df["Date"][0]) == "2020-01-28 00:00:00":
                    ok = False
                    print("var.attributes['Date']")
                df["Date"][0] = datetime.now()
            with var.values() as df:
                if str(df["Date"][0]) == "2020-01-28 00:00:00":
                    ok = False
                    print("var.attributes['Date']")
                df["Date"][0] = old_df["Date"][0]
            
            with var.values() as df:
                if not df["TestBoolean"][0] == False:
                    ok = False
                    print("df[TestBoolean][0] should be False but is {}".format(df["TestBoolean"][0]))
                df["TestBoolean"][0] = True
            with var.values() as df:
                if not df["TestBoolean"][0] == True:
                    ok = False
                    print("df[TestBoolean][0] should be True but is {}".format(df["TestBoolean"][0]))
                df["TestBoolean"][0] = old_df["TestBoolean"][0]
            
            
            with var.values() as df:
                if not df["TestString"][0] == "Hello Pointset":
                    ok = False
                    print(
                        "var.attributes['TestString'], should be hello pointset is: {}\n".format(
                            df["TestString"][0]
                        )
                    )
                df["TestString"][0] = "a"
            
            with var.values() as df:
                if not df["TestString"][0] == "a":
                    ok = False
                    print("var.attributes['TestString'], should be a is: {}\n".format(df["TestString"][0]))
                df["TestString"][0] = old_df["TestString"][0]
                    
            
            with var.values() as df:
                if not df["Discrete (1)"][0] == 42:
                    ok = False
                    print("var.attributes['Discrete (1)']")
                df["Discrete (1)"][0] = 2
            with var.values() as df:
                if not df["Discrete (1)"][0] == 2:
                    ok = False
                    print("var.attributes['Discrete (1)']")
                df["Discrete (1)"][0] = 42
            
            print(ok)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointsetproperty_complete_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            #pointset = petrellink.pointsets['Input/Geometry/Points 1 many points']
            
            stats = var.retrieve_stats()
            
            print('\n', stats['Max'])
            print('\n', stats['Mean'])
            print('\n', stats['Min'])
            print('\n', stats['Number of attributes'])
            print('\n', stats['Number of defined values'])
            print('\n', stats['Number of points'])
            print('\n', stats['Std. dev.'])
            print('\n', stats['Sum'])
            print('\n', stats['Type of data'])
            print('\n', stats['Variance'])
                
            print('\n', type(var.retrieve_stats()))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetRetrieveHistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            res = ""
            for lst in var.retrieve_history().iloc[:1,1:].values:
                for el in lst:
                    res += el
            print(res.replace(" ", ""))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_retrieve_history_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetPath(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            pointset = petrellink.pointsets['Input/Geometry/Points 1 many points']
            print(pointset.path)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_path_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetPetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            #pointset = petrellink.pointsets['Input/Geometry/Points 1 many points']
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_pointset('Input/Geometry/Points 1 many points')
        var.readonly = False
        try:
            from cegalprizm.pythontool.primitives import Point
            
            pointset = petrellink.pointsets['Input/Geometry/Points 1 many points']
            print(pointset.readonly)
            pointset.readonly = False
            print(pointset.readonly)
            pointset.add_point(Point(50,50,50))
            pointset.delete_point(Point(50,50,50))
            pointset.readonly = True
            print(pointset.readonly)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetComplete(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_polylineset('Input/Geometry/Polygon')
        var.readonly = False
        try:
            try:
                is_oop
            except NameError:
                is_oop = False
            
            if is_oop:
                from cegalprizm.pythontool import Point
            
            old_positions = var[0].positions()
            print(var.petrel_name) # Polygon
            print(len(var)) # 1
            print(var[0]) # Polyline(parent_polylineset=PolylineSet(petrel_name="Polygon"))
            print(var[0].polylineset) #PolylineSet(petrel_name="Polygon")
            var.add_line([Point(0,0,0), Point(1,1,1), Point(2,2,2)])
            print(var[1].points[2].x) # 2.0
            var.delete_line(var[0])
            print(var[0].points[1].x) # 1.0
            print(len(var[0].points)) # 3
            print(var[0].readonly) # False
            print(var[0].closed) # True
            print(var.is_closed(0)) # True
            var[0].add_point(Point(3,3,3))
            print(len(var[0].points)) # 4
            var[0].delete_point(Point(1,1,1))
            print([p.x for p in var[0].points]) # [0.0, 2.0, 3.0]
            print(var[0].positions()) # [[0.0, 2.0, 3.0], [0.0, 2.0, 3.0], [0.0, 2.0, 3.0]]
            print(var.get_positions(0)) # [[0.0, 2.0, 3.0], [0.0, 2.0, 3.0], [0.0, 2.0, 3.0]]
            print(var.retrieve_stats()['Number of polygons']) # 1
            for line in var.polylines:
                print(line)
            var.set_positions(0,[10.0, 2.0, 3.0], [10.0, 2.0, 3.0], [10.0, 2.0, 3.0])
            print(var.get_positions(0))
            var.set_positions(0, *old_positions)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_complete_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetGetpoints(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_polylineset('Input/Geometry/Polygon')
        var.readonly = False
        try:
            print(str(type(var.get_positions(0)))[-7:-2])
            print(["{:.2f}".format(v) for item in var.get_positions(0) for v in item])
            pol = var[0]
            print(pol)
            print(str(type(pol.positions()))[-7:-2])
            print(["{:.2f}".format(v) for item in pol.positions() for v in item])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_getpoints_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetCompleteReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_polylineset('Input/Geometry/Polygon')
        var.readonly = True
        try:
            try:
                var.add_line([Point(0,0,0), Point(1,1,1), Point(2,2,2)])
            except:
                print("caught")
            try:
                var.delete_line(var[0])
            except:
                print("caught")
            
            print(var[0].readonly) # True
            
            try:
                var[0].add_point(Point(3,3,3))
            except:
                print("caught")
            
            try:
                var[0].delete_point(var[0].points[0])
            except:
                print("caught")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_complete_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Propertycollection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            grid_properties = [gp for gp in var.parent_collection if not gp.petrel_name.endswith('_copy')] 
            print(len(grid_properties))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\propertycollection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dChunkSetOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            newline = var.clone('Copy of 2D line', True)
            df_original_values = newline.column(10).as_dataframe()
            print(df_original_values.head())
            newline.column(10).set(7.77)
            print(newline.column(10).as_dataframe().head())
            newline.column(10).set(df_original_values)
            print(newline.column(10).as_dataframe().head())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_chunk_set_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dColumn(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #ValueError is thrown if j-index is invalid
            for (i,j,k, val) in var.column(0).enumerate():
                print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                if k == 0:
                    break;
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_column_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dColumns(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #can access the column slices
            for cols in var.columns(jrange=(0,1)):
                for (i,j,k, val) in cols.enumerate():
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                    if k==1:
                        break;
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_columns_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dColumnsvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #ValueError is thrown when the i-index is invalid
            for cols in var.columns(jrange=(-1,1)):
                for (i,j,k, val) in cols.enumerate():
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                    if k==1:
                        break;
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_columnsvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dCoordsextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #prints the seismic's World coordinates
            print(var.coords_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_coordsextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dExtent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #prints the extents in j,k direction. i will always be 'None'
            print(var.extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_extent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dHassameparent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        var_1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var_1.readonly = False
        try:
            print(var.has_same_parent(var))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_hassameparent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dHassameparentValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        var_1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var_1.readonly = False
        try:
            #ValueError is thrown if the other objects is not Seismic 2D line
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_hassameparent_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dIndices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #prints the indices at the given (x,y,z)
            print(var.indices(484799, 6224142, -2400))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_indices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dIndicesvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #ValueError is thrown when (x,y,z) is outside the seismic
            print(var.indices(1,1,1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_indicesvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dPetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #prints Petrel name 
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dPosition(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #prints the (x, y, z) coordinates at a given (j, k) position
            print(var.position(0,0))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_position_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dPositionvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            #ValueError is thrown if position is outside the seismic
            print(var.position(999,0))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_positionvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = True
        try:
            #Cannot write if the Seismic 'Read only' is checked
            with var.column(0).values() as vals:
                vals[0] = 1.23
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var.readonly = False
        try:
            print(var.retrieve_stats().get('Number of cells total'))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dAll(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            chunk_all = var.all()
            print(var.extent)
            print(chunk_all.object_extent)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_all_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dAnnotation(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints the annotation for seismic indices, default to k=0
            print(var.annotation(0,0,0))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_annotation_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dAnnotationIndices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints the indices of a inline/crossline/sample. Sample defaults to 1
            print(var.annotation_indices(855,2297, 1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_annotation_indices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dAnnotationIndicesValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #throws ValueError when indices of inline/xline/sample are outside the seismic
            print(var.annotation_indices(1,1,1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_annotation_indices_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dAnnotationvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #ValueError exception is thrown when indices is outside the seismic
            print(var.annotation(0,0,-200))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_annotationvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dChunk(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Survey 2/Tiny3D')
        var.readonly = False
        try:
            extent = var.extent
            
            def reset():
                allchunk = var.chunk((), (), ())
                with allchunk.values() as vals:
                    for i in range(0, allchunk.slice_extent.i):
                        for j in range(0, allchunk.slice_extent.j):
                            for k in range(0, allchunk.slice_extent.k):
                                vals[i, j, k] = i + 10 * j + 100 * k
            
            def is_in(idx, idx_tuple):
                if idx_tuple is not None:
                    return idx >= idx_tuple[0] and idx <= idx_tuple[1]
                else:
                    return True
            
            def check_chunk(irange, jrange, krange):
                print("check chunk", irange, jrange, krange)
                reset()
                c = var.chunk(irange, jrange, krange)
                if c.as_array() is None:
                    raise Exception("Chunks values are empty")
                c.set(999.0)
            
                with var.chunk((), (), ()).values() as vals:
                    for i in range(0, extent.i):
                        for j in range(0, extent.j):
                            for k in range(0, extent.k):
                                val = vals[i, j, k]
                                if is_in(i, irange) and is_in(j, jrange) and is_in(k, krange):
                                    if val != 999.0:
                                        raise Exception("failed in chunk")
            
                                elif val != i + j * 10 + k * 100:
                                    raise Exception("failed outside chunk")
            
            possible_is = [None] + list(range(0, extent.i))
            possible_js = [None] + list(range(0, extent.j))
            possible_ks = [None] + list(range(0, extent.k))
            
            import itertools as it
            
            i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
            j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
            k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
            for irange in i_s:
                for jrange in j_s:
                    for krange in k_s:
                        check_chunk(irange, jrange, krange)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_chunk_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dSetValue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Survey 2/Tiny3D')
        var.readonly = False
        try:
            extent = var.extent
            chunk_all = var.all()
            original_array = chunk_all.as_array()
            var.set_value(1337.0)
            new_array = var.all().as_array()
            print(abs((new_array - 1337.0).sum()) < 0.05)
            chunk_all.set(original_array)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_set_value_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dChunkError(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            try:
                var.chunk((70,400),(40,45),(150,155)).as_dataframe()
            except Exception as err:
                print(err)
                print('---')
                
            try:
                var.chunk((350,360),(40,45),(150,900)).as_dataframe()
            except Exception as err:
                print(err)
                print('---')
                
            try:
                var.chunk((70,60),(40,45),(150,155)).as_dataframe()
            except Exception as err:
                print(err)
                print('---')
                
            try:
                var.chunk((70,902),(40,45),(150,155)).as_dataframe()
            except Exception as err:
                print(err)
                print('---')
            try:
                var.chunk((-70,-60),(40,45),(150,155)).as_dataframe()
            except Exception as err:
                print(err)
                print('---')
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_chunk_error_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dColumns(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #sets the value to 0 for islice = 0 & 1, can see the change in 3D window. Move the seismic Inline/Xline to islice = 0
            
            original_values = [None]*2
            for i in range(2):
                original_values[i] = [None]*2
                for j in range(2):
                    original_values[i][j] = var.column(i, j).as_array()
            
            for col in var.columns(irange=list(range(0, 2)), jrange=list(range(0,2))):
                col.set(0)
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
            
            for (i,j,k, val) in var.column(1,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
                
            for (i,j,k, val) in var.column(2,0).enumerate():
                if k == 0:
                    print("[{0}, {1}, {2}] == {3:.2f}]".format(i,j,k,val))
            
            
            # Reset to original values
            for i in range(2):
                for j in range(2):
                    var.column(i, j).set(original_values[i][j])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_columns_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dColumnvalueerrorI(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #ValueError is thrown if i-index is invalid
            with var.column(-1,0).values() as vals:
                vals[0] = 1.23
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_columnvalueerror_i_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dColumnvalueerrorJ(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #ValueError is thrown when j-index is invalid
            with var.column(0,-1).values() as vals:
                vals[0] = 1.23
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_columnvalueerror_j_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dCoordsextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints the world co-ordinates
            print(var.coords_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_coordsextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dExtent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints petrel name
            print(var.extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_extent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dHassameparent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            ardmore_clone = var.clone("Ardmore clone", True)
            print(var.has_same_parent(ardmore_clone))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_hassameparent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dHassameparentValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        var_1 = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
        var_1.readonly = False
        try:
            #ValueError is thrown if two different objects are compared for same parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_hassameparent_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dIndices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints the indices at the given (x,y,z)
            print(var.indices(486496, 6223208, -2400))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_indices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dIndicesvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #ValueError is thrown when (x,y,z) is outside the seismic
            print(var.indices(0,0,0))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_indicesvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dLayers(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            vals = var.layer(0).as_array()
            print("{0:.2f}".format(vals[2,3]))
            
            var.layer(0).set(var.layer(0) * 10)
            vals = var.layer(0).as_array()
            print("{0:.2f}".format(vals[2,3]))
            
            var.layer(0).set(var.layer(0) / 10)
            vals = var.layer(0).as_array()
            print("{0:.2f}".format(vals[2,3]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_layers_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dObjectextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints the extent of the slice
            print(var.column(0,0).object_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_objectextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dPath(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            seismic = petrellink.seismic_cubes['Input/Seismic/Ardmore/Seismic3D']
            print(seismic.path)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_path_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dPetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #prints petrel name
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dPosition(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #print the world coordinate positon at the given i,j,k
            print(var.position(0,0,0))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_position_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dPositionvalueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #ValueError is thrown when Position is outside the seismic
            print(var.position(555,555,555))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_positionvalueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = True
        try:
            #Cannot overwrite the values when 'Read only' is checked on
            with var.column(0,0).values() as vals :
                vals[0] = 111
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dSliceclone(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            #trutned object as same values as the original slice
            
            for (i, j, k, val) in var.column(10,10).enumerate():
                if  k ==0 or k== 1:
                    print("[%d %d %d] => %f" % (i, j, k, val))
                    break;
                    
            for (i, j, k, val) in var.column(22,15).enumerate():
                if  k ==0 or k== 1:
                    print("[%d %d %d] => %f" % (i, j, k, val))
                    break;
            
            average_layer = var.column(10,10).clone()
            oldcolumnvalues = var.column(22,15).as_array()
            var.column(22,15).set(average_layer)
            
            for (i, j, k, val) in var.column(22,15).enumerate():
                if  k ==0 or k== 1:
                    print("[%d %d %d] => %f" % (i, j, k, val))
                    break;
            
            var.column(22, 15).set(oldcolumnvalues)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_sliceclone_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dUpdaterawvalue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            original_value = var.column(0,0).as_array()[0]
                
            with var.column(0,0).values() as vals:
                vals[0] = 1.23  
                
            for (i,j,k, val) in var.column(0,0).enumerate():
                print("[{0}, {1}, {2}] == {3:.2f}".format(i,j,k,val))
                if k == 0:
                    break
            
            # Reset to original value
            with var.column(0,0).values() as vals:
                vals[0] = original_value
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_updaterawvalue_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            def mylen(d):
                # Can't use built-in len as CPython doesn't know how to the __len__ of a C# Dictionary, although it can iterate over it (using Python.NET)...
                l = 0
                for k in d:
                    l = l + 1
                return l
            
            print(mylen(var.retrieve_stats()) > 0)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceHassameparent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        var_1 = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var_1.readonly = False
        try:
            #Prints True is both properties have same Parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_hassameparent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceHassameparentValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        var_1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var_1.readonly = False
        try:
            #ValueError is thrown when Surface property is compared with a Seismic cube
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_hassameparent_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceIsundefFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #Returns False if it's a valid value, i.e, not NAN
            #[1,1]==-2710.73999023 is a valid number
            print(var.is_undef_value(var.all().as_array()[1,1]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_isundef_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceIsundefTrue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #Returns True if the value is NAN
            #First manually set the value to NAN using 'undef-value' and then do the is_undef
            
            layer = var.all().as_array()
            original_value = layer[0,0]
            
            layer[0,0] = var.undef_value
            var.all().set(layer)
            print(var.is_undef_value(var.all().as_array()[0,0]))
            
            # Reset
            layer[0,0] = original_value
            var.all().set(layer)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_isundef_true_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceObjectextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #prints the extent of the slice
            print(var.all().object_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_objectextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurface(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #Returns the parent Surface of the attribute
            print(var.surface.petrel_name) 
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurface_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceCoordsextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #Prints the World coordinates
            print(var.surface.coords_extent)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurface_coordsextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            def mylen(d):
                # Can't use built-in len as CPython doesn't know how to the __len__ of a C# Dictionary, although it can iterate over it (using Python.NET)...
                l = 0
                for k in d:
                    l = l + 1
                return l
            
            print(mylen(var.retrieve_stats()) > 0)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurface_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #prints the maximum i & j indices
            print(var.surface.extent)
            print(var.surface.extent.i)
            print(var.surface.extent.j)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurfaceextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceindices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #prints the indices of the cell at the given (x,y) location
            print(var.surface.indices(484798, 6224426))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurfaceindices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceindicesValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #ValueError is thrown when (x,y) is outside the Surface
            print(var.surface.indices(400, 600))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurfaceindices_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceposition(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #Prints the (x,y,z) position of the cell at the given (i,j). z will always be none
            print(var.surface.position(130, 153))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurfaceposition_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfacepositionValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #ValueError is thrown when (i,j) is outside the Surface geometry
            print(var.surface.position(131,154))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurfaceposition_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfacePetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #prints Petrel name of the Surface attribute
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = True
        try:
            #Cannot write to the Surface when 'Read only' is checked
            layer = var.all().as_array()
            layer[0,0] = 0
            var.all().set(layer)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            def mylen(d):
                # Can't use built-in len as CPython doesn't know how to the __len__ of a C# Dictionary, although it can iterate over it (using Python.NET)...
                l = 0
                for k in d:
                    l = l + 1
                return l
            
            print(mylen(var.retrieve_stats()) > 0)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceSetundefvalue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #First set the value to 'undef-value', then change it back to a 'def' value
            layer = var.all().as_array()
            original_value = layer[0,0]
            layer[0,0] = var.undef_value #float('nan')
            var.all().set(layer)
            print(var.all().as_array()[0,0])
            print(var.is_undef_value(var.all().as_array()[0,0]))
            
            layer = var.all().as_array()
            layer[0,0] = -2711.13061523
            var.all().set(layer)
            print("{:.2f}".format(var.all().as_array()[0,0]))
            print(var.is_undef_value(var.all().as_array()[0,0]))
            
            # Reset to original value
            layer[0, 0] = original_value
            var.all().set(layer)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_setundefvalue_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceUnitsymbol(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #print the Petrel units
            print(var.unit_symbol)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_unitsymbol_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceUpdaterawvalues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            #Uncheck 'Read only' and update the rawvalues using all().set(value)
            #The value is set for the whole surface which has one z slice
            
            # 6/6/18 - this float cast is a massive smell.  The slice.set method 
            # should cope now with numpy floats but doesn't seem to? 
            original_values = var.all().as_array()
            
            a = float(var.all().as_array()[0,0])
            var.all().set(a+100.0)
            
            for (i,j,k,val) in var.all().enumerate():
                print("[{0},{1},{2}]=={3:.2f}]".format(i,j,k,val))
                if j == 1:
                    break
            
            # Reset values
            var.all().set(original_values)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_updaterawvalues_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceParentsurfaceSurfaceattributes(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            print(len(var.surface.surface_attributes))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surface_parentsurface_surfaceattributes_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributePosition(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            import numpy as np
            
            print(var.petrel_name)
            pos = var.ijks_to_positions([[1,2,3],[1,2,3]])
            for v in np.array(pos).transpose().ravel():
                print("{:.1f}".format(v))
            ijks = var.positions_to_ijks(pos)
            ijks
            for v in np.array(ijks).transpose().ravel():
                print("{:.1f}".format(v))
            print()
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_position_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributePosition1(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            import numpy as np
            
            print(var.petrel_name)
            pos = var.ijks_to_positions([[1,2,3],[1,2,3]])
            for v in np.array(pos).transpose().ravel():
                print("{:.1f}".format(v))
            ijks = var.positions_to_ijks(pos)
            ijks
            for v in np.array(ijks).transpose().ravel():
                print("{:.1f}".format(v))
            print()
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_position_1_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Surfacecollection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            print(len(var.surface.parent_collection))
            print(next(iter(var.surface.parent_collection)))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfacecollection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteIsundefFalse(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Returns False if it's a valid value, i.e, not NAN
            #[1,1]== 0 is a valid number
            print(var.is_undef_value(var.all().as_array()[1,1]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_isundef_false_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteChunk(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            ok = True
            chunk_0 = var.chunk((4,5), (4, 5))
            data = chunk_0.as_array().flat
            data_vec = [v for v in data]
            if 4 != len(data_vec):
                ok = False
                print("4 != len(data_vec)")
            if [int(v) for v in data_vec] != [0, 0, 0, 0]:
                ok = False
                print("[int(v) for v in data_vec] != [0, 0, 0,0]")
            chunk_1 = var.chunk((4,4), (4,4))
            chunk_1.set(42)
            chunk_2 = var.chunk((4,5), (4, 5))
            new_data_vec = [int(v) for v in chunk_2.as_array().flat]
            if [int(v) for v in new_data_vec] != [42, 0, 0, 0]:
                ok = False
                print("[int(v) for v in new_data_vec] != [42, 0, 0, 0]")
                print([int(v) for v in new_data_vec])
            chunk_1.set(0)
            print(ok)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_chunk_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteDiscretecodes(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #prints the Discrete codes and values
            print(var.discrete_codes)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_discretecodes_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteDiscretecodeschange(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Change the Discrete code. Change is not persistent and Petrel object is not affected
            original_value = var.discrete_codes[1]
            var.discrete_codes[1] = "Sand sand"
            print(var.discrete_codes)
            
            # Reset values
            var.discrete_codes[1] = original_value
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_discretecodeschange_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteHassameparent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        var_1 = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var_1.readonly = False
        try:
            #Ture is both properties have same Parent
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_hassameparent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteHassameparentValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        var_1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var_1.readonly = False
        try:
            #ValueError is throwm if Discrete Surface property is compared with Seismic 3D
            print(var.has_same_parent(var_1))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_hassameparent_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteIsundefTrue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Returns True if the value is NAN
            #First manually set the value to NAN and then do the is_undef
            
            layer = var.all().as_array()
            original_value = layer[0,0]
            layer[0,0] = var.undef_value
            var.all().set(layer)
            print(var.is_undef_value(var.all().as_array()[0,0]))
            
            # Reset value
            layer[0,0] = original_value
            var.all().set(layer)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_isundef_true_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteParentsurface(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Prints the parent surface Petrel name
            print(var.surface.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_parentsurface_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteParentsurfaceextent(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #prints the maximum i & j indices. k will always be zero
            print(var.surface.extent)
            print(var.surface.extent.i)
            print(var.surface.extent.j)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_parentsurfaceextent_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteParentsurfaceindices(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #prints the indices of the cell at the given (x,y) location
            print(var.surface.indices(484155, 6224170))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_parentsurfaceindices_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteParentsurfaceindicesValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown when (x,y) is outside the Surface
            print(var.surface.indices(400, 600))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_parentsurfaceindices_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteParentsurfaceposition(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Prints the (x,y,z) position of the cell at the given (i,j).
            print(var.surface.position(32,25))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_parentsurfaceposition_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteParentsurfacepositionValueerror(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #ValueError is thrown when (i,j) is outside the Surface geometry
            print(var.surface.position(131,154))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_parentsurfaceposition_valueerror_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscretePetrelname(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Prints the Discrete Surface property Petrel name
            print(var.petrel_name)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_petrelname_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteReadonly(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = True
        try:
            #Cannot write to the property when 'Read only' is checked
            layer = var.all().as_array()
            layer[0,0] = 0
            var.all().set(layer)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_readonly_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteRetrievestats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            def mylen(d):
                # Can't use built-in len as CPython doesn't know how to the __len__ of a C# Dictionary, although it can iterate over it (using Python.NET)...
                l = 0
                for k in d:
                    l = l + 1
                return l
            
            print(mylen(var.retrieve_stats()) > 0)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_retrievestats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteSetundefvalue(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #First set the value to 'undef-value', then change it back to a 'def' value
            #For Discrete Surface 'undef_value' = 2417483647 (MAXINT)
            
            layer = var.all().as_array()
            original_value = layer[0, 0]
            layer[0,0] = var.undef_value
            var.all().set(layer)
            print(var.all().as_array()[0,0])
            print(var.is_undef_value(var.all().as_array()[0,0]))
            
            layer = var.all().as_array()
            layer[0,0] = -27
            var.all().set(layer)
            print(var.all().as_array()[0,0])
            print(var.is_undef_value(var.all().as_array()[0,0]))
            
            # Reset value
            layer[0, 0] = original_value
            var.all().set(layer)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_setundefvalue_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteUnitsymbol(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Prints the units for the Discrete Surface property
            print(var.unit_symbol)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_unitsymbol_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteUpdaterawvalues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            #Can chnage the values when 'Read only' is unchecked
            layer = var.all().as_array()
            original_value = layer[0,0]
            layer[0,0] = 12
            var.all().set(layer)
            print(var.all().as_array()[0,0])
            
            # Reset values
            layer[0,0] = original_value
            var.all().set(layer)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_updaterawvalues_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeChunk(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            ok = True
            chunk_0 = var.chunk((4,4), (4, 4))
            data = chunk_0.as_array().flat
            data_vec = [v for v in data]
            if 1 != len(data_vec):
                ok = False
                print("1 != len(data_vec)\n")
            # Or statement because value of changes depending on what petrel tests has been run
            # before.
            if not ([int(v) for v in data_vec] == [-2709] or [int(v) for v in data_vec] == [-2711]):
                ok = False
                print("not ([int(v) for v in data_vec] == [-2709] or [int(v) for v in data_vec] == [-2711]), actually it is {}\n"
                            .format([int(v) for v in data_vec]))
            
            old_value = data_vec[0] 
            chunk_1 = var.chunk((4,4), (4,4))
            chunk_1.set(-3000)
            chunk_2 = var.chunk((4,4), (4, 4))
            new_data_vec = [int(v) for v in chunk_2.as_array().flat]
            if not [int(v) for v in new_data_vec] == [-3000]:
                ok = False
                print("not [int(v) for v in new_data_vec] == [-3000], actually it is {}\n"
                      .format([int(v) for v in new_data_vec]))
            chunk_1.set(old_value)
            print(ok)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_chunk_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            rho = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
            try:
                rho_copy = rho.clone('Rho_copy', copy_values = True)
            except Exception:
                rho_copy = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho_copy')
            
            print(rho.path)
            print(rho_copy.path)
            
            rho_layer = rho.layer(100).as_array()
            rho_copy_layer = rho_copy.layer(100).as_array()
            
            for i in range(0, 100, 20):
                for j in range(0, 50, 10):
                    print('{:.4f}'.format(rho_layer[i, j]) , '{:.4f}'.format(rho_copy_layer[i, j]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            facies = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
            try:
                facies_copy = facies.clone('Facies_copy', copy_values = True)
            except Exception:
                facies_copy = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies_copy', discrete = True)
            
            print(facies.path)
            print(facies_copy.path)
            
            facies_layer = facies.layer(100).as_array()
            facies_copy_layer = facies_copy.layer(100).as_array()
            
            i = 36
            j = 31
            for k in range (430, 620, 10):
                facies_layer = facies.layer(k).as_array()
                val = facies_layer[i, j]
                print(k, i, j, facies_layer[i, j] , facies_copy_layer[i, j])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            log_vs = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs')
            try:
                log_vs_copy = log_vs.clone('Vs_copy', copy_values = True)
            except Exception:
                log_vs_copy = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Vs_copy')
            
            print(log_vs.path)
            print(log_vs_copy.path)
            
            log_vs_samples = log_vs.samples
            log_vs_copy_samples = log_vs_copy.samples
            
            for i in range(9300, 10000, 100):
                s = log_vs_samples.at(i)
                s_copy = log_vs_copy_samples.at(i)
                print(i, s)
                print(i, s_copy)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllog_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WelllogdiscreteCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            log_facies = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies', discrete = True)  
            try:
                log_facies_copy = log_facies.clone('Facies_copy', copy_values = True)
            except Exception:
                log_facies_copy = petrellink._get_well_log('Input/Wells/Well_Good/Well logs/Facies_copy', discrete = True)
            
            print(log_facies.path)
            print(log_facies_copy.path)
            
            log_facies_samples = log_facies.samples
            log_facies_copy_samples = log_facies_copy.samples
            
            for i in range(9300, 10000, 100):
                s = log_facies_samples.at(i)
                s_copy = log_facies_copy_samples.at(i)
                print()
                print(i, s)
                print(i, s_copy)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\welllogdiscrete_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            surface_twt = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
            try:
                surface_twt_copy = surface_twt.clone('TWT_copy', copy_values = True)
            except Exception:
                surface_twt_copy = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT_copy')
            
            print(surface_twt.path)
            print(surface_twt_copy.path)
            
            surface_twt_values = surface_twt.all().as_array()
            surface_twt_copy_values = surface_twt_copy.all().as_array()
            
            for i in range(0, 100, 20):
                for j in range(0, 50, 10):
                    print('{:.4f}'.format(surface_twt_values[i, j]) , '{:.4f}'.format(surface_twt_copy_values[i, j]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeCloneNocopyOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            surface_twt = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
            try:
                surface_twt_copy = surface_twt.clone('TWT_nocopy', copy_values = False)
            except Exception:
                surface_twt_copy = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT_nocopy')
            
            print(surface_twt.path)
            print(surface_twt_copy.path)
            
            surface_twt_copy_values = surface_twt_copy.all().as_array()
            
            for i in range(0, 100, 20):
                for j in range(0, 50, 10):
                    print('{:.4f}'.format(0.0) , '{:.4f}'.format(surface_twt_copy_values[i, j]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_clone_nocopy_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            try:
                is_oop
            except NameError:
                is_oop = False
            
            surface_facies = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
            if is_oop:
                surface_facies.readonly = False
            
            with surface_facies.all().values() as vals:
                original_value = vals[40, 50]
                vals[40, 50] = 9
            
            try:
                surface_facies_copy = surface_facies.clone('Facies_copy', copy_values = True)
            except Exception:
                surface_facies_copy = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies_copy', discrete = True)
                
            print(surface_facies.path)
            print(surface_facies_copy.path)
            
            surface_facies_values = surface_facies.all().as_array()
            surface_facies_copy_values = surface_facies_copy.all().as_array()
            
            all_equal = True
            for i in range(0, 131, 10):
                for j in range(0, 75, 10):
                    val = surface_facies_values[i, j]
                    val_copy = surface_facies_copy_values[i, j]
                    all_equal = all_equal and val == val_copy
                    if val > 0 or val_copy > 0:
                        print(i, j, val, val_copy)
            
            print(all_equal)
            
            # Reset value
            with surface_facies.all().values() as vals:
                vals[40, 50] = original_value
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            seismic3d = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
            try:
                seismic3d_copy = seismic3d.clone('Seismic3D_copy', copy_values = True)
            except Exception:
                seismic3d_copy = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D_copy')
            
            print(seismic3d.path)
            print(seismic3d_copy.path)
            
            seismic3d_layer = seismic3d.layer(100).as_array()
            seismic3d_copy_layer = seismic3d_copy.layer(100).as_array()
            
            for i in range(0, 100, 20):
                for j in range(0, 50, 10):
                    print(i, j, '{:.4f}'.format(seismic3d_layer[i, j]) , '{:.4f}'.format(seismic3d_copy_layer[i, j]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic2dCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            seismic2d = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D')
            try:
                seismic2d_copy = seismic2d.clone('Seismic2D_copy', copy_values = True)
            except Exception:
                seismic2d_copy = petrellink._get_seismic_2d('Input/Seismic/Survey 1/Seismic2D_copy')
            
            print(seismic2d.path)
            print(seismic2d_copy.path)
            
            seismic2d_column = seismic2d.column(50).as_array()
            seismic2d_copy_column = seismic2d_copy.column(50).as_array()
            
            for k in range(0, 100, 10):
                print(k, '{:.4f}'.format(seismic2d_column[k]) , '{:.4f}'.format(seismic2d_copy_column[k]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic2D_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogSmoketest(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_global_well_log('Input/Wells/Global well logs/GR')
        var.readonly = True
        try:
            for log in var.logs:
                print (log)
                print (log.well)
                print (len(log.samples))
            
            
            print(var.log('Well_Good'))
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllog_smoketest_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogLog(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_global_well_log('Input/Wells/Global well logs/GR')
        var.readonly = True
        try:
            print(var.log('Well_Good'))
            
            try:
                print(var.log('Well_Goodie'))
            except Exception as exc:
                print(exc)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllog_log_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogBasic(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_global_well_log('Input/Wells/Global well logs/GR')
        var.readonly = False
        try:
            print(var.petrel_name)
            print(var.unit_symbol)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllog_basic_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            gr = petrellink._get_global_well_log('Input/Wells/Global well logs/GR')
            try:
                gr_copy = gr.clone('GR_copy')
            except Exception:
                gr_copy = petrellink._get_global_well_log('Input/Wells/Global well logs/GR_copy')
            
            print(gr.path)
            print(gr_copy.path)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllog_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogdiscreteCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            g_facies = petrellink._get_global_well_log('Input/Wells/Global well logs/Facies', discrete=True)
            try:
                g_facies_copy = g_facies.clone('Facies_copy')
            except Exception:
                g_facies_copy = petrellink._get_global_well_log('Input/Wells/Global well logs/Facies_copy')
            
            print(g_facies.path)
            print(g_facies_copy.path)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllogdiscrete_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogdiscreteLog(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        facies_global = petrellink._get_global_well_log('Input/Wells/Global well logs/Facies', discrete = True)
        facies_global.readonly = False
        try:
            print(facies_global.log('Well_Good'))
            
            try:
                print(facies_global.log('Well_Goodie'))
            except Exception as exc:
                print(exc)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllogdiscrete_log_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogdiscreteLogs(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        facies_global = petrellink._get_global_well_log('Input/Wells/Global well logs/Facies', discrete = True)
        facies_global.readonly = False
        try:
            print("\n".join([v.petrel_name for v in facies_global.logs]))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllogdiscrete_logs_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GlobalwelllogdiscreteWithKey(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        facies_global = petrellink._get_global_well_log('Input/Wells/Global well logs/Facies', discrete = True)
        facies_global.readonly = False
        try:
            print(facies_global.log('Well_Good'))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\globalwelllogdiscrete_with_key_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PointsetCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            ps = petrellink.pointsets['Input/Geometry/Points 1']
            try:
                ps_clone = ps.clone('Points 1_copy', copy_values = True)
            except:
                ps_clone = petrellink.pointsets['Input/Geometry/Points 1_copy']
            
            print(ps.path)
            print(ps_clone.path)
            
            print('')
            points = ps.points
            points_clone = ps_clone.points
            for i in range(len(points)):
                print('%.2f' % points[i].x,
                    '%.2f' % points[i].y,
                    '%.2f' % points[i].z,
                    ' = ',
                    '%.2f' % points_clone[i].x,
                    '%.2f' % points_clone[i].y,
                    '%.2f' % points_clone[i].z)
            
            props = ps.as_dataframe()
            props_clone = ps_clone.as_dataframe()
            
            print('')
            
            for key in list(props):
                print(key, ': ', end='')
            
                vals = props[key]
                
                # Behavior change in Petrel 2021. In new PointSets TWTAuto property is named 'TWT' instead of 'TWT auto'
                vals_copy = props_clone['TWT'] if key == 'TWT auto' and not 'TWT auto' in props_clone.columns else props_clone[key]
                
                for i in range(len(vals)):
                    if isinstance(vals[i], float):
                        print('%.2f' % vals[i], ' = ', '%.2f' % vals_copy[i], end='')
                    else:
                        print(vals[i], ' = ', vals_copy[i], end='')
                print('')
            
            
            ps = petrellink.pointsets['Input/Geometry/Points 1 many points']
            try:
                ps_clone = ps.clone('Points 1 many points_copy', copy_values = True)
            except:
                ps_clone = petrellink.pointsets['Input/Geometry/Points 1 many points_copy']
            
            print(ps.path)
            print(ps_clone.path)
            
            print('')
            points = ps.points
            points_clone = ps_clone.points
            for i in range(len(points)):
                print('%.2f' % points[i].x,
                    '%.2f' % points[i].y,
                    '%.2f' % points[i].z,
                    ' = ',
                    '%.2f' % points_clone[i].x,
                    '%.2f' % points_clone[i].y,
                    '%.2f' % points_clone[i].z)
            
            props = ps.as_dataframe()
            props_clone = ps_clone.as_dataframe()
            
            print('')
            
            for key in list(props):
                print(key, ': ', end='')
            
                vals = props[key]
                
                # Behavior change in Petrel 2021. In new PointSets TWTAuto property is named 'TWT' instead of 'TWT auto'
                vals_copy = props_clone['TWT'] if key == 'TWT auto' and not 'TWT auto' in props_clone.columns else props_clone[key]
                
                for i in range(len(vals)):
                    if isinstance(vals[i], float):
                        print('%.2f' % vals[i], ' = ', '%.2f' % vals_copy[i], end='')
                    else:
                        print(vals[i], ' = ', vals_copy[i], end='')
                print('')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\pointset_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PolylinesetCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            ps = petrellink._get_polylineset('Input/Geometry/Polygon')
            try:
                ps_clone = ps.clone('Polygon_copy', copy_values = True)
            except:
                ps_clone = petrellink._get_polylineset('Input/Geometry/Polygon_copy')
            
            try:
                ps_clone_noval = ps.clone('Polygon_copy_noval', copy_values = False)
            except:
                ps_clone_noval = petrellink._get_polylineset('Input/Geometry/Polygon_copy_noval')
            
            print(ps.path)
            print(ps_clone.path)
            print(ps_clone_noval.path)
            
            print('points')
            lines = ps.polylines
            lines_clone = ps_clone.polylines
            lines_clone_noval = ps_clone_noval.polylines
            
            
            for line in lines:
                for point in line.points:
                    print('%.2f' % point.x, '%.2f' % point.y, '%.2f' % point.z)
            
            print('')
            
            for line in lines_clone:
                for point in line.points:
                    print('%.2f' % point.x, '%.2f' % point.y, '%.2f' % point.z)
                 
            print('')
                
            for line in lines_clone_noval:
                for point in line.points:
                    print('%.2f' % point.x, '%.2f' % point.y, '%.2f' % point.z)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\polylineset_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizoninterpretation3dCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            hi = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU/Ardmore')
            try:
                hi_clone = hi.clone('Ardmore_clone', copy_values = True)
            except:
                hi_clone = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU_copy/Ardmore_clone')
            
            print(hi.path)
            print(hi_clone.path)
            
            print()
            
            print('** Source **')
            
            print('Extent:', hi.extent)
            print(hi.position(200, 202))
            
            for prop in hi.horizon_property_3ds:
                if prop.petrel_name == "TWT":
                    print()
                    print(prop)
            
                    chunk = prop.chunk((200, 201), (202, 203))
                    vals = chunk.as_array()
                    for i in [0, 1]:
                        for j in [0, 1]:
                            print('%.4f' % vals[i, j], '', end='')
                    print()
                else:
                    print()
                    print(prop)
            
                    prop.readonly = False
                    chunk = prop.chunk((200, 201), (202, 203))
                    with chunk.values() as vals:
                        for i in [0, 1]:
                            for j in [0, 1]:
                                print('%.4f' % vals[i, j], '', end='')
                        print()
            
            print()
            print('** Clone **')
            
            print('Extent:', hi_clone.extent)
            print(hi_clone.position(200, 202))
            
            for prop in hi_clone.horizon_property_3ds:
                if prop.petrel_name == "TWT":
                    print()
                    print(prop)
            
                    chunk = prop.chunk((200, 201), (202, 203))
                    vals = chunk.as_array()
                    for i in [0, 1]:
                        for j in [0, 1]:
                            print('%.4f' % vals[i, j], '', end='')
                    print()
                else:
                    print()
                    print(prop)
            
                    prop.readonly = False
                    chunk = prop.chunk((200, 201), (202, 203))
                    with chunk.values() as vals:
                        for i in [0, 1]:
                            for j in [0, 1]:
                                print('%.4f' % vals[i, j], '', end='')
                        print()
            
            
            try:
                hi_clone = hi.clone('Ardmore_clone_noval', copy_values = False)
            except:
                hi_clone = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU_copy/Ardmore_clone_noval')
            
            print()
            print(hi_clone.path)
            print()
            
            print('** Clone noval**')
            
            print('Extent:', hi_clone.extent)
            print(hi_clone.position(200, 202))
            
            for prop in hi_clone.horizon_property_3ds:
                if prop.petrel_name == "TWT":
                    print()
                    print(prop)
            
                    chunk = prop.chunk((200, 201), (202, 203))
                    vals = chunk.as_array()
                    for i in [0, 1]:
                        for j in [0, 1]:
                            print('%.4f' % vals[i, j], '', end='')
                    print()
                else:
                    print()
                    print(prop)
            
                    prop.readonly = False
                    chunk = prop.chunk((200, 201), (202, 203))
                    with chunk.values() as vals:
                        for i in [0, 1]:
                            for j in [0, 1]:
                                print('%.4f' % vals[i, j], '', end='')
                        print()
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizoninterpretation3D_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizonproperty3dCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            horizon = petrellink.horizon_interpretation_3ds['Input/Seismic/Interpretation folder 1/BCU/Ardmore']
            horizonproperty = petrellink.horizon_properties['Input/Seismic/Interpretation folder 1/BCU/Ardmore/TWT']
            
            print(horizon.path)
            print(horizonproperty.path)
            
            new_property_no_copy = horizonproperty.clone("new_property_no_copy_clone", copy_values=False)
            new_property_do_copy = horizonproperty.clone("new_property_do_copy_clone", copy_values=True)
            
            not_copied_values = new_property_no_copy.all().as_array()
            copied_values = new_property_do_copy.all().as_array()
            orig_values = horizonproperty.all().as_array()
            
            for i in range(5):
                for j in range(5):
                    print("{:.2f}, {:.2f}, {:.2f}".format(orig_values[i,j], copied_values[i,j], not_copied_values[i, j]))
            
            print("\n".join([str(h) for h in horizon.horizon_property_3ds]))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizonproperty3D_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveyBasic(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_explicit_well_survey('Input/Wells/Well_Good/Explicit survey 1')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good/XYZ')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good/XYTVD')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good/DXDYTVD')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good/MDINCLAZIM')
        var_4.readonly = False
        try:
            # var -> Explicit survey
            print(var.petrel_name)
            print(var.well)
            print(var.well_survey_type)
            print(var.record_count)
            var_df = var.as_dataframe()
            print(len(var_df.index))
            print(var_df.columns)
            
            # var_1 -> XYZ well survey
            print(var_1.petrel_name)
            print(var_1.well)
            print(var_1.well_survey_type)
            print(var_1.record_count)
            var_1_df = var_1.as_dataframe()
            print(len(var_1_df.index))
            print(var_1_df.columns)
            
            # var_2 -> XYTVD well survey
            print(var_2.petrel_name)
            print(var_2.well)
            print(var_2.well_survey_type)
            print(var_2.record_count)
            var_2_df = var_2.as_dataframe()
            print(len(var_2_df.index))
            print(var_2_df.columns)
            
            # var_3 -> DXDYTVD well survey
            print(var_3.petrel_name)
            print(var_3.well)
            print(var_3.well_survey_type)
            print(var_3.azimuth_reference)
            print(var_3.record_count)
            var_3_df = var_3.as_dataframe()
            print(len(var_3_df.index))
            print(var_3_df.columns)
            
            # var_4 -> MD incl azim well survey
            print(var_4.petrel_name)
            print(var_4.well)
            print(var_4.well_survey_type)
            print(var_4.azimuth_reference)
            print(var_4.record_count)
            var_4_df = var_4.as_dataframe()
            print(len(var_4_df.index))
            print(var_4_df.columns)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_basic_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveySetSurveyAsDefinitive(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_explicit_well_survey('Input/Wells/Well_Good/Explicit survey 1')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good/XYZ')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good/XYTVD')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good/DXDYTVD')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good/MDINCLAZIM')
        var_4.readonly = False
        well = petrellink._get_well('Input/Wells/Well_Good')
        well.readonly = False
        try:
            print(well.retrieve_stats().get('Number of points'))
            
            # var_1 -> XYZ well survey
            var_1.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            var.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            
            # var_2 -> XYTVD well survey
            var_2.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            var.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            
            # var_3 -> DXDYTVD well survey
            var_3.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            var.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            
            # var_4 -> MD incl azim well survey
            var_4.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
            
            # Explicit at the end to not introduce changes into the project
            # var -> Explicit survey
            var.set_survey_as_definitive()
            print(well.retrieve_stats().get('Number of points'))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_set_survey_as_definitive_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveyCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_explicit_well_survey('Input/Wells/Well_Good/Explicit survey 1')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good/XYZ')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good/XYTVD')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good/DXDYTVD')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good/MDINCLAZIM')
        var_4.readonly = False
        try:
            # var -> Explicit survey
            print(var.path)
            var_df = var.as_dataframe()
            print(var_df.columns)
            print(len(var_df.index))
            
            var_clone_copy = var.clone(var.petrel_name + "_clone_copy", copy_values=True)
            print(var_clone_copy.path)
            var_clone_copy_df = var_clone_copy.as_dataframe()
            print(var_clone_copy_df.columns)
            print(len(var_clone_copy_df.index))
            
            var_clone_nocopy = var.clone(var.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_clone_nocopy.path)
            var_clone_nocopy_df = var_clone_nocopy.as_dataframe()
            print(var_clone_nocopy_df.columns)
            print(len(var_clone_nocopy_df.index))
            
            # var_1 -> XYZ well survey
            print(var_1.path)
            var_1_df = var_1.as_dataframe()
            print(var_1_df.columns)
            print(len(var_1_df.index))
            
            var_1_clone_copy = var_1.clone(var_1.petrel_name + "_clone_copy", copy_values=True)
            print(var_1_clone_copy.path)
            var_1_clone_copy_df = var_1_clone_copy.as_dataframe()
            print(var_1_clone_copy_df.columns)
            print(len(var_1_clone_copy_df.index))
            
            var_1_clone_nocopy = var_1.clone(var_1.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_1_clone_nocopy.path)
            var_1_clone_nocopy_df = var_1_clone_nocopy.as_dataframe()
            print(var_1_clone_nocopy_df.columns)
            print(len(var_1_clone_nocopy_df.index))
            
            # var_2 -> XYTVD well survey
            print(var_2.path)
            var_2_df = var_2.as_dataframe()
            print(var_2_df.columns)
            print(len(var_2_df.index))
            
            var_2_clone_copy = var_2.clone(var_2.petrel_name + "_clone_copy", copy_values=True)
            print(var_2_clone_copy.path)
            var_2_clone_copy_df = var_2_clone_copy.as_dataframe()
            print(var_2_clone_copy_df.columns)
            print(len(var_2_clone_copy_df.index))
            
            var_2_clone_nocopy = var_2.clone(var_2.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_2_clone_nocopy.path)
            var_2_clone_nocopy_df = var_2_clone_nocopy.as_dataframe()
            print(var_2_clone_nocopy_df.columns)
            print(len(var_2_clone_nocopy_df.index))
            
            # var_3 -> DXDYTVD well survey
            print(var_3.path)
            var_3_df = var_3.as_dataframe()
            print(var_3_df.columns)
            print(len(var_3_df.index))
            
            var_3_clone_copy = var_3.clone(var_3.petrel_name + "_clone_copy", copy_values=True)
            print(var_3_clone_copy.path)
            var_3_clone_copy_df = var_3_clone_copy.as_dataframe()
            print(var_3_clone_copy_df.columns)
            print(len(var_3_clone_copy_df.index))
            
            var_3_clone_nocopy = var_3.clone(var_3.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_3_clone_nocopy.path)
            var_3_clone_nocopy_df = var_3_clone_nocopy.as_dataframe()
            print(var_3_clone_nocopy_df.columns)
            print(len(var_3_clone_nocopy_df.index))
            
            # var_4 -> MD incl azim well survey
            print(var_4.path)
            var_4_df = var_4.as_dataframe()
            print(var_4_df.columns)
            print(len(var_4_df.index))
            
            var_4_clone_copy = var_4.clone(var_4.petrel_name + "_clone_copy", copy_values=True)
            print(var_4_clone_copy.path)
            var_4_clone_copy_df = var_4_clone_copy.as_dataframe()
            print(var_4_clone_copy_df.columns)
            print(len(var_4_clone_copy_df.index))
            
            var_4_clone_nocopy = var_4.clone(var_4.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_4_clone_nocopy.path)
            var_4_clone_nocopy_df = var_4_clone_nocopy.as_dataframe()
            print(var_4_clone_nocopy_df.columns)
            print(len(var_4_clone_nocopy_df.index))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveyDroid(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_explicit_well_survey('Input/Wells/Well_Good/Explicit survey 1')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good/XYZ')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good/XYTVD')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good/DXDYTVD')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good/MDINCLAZIM')
        var_4.readonly = False
        try:
            # var -> Explicit survey
            print(var.droid)
            
            # var_1 -> XYZ well survey
            print(var_1.droid)
            
            # var_2 -> XYTVD well survey
            print(var_2.droid)
            
            # var_3 -> DXDYTVD well survey
            print(var_3.droid)
            
            # var_4 -> MD incl azim well survey
            print(var_4.droid)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_droid_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveyRetrievehistory(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_explicit_well_survey('Input/Wells/Well_Good/Explicit survey 1')
        var.readonly = False
        try:
            history_df = var.retrieve_history()
            first_row = history_df.iloc[0, 1:]
            print(first_row)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_retrievehistory_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveySetter(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good/XYZ')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good/XYTVD')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good/DXDYTVD')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good/MDINCLAZIM')
        var_4.readonly = False
        try:
            # var_1 -> XYZ well survey
            print(var_1.petrel_name)
            var_1_df = var_1.as_dataframe()
            var_1_df_orig = var_1.as_dataframe()
            print(var_1_df.columns)
            print(var_1_df.iloc[0,:])
            var_1_df.loc[:,"X"] = var_1_df.loc[:,"X"] + 10
            var_1.set(xs=var_1_df.loc[:,"X"], ys=var_1_df.loc[:,"Y"], zs=var_1_df.loc[:,"Z"])
            var_1_df = var_1.as_dataframe()
            print(var_1_df.columns)
            print(var_1_df.iloc[0,:])
            var_1.set(xs=var_1_df_orig.loc[:,"X"], ys=var_1_df_orig.loc[:,"Y"], zs=var_1_df_orig.loc[:,"Z"])
            
            # var_2 -> XYTVD well survey
            print(var_2.petrel_name)
            var_2_df = var_2.as_dataframe()
            var_2_df_orig = var_2.as_dataframe()
            print(var_2_df.columns)
            print(var_2_df.iloc[0,:])
            var_2_df.loc[:,"X"] = var_2_df.loc[:,"X"] + 10
            var_2.set(xs=var_2_df.loc[:,"X"], ys=var_2_df.loc[:,"Y"], tvds=var_2_df.loc[:,"TVD"])
            var_2_df = var_2.as_dataframe()
            print(var_2_df.columns)
            print(var_2_df.iloc[0,:])
            var_2.set(xs=var_2_df_orig.loc[:,"X"], ys=var_2_df_orig.loc[:,"Y"], tvds=var_2_df_orig.loc[:,"TVD"])
            
            # var_3 -> DXDYTVD well survey
            print(var_3.petrel_name)
            var_3_df = var_3.as_dataframe()
            var_3_df_orig = var_3.as_dataframe()
            print(var_3_df.columns)
            print(var_3_df.iloc[0,:])
            var_3_df.loc[:,"DX"] = var_3_df.loc[:,"DX"] + 10
            var_3.set(dxs=var_3_df.loc[:,"DX"], dys=var_3_df.loc[:,"DY"], tvds=var_3_df.loc[:,"TVD"])
            var_3_df = var_3.as_dataframe()
            print(var_3_df.columns)
            print(var_3_df.iloc[0,:])
            var_3.set(dxs=var_3_df_orig.loc[:,"DX"], dys=var_3_df_orig.loc[:,"DY"], tvds=var_3_df_orig.loc[:,"TVD"])
            
            # var_4 -> MD incl azim well survey
            print(var_4.petrel_name)
            var_4_df = var_4.as_dataframe()
            var_4_df_orig = var_4.as_dataframe()
            print(var_4_df.columns)
            print(var_4_df.iloc[0,:])
            var_4_df.loc[:,"MD"] = var_4_df.loc[:,"MD"] + 10
            var_4.set(mds=var_4_df.loc[:,"MD"], incls=var_4_df.loc[:,"Inclination"], azims=var_4_df.loc[:,"Azimuth GN"])
            var_4_df = var_4.as_dataframe()
            print(var_4_df.columns)
            print(var_4_df.iloc[0,:])
            var_4.set(mds=var_4_df_orig.loc[:,"MD"], incls=var_4_df_orig.loc[:,"Inclination"], azims=var_4_df_orig.loc[:,"Azimuth GN"])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_setter_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveySetterExplicit(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_explicit_well_survey('Input/Wells/Well_Good/Explicit survey 1')
        var.readonly = False
        try:
            # var -> Explicit survey
            print(var.petrel_name)
            var_df = var.as_dataframe()
            var_df.loc[:,"X"] = var_df.loc[:,"X"] + 10
            var.set(xs=var_df.loc[:,"X"], ys=var_df.loc[:,"Y"], zs=var_df.loc[:,"Z"], mds=var_df.loc[:,"MD"], incls=var_df.loc[:,"Inclination"], azims=var_df.loc[:,"Azimuth GN"])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurvey_setter_explicit_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveylateralBasic(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral to explicit')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good lateral/XYZ lateral')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good lateral/DXDYTVD lateral')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good lateral/MDINCLAZIM lateral')
        var_4.readonly = False
        try:
            # var -> XYTVD lateral survey tied to Explicit
            print(var.petrel_name)
            print(var.well)
            print(var.well_survey_type)
            print(var.record_count)
            var_df = var.as_dataframe()
            print(len(var_df.index))
            print(var_df.columns)
            
            # var_1 -> XYZ lateral well survey
            print(var_1.petrel_name)
            print(var_1.well)
            print(var_1.well_survey_type)
            print(var_1.record_count)
            var_1_df = var_1.as_dataframe()
            print(len(var_1_df.index))
            print(var_1_df.columns)
            
            # var_2 -> XYTVD lateral well survey
            print(var_2.petrel_name)
            print(var_2.well)
            print(var_2.well_survey_type)
            print(var_2.record_count)
            var_2_df = var_2.as_dataframe()
            print(len(var_2_df.index))
            print(var_2_df.columns)
            
            # var_3 -> DXDYTVD lateral well survey
            print(var_3.petrel_name)
            print(var_3.well)
            print(var_3.well_survey_type)
            print(var_3.azimuth_reference)
            print(var_3.record_count)
            var_3_df = var_3.as_dataframe()
            print(len(var_3_df.index))
            print(var_3_df.columns)
            
            # var_4 -> MD incl azim lateral well survey
            print(var_4.petrel_name)
            print(var_4.well)
            print(var_4.well_survey_type)
            print(var_4.azimuth_reference)
            print(var_4.record_count)
            var_4_df = var_4.as_dataframe()
            print(len(var_4_df.index))
            print(var_4_df.columns)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurveylateral_basic_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveylateralCloneOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral to explicit')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good lateral/XYZ lateral')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good lateral/DXDYTVD lateral')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good lateral/MDINCLAZIM lateral')
        var_4.readonly = False
        try:
            # var -> Explicit survey
            print(var.path)
            var_df = var.as_dataframe()
            print(var_df.columns)
            print(len(var_df.index))
            
            var_clone_copy = var.clone(var.petrel_name + "_clone_copy", copy_values=True)
            print(var_clone_copy.path)
            var_clone_copy_df = var_clone_copy.as_dataframe()
            print(var_clone_copy_df.columns)
            print(len(var_clone_copy_df.index))
            
            var_clone_nocopy = var.clone(var.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_clone_nocopy.path)
            var_clone_nocopy_df = var_clone_nocopy.as_dataframe()
            print(var_clone_nocopy_df.columns)
            print(len(var_clone_nocopy_df.index))
            
            # var_1 -> XYZ well survey
            print(var_1.path)
            var_1_df = var_1.as_dataframe()
            print(var_1_df.columns)
            print(len(var_1_df.index))
            
            var_1_clone_copy = var_1.clone(var_1.petrel_name + "_clone_copy", copy_values=True)
            print(var_1_clone_copy.path)
            var_1_clone_copy_df = var_1_clone_copy.as_dataframe()
            print(var_1_clone_copy_df.columns)
            print(len(var_1_clone_copy_df.index))
            
            var_1_clone_nocopy = var_1.clone(var_1.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_1_clone_nocopy.path)
            var_1_clone_nocopy_df = var_1_clone_nocopy.as_dataframe()
            print(var_1_clone_nocopy_df.columns)
            print(len(var_1_clone_nocopy_df.index))
            
            # var_2 -> XYTVD well survey
            print(var_2.path)
            var_2_df = var_2.as_dataframe()
            print(var_2_df.columns)
            print(len(var_2_df.index))
            
            var_2_clone_copy = var_2.clone(var_2.petrel_name + "_clone_copy", copy_values=True)
            print(var_2_clone_copy.path)
            var_2_clone_copy_df = var_2_clone_copy.as_dataframe()
            print(var_2_clone_copy_df.columns)
            print(len(var_2_clone_copy_df.index))
            
            var_2_clone_nocopy = var_2.clone(var_2.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_2_clone_nocopy.path)
            var_2_clone_nocopy_df = var_2_clone_nocopy.as_dataframe()
            print(var_2_clone_nocopy_df.columns)
            print(len(var_2_clone_nocopy_df.index))
            
            # var_3 -> DXDYTVD well survey
            print(var_3.path)
            var_3_df = var_3.as_dataframe()
            print(var_3_df.columns)
            print(len(var_3_df.index))
            
            var_3_clone_copy = var_3.clone(var_3.petrel_name + "_clone_copy", copy_values=True)
            print(var_3_clone_copy.path)
            var_3_clone_copy_df = var_3_clone_copy.as_dataframe()
            print(var_3_clone_copy_df.columns)
            print(len(var_3_clone_copy_df.index))
            
            var_3_clone_nocopy = var_3.clone(var_3.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_3_clone_nocopy.path)
            var_3_clone_nocopy_df = var_3_clone_nocopy.as_dataframe()
            print(var_3_clone_nocopy_df.columns)
            print(len(var_3_clone_nocopy_df.index))
            
            # var_4 -> MD incl azim well survey
            print(var_4.path)
            var_4_df = var_4.as_dataframe()
            print(var_4_df.columns)
            print(len(var_4_df.index))
            
            var_4_clone_copy = var_4.clone(var_4.petrel_name + "_clone_copy", copy_values=True)
            print(var_4_clone_copy.path)
            var_4_clone_copy_df = var_4_clone_copy.as_dataframe()
            print(var_4_clone_copy_df.columns)
            print(len(var_4_clone_copy_df.index))
            
            var_4_clone_nocopy = var_4.clone(var_4.petrel_name + "_clone_nocopy", copy_values=False)
            print(var_4_clone_nocopy.path)
            var_4_clone_nocopy_df = var_4_clone_nocopy.as_dataframe()
            print(var_4_clone_nocopy_df.columns)
            print(len(var_4_clone_nocopy_df.index))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurveylateral_clone_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveylateralDroid(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral to explicit')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good lateral/XYZ lateral')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good lateral/DXDYTVD lateral')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good lateral/MDINCLAZIM lateral')
        var_4.readonly = False
        try:
            # var -> XYTVD lateral survey tied to Explicit
            print(var.droid)
            
            # var_1 -> XYZ lateral well survey
            print(var_1.droid)
            
            # var_2 -> XYTVD lateral well survey
            print(var_2.droid)
            
            # var_3 -> DXDYTVD lateral well survey
            print(var_3.droid)
            
            # var_4 -> MD incl azim lateral well survey
            print(var_4.droid)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurveylateral_droid_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellsurveylateralSetter(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral to explicit')
        var.readonly = False
        var_1 = petrellink._get_xyz_well_survey('Input/Wells/Well_Good lateral/XYZ lateral')
        var_1.readonly = False
        var_2 = petrellink._get_xytvd_well_survey('Input/Wells/Well_Good lateral/XYTVD lateral')
        var_2.readonly = False
        var_3 = petrellink._get_dxdytvd_well_survey('Input/Wells/Well_Good lateral/DXDYTVD lateral')
        var_3.readonly = False
        var_4 = petrellink._get_mdinclazim_well_survey('Input/Wells/Well_Good lateral/MDINCLAZIM lateral')
        var_4.readonly = False
        try:
            # var -> XYTVD lateral survey tied to Explicit
            print(var.petrel_name)
            var_df = var.as_dataframe()
            var_df_orig = var.as_dataframe()
            print(var_df.columns)
            print(var_df.iloc[0,:])
            var_df.loc[:,"X"] = var_df.loc[:,"X"] + 10
            var.set(xs=var_df.loc[:,"X"], ys=var_df.loc[:,"Y"], tvds=var_df.loc[:,"TVD"])
            var_df = var.as_dataframe()
            print(var_df.columns)
            print(var_df.iloc[0,:])
            var.set(xs=var_df_orig.loc[:,"X"], ys=var_df_orig.loc[:,"Y"], tvds=var_df_orig.loc[:,"TVD"])
            
            # var_1 -> XYZ lateral well survey
            print(var_1.petrel_name)
            var_1_df = var_1.as_dataframe()
            var_1_df_orig = var_1.as_dataframe()
            print(var_1_df.columns)
            print(var_1_df.iloc[0,:])
            var_1_df.loc[:,"X"] = var_1_df.loc[:,"X"] + 10
            var_1.set(xs=var_1_df.loc[:,"X"], ys=var_1_df.loc[:,"Y"], zs=var_1_df.loc[:,"Z"])
            var_1_df = var_1.as_dataframe()
            print(var_1_df.columns)
            print(var_1_df.iloc[0,:])
            var_1.set(xs=var_1_df_orig.loc[:,"X"], ys=var_1_df_orig.loc[:,"Y"], zs=var_1_df_orig.loc[:,"Z"])
            
            # var_2 -> XYTVD lateral well survey
            print(var_2.petrel_name)
            var_2_df = var_2.as_dataframe()
            var_2_df_orig = var_2.as_dataframe()
            print(var_2_df.columns)
            print(var_2_df.iloc[0,:])
            var_2_df.loc[:,"X"] = var_2_df.loc[:,"X"] + 10
            var_2.set(xs=var_2_df.loc[:,"X"], ys=var_2_df.loc[:,"Y"], tvds=var_2_df.loc[:,"TVD"])
            var_2_df = var_2.as_dataframe()
            print(var_2_df.columns)
            print(var_2_df.iloc[0,:])
            var_2.set(xs=var_2_df_orig.loc[:,"X"], ys=var_2_df_orig.loc[:,"Y"], tvds=var_2_df_orig.loc[:,"TVD"])
            
            # var_3 -> DXDYTVD lateral well survey
            print(var_3.petrel_name)
            var_3_df = var_3.as_dataframe()
            var_3_df_orig = var_3.as_dataframe()
            print(var_3_df.columns)
            print(var_3_df.iloc[0,:])
            var_3_df.loc[:,"DX"] = var_3_df.loc[:,"DX"] + 10
            var_3.set(dxs=var_3_df.loc[:,"DX"], dys=var_3_df.loc[:,"DY"], tvds=var_3_df.loc[:,"TVD"])
            var_3_df = var_3.as_dataframe()
            print(var_3_df.columns)
            print(var_3_df.iloc[0,:])
            var_3.set(dxs=var_3_df_orig.loc[:,"DX"], dys=var_3_df_orig.loc[:,"DY"], tvds=var_3_df_orig.loc[:,"TVD"])
            
            # var_4 -> MD incl azim lateral well survey
            print(var_4.petrel_name)
            var_4_df = var_4.as_dataframe()
            var_4_df_orig = var_4.as_dataframe()
            print(var_4_df.columns)
            print(var_4_df.iloc[0,:])
            var_4_df.loc[:,"MD"] = var_4_df.loc[:,"MD"] + 10
            var_4.set(mds=var_4_df.loc[:,"MD"], incls=var_4_df.loc[:,"Inclination"], azims=var_4_df.loc[:,"Azimuth GN"])
            var_4_df = var_4.as_dataframe()
            print(var_4_df.columns)
            print(var_4_df.iloc[0,:])
            var_4.set(mds=var_4_df_orig.loc[:,"MD"], incls=var_4_df_orig.loc[:,"Inclination"], azims=var_4_df_orig.loc[:,"Azimuth GN"])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\wellsurveylateral_setter_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellSurveys(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_well('Input/Wells/Well_Good')
        var.readonly = False
        var_1 = petrellink._get_well('Input/Wells/Well_Good lateral')
        var_1.readonly = False
        try:
            print(len(var.surveys))
            for sur in var.surveys:
                print(sur)
            
            print(len(var_1.surveys))
            for sur in var_1.surveys:
                print(sur)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\well_surveys_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeChunkSetDf(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        var.readonly = False
        try:
            print(var.readonly)
            
            chunk = var.chunk((5,15),(5,10))
            df_to_reset_values = chunk.as_dataframe()
            
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = df.loc[:,'Value'] * 2
            
            #set with df - correct input
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().head())
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
            chunk.set(df_to_reset_values)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_chunk_set_df_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteChunkSetDf(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        var.readonly = False
        try:
            print(var.readonly)
            
            chunk = var.chunk((5,15),(5,10))
            df_to_reset_values = chunk.as_dataframe()
            
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = df.loc[:,'Value'] + 1
            
            #set with df - correct input
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().head())
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
            #Try set non-integer values -should raise ValueError
            df.loc[:,'Value_new'] = df.loc[:,'Value'] + 1.05
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
            chunk.set(df_to_reset_values)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_chunk_set_df_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizoninterpretation3dChunkSetDf(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU/Ardmore')
        var.readonly = False
        try:
            print(var.readonly)
            
            chunk = var.chunk((5,15),(5,10))
            df_to_reset_values = chunk.as_dataframe()
            
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = df.loc[:,'Value'] * 2
            
            #set with df - correct input
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().head())
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
            chunk.set(df_to_reset_values)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizoninterpretation3D_chunk_set_df_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Horizonproperty3dChunkSetDf(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            var = petrellink.horizon_properties['Input/Seismic/Interpretation folder 1/BCU/Ardmore/Autotracker: Confidence']
            var.readonly = False
            print(var.readonly)
            
            chunk = var.chunk((5,15),(5,10))
            df_to_reset_values = chunk.as_dataframe()
            
            df = chunk.as_dataframe()
            df['Value_new'] = df['Value']
            df.loc[:,'Value_new'] = df.loc[:,'Value'] * 2
            
            #set with df - correct input
            try:
                chunk.set(df)
            except Exception as err:
                print(err)
            print(chunk.as_dataframe().head())
            try:
                chunk.set(df, 'Value_new')
            except Exception as err:
                print(err)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
            chunk.set(df_to_reset_values)
            print(var.chunk((5,15),(5,10)).as_dataframe().head())
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\horizonproperty3D_chunk_set_df_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Positionconverters(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        seismic = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        seismic.readonly = False
        surface = petrellink._get_surface('Input/TWT Surface/BCU')
        surface.readonly = False
        grid = petrellink._get_grid('Models/Structural grids/Model_Good')
        grid.readonly = True
        grid_property = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        grid_property.readonly = False
        well = petrellink._get_well('Input/Wells/Well_Good')
        well.readonly = False
        interpretation = petrellink._get_horizon_interpretation_3d('Input/Seismic/Interpretation folder 1/BCU/Ardmore')
        interpretation.readonly = False
        pointset = petrellink._get_pointset('Input/Geometry/Seismic_pointset')
        pointset.readonly = False
        try:
            import cegalprizm.pythontool.experimental as ex
            ex.set_experimental_ok(True)
            import numpy as np
            
            for ob in [seismic, grid]:
                print(ob.petrel_name)
                pos = ob.ijks_to_positions([[1,2,3],[1,2,3],[1,2,3]])
                for v in np.array(pos).transpose().ravel():
                    print("{:.1f}".format(v))
                ijks = ob.positions_to_ijks(pos)
                ijks
                for v in np.array(ijks).transpose().ravel():
                    print("{:.1f}".format(v))
                print()
            
            for ob in [surface,interpretation]:
                print(ob.petrel_name)
                pos = ob.ijks_to_positions([[1,2,3],[1,2,3]])
                for v in np.array(pos).transpose().ravel():
                    print("{:.1f}".format(v))
                ijks = ob.positions_to_ijks(pos)
                ijks
                for v in np.array(ijks).transpose().ravel():
                    print("{:.1f}".format(v))
                print()
                
            ps_df = pointset.as_dataframe()
            ijk = [col[:3] for col in seismic.positions_to_ijks([ps_df[col].values for col in ["x","y", "z"]])]
            positions = seismic.ijks_to_positions(ijk)
            for v in np.array(positions)[:3,:3].transpose().ravel():
                print("{:.1f}".format(v))
                
            import numpy as np
            print(np.sum(ps_df[["x", "y", "z"]].values[:3,:3] - np.array([col[:3] for col in positions]).transpose()))
            
            
            print(np.abs(np.sum(ps_df[["x", "y", "z"]].values[:3,:3] - np.array([col[:3] for col in positions]).transpose())) < 1)
            
            for v in np.array(well.md_to_xytime([5000,5100])).transpose().ravel():
                print("{:.1f}".format(v))
                
            for v in np.array(well.md_to_xydepth([5000,5100])).transpose().ravel():
                print("{:.1f}".format(v))
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\positionconverters_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyChunkSize(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        var.readonly = False
        try:
            c = var.chunk((10, 20), (10, 20), (10, 20))
            assert c.as_array().shape == (11, 11, 11)
            print('ok')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_size_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyChunkSize1(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            c = var.chunk((10, 20), (10, 20), (10, 20))
            assert c.as_array().shape == (11, 11, 11)
            print('ok')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_size_1_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_WellLogExceptions(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            from cegalprizm.pythontool.exceptions import UserErrorException
            
            dt = petrellink.well_logs['Input/Wells/Well_Good/Well logs/DT']
            facies = petrellink.discrete_well_logs['Input/Wells/Well_Good/Well logs/Facies']
            
            facies.readonly = False
            
            dt.readonly = False
            mds = [5700, 5700.1, 5700.2]
            values = [-10.0, 1]
            values_disc = [6.99, 4]
            
            failed = False
            
            try:
                dt.readonly = False
                dt.set_values(mds, values)
            except ValueError as ve:
                if not "mds and values must be the same length" in str(ve):
                    failed |= True
            except:
                failed |= True
            
            try:
                facies.readonly = False
                facies.set_values(mds, values)
            except ValueError as ve:
                if not "mds and values must be the same length" in str(ve):
                    failed |= True
            except:
                failed |= True
            
            mds = dt.as_dataframe()['MD'].to_list()
            values = dt.as_dataframe()['Value'].to_list()
            mds.append(10000)
            values.append(150)
            mds.append(1000)
            values.append(200)
            try:
                dt.readonly = False
                dt.set_values(mds, values) #Here petrellink dies
            except UserErrorException as ve:
                if not "Measured depths are not strictly monotonic" in str(ve):
                    failed |= True
            except:
                failed |= True
            if failed:
                print("Failed")
            else:
                print("All good")
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\well_log_exceptions_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))

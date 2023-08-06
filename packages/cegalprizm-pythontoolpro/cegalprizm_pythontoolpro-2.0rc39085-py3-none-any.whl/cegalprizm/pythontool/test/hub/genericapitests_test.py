# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import io
import os
import sys
from cegalprizm.pythontool.test.hub.petreltestcase import PetreltestUnitCase
from cegalprizm.pythontool import PetrelConnection


class GenericApiTestsTest(PetreltestUnitCase):
    _project: str = fr'{os.environ["home"]}/Documents\PetrelUnitTestFramework\1\PythonToolTestProject\PythonToolTestProject.pet'
    
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




    def test_BridgeAccessors(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        grid1 = petrellink._get_grid('Models/Structural grids/Model_Good')
        grid1.readonly = True
        grid2 = petrellink._get_grid('Models/Structural grids/Model_Crazy')
        grid2.readonly = True
        prop1 = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        prop1.readonly = False
        prop2 = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        prop2.readonly = False
        try:
            print(grid1.petrel_name)
            print(grid2.petrel_name)
            print(prop1.petrel_name)
            print(prop2.petrel_name)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\bridge_accessors_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_BridgeIterOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            output = []
            for (guid, grid) in list(petrellink.grids.items()):
                output.append("*={0}".format(grid.petrel_name))
            for (guid, prop) in list(petrellink.grid_properties.items()):
                output.append("*={0}".format(prop.petrel_name))
            
            # could have iterated in any order, so sort the list alphabetically
            # (the expected output is sorted alphabetically as well)
            output.sort()
            for line in output:
                print(line)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\bridge_iter_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_BridgeInjection(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        grid1 = petrellink._get_grid('Models/Structural grids/Model_Good')
        grid1.readonly = True
        grid2 = petrellink._get_grid('Models/Structural grids/Model_Crazy')
        grid2.readonly = True
        prop1 = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        prop1.readonly = False
        prop2 = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Vp')
        prop2.readonly = False
        seismic1 = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        seismic1.readonly = False
        try:
            # python objects should be injected automatically with the corret name
            print("grid1=" + grid1.petrel_name)
            print("grid2=" + grid2.petrel_name)
            print("prop1=" + prop1.petrel_name)
            print("prop2=" + prop2.petrel_name)
            print("seismic1=" + seismic1.petrel_name)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\bridge_injection_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteCodes(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        Var.readonly = False
        try:
            print(Var.discrete_codes)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_codes_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertydiscreteApiValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        var.readonly = False
        try:
            import math
            
            try:
                is_oop
            except NameError:
                is_oop = False
            
            prop = var
            k = 502
            
            layer = prop.layer(k)
            
            # smoketest, set the layer values to be themselves
            layer.set(layer.as_array())
            
            # set all layer 502 values to be 'new_value'
            layer = prop.layer(k)
            original_values = layer.as_array()
            
            new_value = 2
            
            # set all layer values to be 'new_value'
            rawvalues = layer.as_array()
            using_cpython = "numpy" in str(type(rawvalues))
            values = rawvalues.flat if using_cpython else rawvalues
            new_values = [new_value for v in values]
            layer.set(new_values)
            
            # confirm they are by layer
            allNewValueByLayer = True
            layer2 = prop.layer(k)
            for v in layer2.as_array().flat if using_cpython else layer2.as_array():
                if prop.is_undef_value(v):
                    continue
                if v != new_value:
                    print(v, new_value)
                    allNewValueByLayer = False
            
            # confirm they are by column
            allNewValueByCol = True
            
             # Takes very long time in oop mode, so only test per 9th i and j value
            step = 9 if is_oop else 1
            for i in range(0, prop.grid.extent.i, step):
                for j in range(0, prop.grid.extent.j, step):
                    col = prop.column(i, j)
                    v = col.as_array()[k]
                    if prop.is_undef_value(v):
                        continue
                    if v != new_value:
                        allNewValueByCol = False
            
            print("by layer: {0}, by column: {1}".format(allNewValueByLayer, allNewValueByCol))
            
            # Reset prop
            prop.layer(k).set(original_values)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridpropertydiscrete_api_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributediscreteApiValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        Var.readonly = False
        try:
            oldslicevalues = Var.all().as_array()
            
            oldvalue = Var.all().as_array()[2, 3]
            rawvalues = Var.all().as_array()
            using_cpython = "numpy" in str(type(rawvalues))
            if using_cpython:
                Var.all().set([oldvalue + 1 for v in Var.all().as_array().flat])
            else:
                Var.all().set([oldvalue + 1 for v in Var.all().as_array()])
            newvalue = Var.all().as_array()[2, 3]
            print("%d %d" % (oldvalue, newvalue))
            
            
            Var.all().set(oldslicevalues)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattributediscrete_api_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Oneplusone(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            print(1+1)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\oneplusone_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyApiAcceptsFloats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        Var.readonly = False
        try:
            original_values = Var.layer(500).as_array()
            
            with Var.layer(500).values() as vals:
                vals[10, 10] = 1.23
            print("{0:.2f}".format(Var.layer(500).as_array()[10, 10]))
            
            Var.layer(500).set(original_values)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_api_accepts_floats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyApiEnumerate(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        Var.readonly = False
        try:
            import itertools
            layer = Var.layer(500)
            print("[" + ', '.join(["({0[0]}, {0[1]}, {0[2]}, {0[3]:.2f})".format(t) for t in itertools.islice(layer.enumerate(), 0, 5)]) + "]" )
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_api_enumerate_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyApiSmoketest(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        Var.readonly = False
        try:
            import math
            
            try:
                is_oop
            except NameError:
                is_oop = False
            
            new_value = 0.006
            k = 502
            
            def approx_equal(a, b, tol):
                return abs(a - b) < tol
            
            prop = Var
            
            # set all layer 500 values to be 'new_value'
            layer = prop.layer(k)
            original_values = layer.as_array()
            
            rawvalues = layer.as_array()
            using_cpython = "numpy" in str(type(rawvalues))
            if using_cpython:
                layer.set([new_value for v in rawvalues.flat])
            else:
                layer.set([new_value for v in rawvalues])
            
            # confirm they are by layer
            allNewValueByLayer = True
            layer2 = prop.layer(k) 
            
            layer2_values = layer2.as_array().flat if using_cpython else layer2.as_array()
            
            for v in layer2_values:
                if math.isnan(v):
                    continue
                if not approx_equal(v, new_value, 0.00001):
                    allNewValueByLayer = False
            
            # confirm they are by column
            # This takes a very long time in oop mode, so then just test at each 9th value of i and j
            step = 9 if is_oop else 1
            allNewValueByCol = True
            for i in range(0, prop.grid.extent.i, step):
                for j in range(0, prop.grid.extent.j, step):
                    col = prop.column(i, j)
                    v = col.as_array()[k]
                    if math.isnan(v):
                        continue
                    if not approx_equal(v, new_value, 0.00001):
                        allNewValueByCol = False
            
            print("by layer: {0}, by column: {1}".format(allNewValueByLayer, allNewValueByCol))
            
            # reset layer to original values
            prop.layer(k).set(original_values)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_api_smoketest_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyApiValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        Var.readonly = False
        try:
            import math
            
            def approx_equal(a, b, tol):
                return abs(a - b) < tol
            
            prop = Var
            col = prop.column(2, 3)
            original_values = col.as_array()
            
            new_value = 0.1
            
            with col.values() as vals:
               for k in range(prop.grid.extent.k):
                   vals[k] = new_value
            
            col2 = prop.column(2, 3)
            count_not_nan = 0
            allNewValue = True
            for v in col2.as_array():
               if math.isnan(v):
                   continue
               count_not_nan += 1
               if not approx_equal(v, new_value, 0.001):
                  allNewValue = False
            
            print("{0} {1}".format(count_not_nan, allNewValue))
            
            # Reset prop
            prop.column(2, 3).set(original_values)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_api_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_GridpropertyRetrieveStats(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/VShale')
        var.readonly = False
        try:
            print(var.retrieve_stats()['Max'])
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_retrieve_stats_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dApiAnnotationRoundtrip(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        var.readonly = False
        try:
            try:
                is_oop
            except NameError:
                is_oop = False
            
            errors = 0
            fails = 0
            count = 0
            # This takes very long time in out-of-process mode. Thus only test per 9th i and j value
            step = 9 if is_oop else 1
            for i in range(0, min(10, var.extent.i), step):
                for j in range(0, min(10, var.extent.j), step):
                    for k in range(var.extent.k):
                        count += 1
                        try:
                            ann = var.annotation(i, j, k)
                            idx = var.annotation_indices(ann.inline, ann.xline, ann.sample)
                            if idx.i != i or idx.j != j or idx.k != k:
                                fails += 1
                        except Exception as e:
                            errors += 1
            
            if is_oop:
                count += 25100 - 1004
            
            print("Count %d Fails %d Errors %d" % (count, fails, errors))
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_api_annotation_roundtrip_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_Seismic3dApiGriddingRoundtrip(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_seismic_cube('Input/Seismic/Ardmore/Seismic3D')
        Var.readonly = False
        try:
            try:
                is_oop
            except NameError:
                is_oop = False
            
            errors = 0
            fails = 0
            count = 0
            # This takes very long time in out-of-process mode. Thus only test per 9th i and j value
            step = 9 if is_oop else 1
            for i in range(0, min(10, Var.extent.i), step):
                for j in range(0, min(10, Var.extent.j), step):
                    for k in range(Var.extent.k):
                        count += 1
                        try:
                            pos = Var.position(i, j, k)
                            idx = Var.indices(pos.x, pos.y, pos.z)
                            if idx.i != i or idx.j != j or idx.k != k:
                                fails += 1
                        except Exception as e:
                            errors += 1
            
            if is_oop:
                count += 25100 - 1004
            
            print("Count %d Fails %d Errors %d" % (count, fails, errors))
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\seismic3D_api_gridding_roundtrip_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeApiGriddingRoundtrip(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        Var.readonly = False
        try:
            # roundtrip
            try:
                is_oop
            except NameError:
                is_oop = False
            
            surface = Var.surface
            fails = 0
            errors = 0
            # This takes very long time in out-of-process mode. Thus only test per 9th i and j value
            step = 9 if is_oop else 1
            for i in range(0, surface.extent.i, step):
                for j in range(0, surface.extent.j, step):
                    try:
                        pos = surface.position(i, j)
                    except ValueError:
                        fails += 1
                        continue
                    idx = surface.indices(pos.x, pos.y)
                    if idx.i != i or idx.j != j:
                        errors += 1
            
            print("Fails: %d, Errors: %d" % (fails, errors))
            
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_api_gridding_roundtrip_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeApiEnumerate(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        Var.readonly = False
        try:
            import itertools
            vals = Var.all()
            x = [(t[0:3], '{0:.4f}'.format(t[3])) for t in itertools.islice(vals.enumerate(), 0, 5)]
            print(x)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_api_enumerate_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_SurfaceattributeApiValues(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        Var = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        Var.readonly = False
        try:
            
            import math
            
            def approx_equal(a, b, tol):
                return abs(a - b) < tol
            
            sa = Var
            original_values = sa.all().as_array()
            
            new_value = -0.1
            with sa.all().values() as vals:
                for i in range(sa.surface.extent.i):
                    for j in range(sa.surface.extent.j):
                        vals[i, j] = new_value
            
            count_non_nan = 0
            all_new_value = True
            
            rawvalues =  sa.all().as_array()
            using_cpython = "numpy" in str(type(rawvalues))
            for v in rawvalues.flat if using_cpython else rawvalues:
                if math.isnan(v):
                    continue
                count_non_nan += 1
                if not approx_equal(v, new_value, 0.0001):
                    all_new_value = False
            
            print("{0} {1}".format(count_non_nan, all_new_value))
            
            # Reset values
            sa.all().set(original_values)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\surfaceattribute_api_values_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_UndefValueSmoketest(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        prop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Rho')
        prop.readonly = False
        discreteprop = petrellink._get_grid_property('Models/Structural grids/Model_Good/Properties/Facies', discrete = True)
        discreteprop.readonly = False
        attr = petrellink._get_surface_attribute('Input/TWT Surface/BCU/TWT')
        attr.readonly = False
        surfaceattr = petrellink._get_surface_attribute('Input/TWT Surface/BCU/Facies', discrete = True)
        surfaceattr.readonly = False
        try:
            def dual(v):
                return v.is_undef_value(v.undef_value)
            
            print(str(dual(prop))+str(dual(discreteprop))+str(dual(attr))+str(dual(surfaceattr)))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\undef_value_smoketest_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))




    def test_PetrelconnectionPingOop(self):
        output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = output
        petrellink = PetrelConnection(petrel_ctx = self._ptx, allow_experimental=True)
        is_oop = True
        
        try:
            a = petrellink.ping()
            b = petrellink.ping()
            c = petrellink.ping()
            d = petrellink.ping()
            print(b-a)
            print(c-b)
            print(d-c)
            
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\petrelconnection_ping_oop_expected.txt', 'r') as f:
            expected_output =  f.read()
        output.seek(0)
        actual_output = output.read()
        sys.stdout = sys_out
        self.assertTrue(''.join(expected_output.split()) in ''.join(actual_output.split()))

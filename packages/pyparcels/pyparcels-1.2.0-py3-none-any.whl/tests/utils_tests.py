import json
import os
import unittest
from unittest import TestLoader, TestSuite
from arcgis import GIS
from arcgis.features import FeatureLayer, FeatureLayerCollection, FeatureSet
from pyparcels.features import feature_utils as fu
from pyparcels.parcels import parcels_utils as pu
from pyparcels.versioning import versioning_utils as vu

class TestUtilsPackage(unittest.TestCase):
    """Test the features, parcels and versioning utils in pyapi_helpers package"""

    out_file = None
    vms = None
    gis = None
    version = None
    service_urls = {}
    parcel_fabric_flc = None
    base_server_url = None

    @classmethod
    def setUpClass(cls):
        cls.base_server_url = (
            "https://krennic.esri.com/server/rest/services/HCAD_Subset/"
        )
        cls.gis = GIS(
            "https://krennic.esri.com/portal/", "admin", "esri.agp", verify_cert=False
        )
        endpoints = ["FeatureServer", "ParcelFabricServer",
                     "VersionManagementServer"]
        cls.service_urls = {
            url: cls.base_server_url + url for url in endpoints}
        cls.parcel_fabric_flc = FeatureLayerCollection(
            cls.service_urls["FeatureServer"], cls.gis
        )

        # some existing record guid
        cls.test_guid = "{4DAD729F-03FA-4D57-85B0-8DC120B7CBEA}"

        cls.vms = cls.parcel_fabric_flc.versions
        cls.records_service_url = f"{cls.service_urls['FeatureServer']}/1"
        cls.version = vu.create_version(cls.vms)
        cls.out_file = r"C:\temp\layer_id.json"

    def test_where_in_str(self):
        x = fu.generate_where_in_clause("name", ["a", "b", "c"])
        self.assertEqual(x, "name in ('a','b','c')")

    def test_where_in_int(self):
        x = fu.generate_where_in_clause("name", [1, 2, 3])
        self.assertEqual(x, "name in (1,2,3)")

    def test_get_featureLayer(self):
        fl = fu.get_feature_layer(self.parcel_fabric_flc, "Records")
        self.assertIsInstance(fl, FeatureLayer, "Object is not a FeatureLayer")

    def test_query_fl_no_id(self):
        features = fu.query_service(
            url=self.records_service_url,
            gis=self.gis,
            out_fields=["name", "objectid"],
            version_name="sde.Default",
            where="name = 'SomeNewRecord'",
        )
        self.assertIsNotNone(features, "Empty result")

    def test_query_fl_with_id(self):
        features = fu.query_service(
            url=self.service_urls["FeatureServer"],
            gis=self.gis,
            out_fields=["name", "objectid"],
            version_name=self.version,
            fl_id=1,
            where="name = 'SomeNewRecord'",
            return_geom=True
        )
        print(features)
        self.assertIsNotNone(features, "Empty result")
        self.assertIsInstance(features, FeatureSet,
                              "Object is not a FeatureSet")

    def test_create_parcel_record(self):
        record = pu.create_parcel_record(
            self.parcel_fabric_flc, version_name=self.version, record_name="Test123"
        )
        self.assertTrue(
            record.get("addResults")[0].get(
                "success"), "Record creation failed."
        )

    def test_get_record_by_name(self):
        record = pu.get_record_by_name(
            self.gis,
            self.records_service_url,
            "SomeNewRecord",
            gdb_version=self.version,
        )
        self.assertIsNotNone(record, "Empty result in Records query")
        self.assertEqual(record[0].get(
            "attributes").get("Name"), "SomeNewRecord")

    def test_get_record_by_guid(self):
        record = pu.get_record_by_guid(
            self.gis, self.records_service_url, self.test_guid, gdb_version=self.version
        )
        self.assertIsNotNone(record, "Empty result in Records query")
        self.assertEqual(record[0].get(
            "attributes").get("Name"), "SomeNewRecord")

    def test_get_all_layer_ids_from_flc(self):
        lyr_nt = fu.basic_lyr_info(self.parcel_fabric_flc)
        self.assertIsNotNone(lyr_nt)
        self.assertTrue(len(lyr_nt) == 20,
                        "Incorrect quantity of layer ID results")

    def test_get_single_ids_from_flc(self):
        lyr_nt = fu.basic_lyr_info(self.parcel_fabric_flc, "Tax")
        self.assertIsNotNone(lyr_nt)
        self.assertTrue(lyr_nt[0].lyr_name == "Tax")
        self.assertTrue(len(lyr_nt) == 1,
                        "Incorrect quantity of layer ID results")

    def test_layer_ids_to_json(self):
        try:
            self.assertTrue(fu.feature_layer_ids_to_json(
                self.parcel_fabric_flc, self.out_file))
            with open(self.out_file, "r") as layer_id_file:
                layer_id_json = json.load(layer_id_file)

            first_layer_val = layer_id_json[0]
            first_layer_id = first_layer_val.get("lyr_id")
            first_layer_name = first_layer_val.get("lyr_name")

            self.assertTrue(
                first_layer_id == 0, f"Layer ID json: expected ID: 0, got {first_layer_id}")
            self.assertTrue(
                first_layer_name == "Pro_Parcel_Fabric_1A",
                f"Layer ID json: expected ParcelFabric, got {first_layer_name}")
        finally:
            os.remove(self.out_file)
            json_file_exists = os.path.exists(self.out_file)
            self.assertFalse(json_file_exists,
                             "Did not remove the json layer id file")

    @classmethod
    def tearDownClass(cls):
        vu.clean_up_versions(cls.vms)


if __name__ == "__main__":

    tests = TestLoader().discover("./tests", "test_*.py")
    suite = TestSuite(tests)
    runner = HTMLTestRunner(output=temp_dir)

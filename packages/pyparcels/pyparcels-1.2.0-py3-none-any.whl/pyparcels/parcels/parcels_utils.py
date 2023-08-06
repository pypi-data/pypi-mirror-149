import time
import pandas as pd
from arcgis.features import FeatureLayer, FeatureSet
from pyparcels.features import feature_utils


def query_parcel_features(gis, parcel_list, where, fl_id, url, version):
    """ Get a list of dicts containing the globalid and layer id of desired features
    by querying a FeatureLayer.  Extract the GlobalID value from each feature and
    build up the correct dict format.

    This format is used in all ParcelFabricServer functions that consume parcel polygons.

    ```
    [{"id": "{94A3C67D-46F0-4333-9757-8ED3F8E04600}","layerId": "10"},
      {"id": "{69737BE5-E49C-415E-8CF8-730165D94DD1}","layerId": "10"}]
    ```

    Args:
      gis (arcgis.GIS): GIS of the service
      parcel_list (list): List of features to query
      where (str): WHERE clause to filter results
      fl_id (int): Layer ID of feature layer to query
      url (str): URL of feature server
      version (str): branch version

    Returns:
      list(dict,...)
    """
    if len(parcel_list) > 0 and where is None:
        where = "OBJECTID in ("
        for p in range(len(parcel_list)):
            where += str(parcel_list[p]) + ","
        where = where[:-1] + ")"
    try:
        tax_parcels = feature_utils.query_service(url=url,
                                                  fl_id=fl_id,
                                                  gis=gis,
                                                  where=where,
                                                  out_fields=["globalid"],
                                                  version_name=version).to_dict()
        # Create array of parcels to merge
        parcels_to_merge = []
        if "GlobalID" in tax_parcels["features"][0]["attributes"]:
            glob_id = "GlobalID"
        elif "globalid" in tax_parcels["features"][0]["attributes"]:
            glob_id = "globalid"
        else:
            raise KeyError("Could not find a GlobalID/globalid column")
        for item in tax_parcels["features"]:
            parcels_to_merge.append({
                "id": item["attributes"][glob_id],
                "layerId": fl_id
            })
    except Exception as ex:
        print(ex)
        return None
    return parcels_to_merge


def create_parcel_record(flc, version_name, record_name="NewRecord001"):
    """Create a parcel record in the Records feature layer

    Args:
      flc (arcgis.Features.FeatureLayerCollection): FLC of the parcel fabric 
      version_name: branch version
      record_name:  Name of the new record
                        (Default value = "NewRecord001")

    Returns:
      Dict of edited features
    """
    # Record information with empty geometry.  The geometry is created during Build
    record_dict = {"attributes": {
        "name": record_name
    },
        "geometry": None
    }
    records_fl = feature_utils.get_feature_layer(flc, "records")

    # Call edit_features method on the feature_layer object
    new_record = records_fl.edit_features(
        adds=[record_dict], gdb_version=version_name)
    return new_record


def get_record_by_name(gis, records_url, record_name, gdb_version, out_fields=None):
    """Query the records feature class to get back some specic attributes.

    Args:
      gis (arcgis.GIS): GIS of the service
      records_url (str): URL of the parcel record
      record_name (str): Name of the parcel record
      gdb_version (str): Branch version
      out_fields (list): Fields to return
    Returns:
      arcgis.features.FeatureLayer
    """
    if not out_fields:
        out_fields = ["name", "globalId"]

    where = "name = '{}'".format(record_name)
    records_fl = FeatureLayer(records_url, gis)
    record_attributes = records_fl.query(
        where=where,
        gdb_version=gdb_version,
        out_fields=out_fields
    ).to_dict()
    return record_attributes["features"]


def get_record_by_guid(gis, records_url, guid, gdb_version):
    """Query the records feature class to get back some specic attributes.

    Args:
      gis (arcgis.GIS): GIS of the service
      records_url: URL of records feature layer
      guid: GlobalID value of desired record
      gdb_version: branch version

    Returns:
      str (GUID)
    """
    where = "GLOBALID = '{}'".format(guid)
    records_fl = FeatureLayer(records_url, gis)
    record_attributes = records_fl.query(
        where=where,
        gdb_version=gdb_version,
        out_fields=["NAME", "GLOBALID"],
    ).to_dict()
    return record_attributes["features"]


def external_lines_to_parcels(path_to_lines: str,
                              record_guid: str,
                              cad_line_types: list) -> FeatureSet:
    """ Generate valid parcel lines from a polyline feature class (.shp, fgdb, egdb, CAD)

    Take in a feature class of lines, convert to SeDF for processing, return a FeatureSet

    Args:
      path_to_lines (str): File path to the lines feature class
      record_guid (str): The CreatedByRecord GUID of the new parcel lines
      cad_line_types (list): List of layer types found in some CAD data (optional)

    Returns:
      arcgis.features.FeatureSet
    """
    sdf = pd.DataFrame.spatial.from_featureclass(path_to_lines)
    geometry_type = sdf.SHAPE.geom.geometry_type[0]
    assert geometry_type == "polyline", f"Must be of type polyline: {geometry_type}"

    # Keep only CAD lines with a 'Layer' attribute in the cad_line_types list
    if cad_line_types:
        sdf = sdf.loc[sdf["Layer"].isin(cad_line_types)].copy()

    # Drop all but the SHAPE column
    sdf.drop(sdf.columns.difference(["SHAPE"]), axis=1, inplace=True)
    # Add the CreatedByRecord column
    sdf.loc[:, "CreatedByRecord"] = record_guid
    # Turn sdf into FeatureSet
    lines_fs = FeatureSet.from_dataframe(sdf)

    return lines_fs

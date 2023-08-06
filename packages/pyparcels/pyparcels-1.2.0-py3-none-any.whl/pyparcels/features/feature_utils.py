import json
import os
import pandas as pd
import arcgis.features
from arcgis.features import FeatureLayer, FeatureLayerCollection
from collections import namedtuple

from typing import List


def generate_where_in_clause(field_name, feature_list):
    """

    Args:
      field_name (str): Name of column to query
      feature_list (list): List of values to generate IN clause

    Returns:
        string e.g. `WHERE name IN ('a' ,'b', 'c')`
    """
    # Build up 'IN' clause for searching
    where_str = f"{field_name} in ("
    for p in feature_list:
        if not isinstance(p, str):
            where_str += f"{str(p)},"
        else:
            where_str += f"'{str(p)}',"
    where_str = f"{where_str[:-1]})"
    return where_str


def query_service(url, gis,  out_fields, version_name, fl_id=None, where="1=1", return_geom=False):
    """Returns a FeatureSet containing the features matching the query

    Args:
      url (str): URL of FeatureServer service to query
      gis (GIS): GIS of feature service 
      out_fields (list): list of fields t return
      version_name (str): branch version
      fl_id (int): (optional) LayerId of service
      where (str): (optional) WHERE clause to filter query

    Returns:
        arcgis.features.FeatureSet of features matching the query
    """
    if not fl_id:
        fl = arcgis.features.FeatureLayer(f"{url}", gis)
    else:
        fl = arcgis.features.FeatureLayer(f"{url}/{fl_id}", gis)
    return fl.query(
        where=where,
        out_fields=out_fields,
        return_geometry=return_geom,
        gdb_version=version_name,
    )


def get_feature_layer(flc: FeatureLayerCollection, lyr_name: str) -> FeatureLayer:
    """Get a FeatureLayer out of a FeatureLayerCollection by its name property

    Args:
      flc (arcgis.features.FeatureLayerCollection): The FeatureLayerCollection 
      containing the desired FeatureLayer

      lyr_name (str): The name

    Returns:
      arcgis.features.FeatureLayer
    """
    fl_url = [n for n in flc.layers
              if n.properties.name.lower() == lyr_name.lower()]
    fl = FeatureLayer(fl_url[0].url)
    return fl


def basic_lyr_info(feature_layer_collection: FeatureLayerCollection, layer_name: str = None) -> List[namedtuple]:
    """Get a list of namedtuples containing
        - layer name
        - layer collection order number as they appear in the collection
        - the layer's layer ID
        - the url to the feature layer

        Or:
        A single named tuple described above for a specific layer

        Args:
          feature_layer_collection (arcgis.features.FeatureLayerCollection): The FeatureLayerCollection
          containing the desired FeatureLayer

          layer_name (str): (optional) The name of a layer in the collection

        Returns:
          List[namedtuple]
    """
    layers = feature_layer_collection.layers
    LayerProps = namedtuple("LayerProp", ["lyr_name", "lyr_list_order", "lyr_id", "lyr_url"])
    layer_props = []
    for i, lyr in enumerate(layers):
        lp = LayerProps(lyr.properties.name, i, lyr.properties.id, lyr.url)
        layer_props.append(lp)

    if layer_name:
        return [lyr for lyr in layer_props if lyr.lyr_name == layer_name]
    return layer_props


def feature_layer_ids_to_json(feature_layer_collection: FeatureLayerCollection, file_name: str) -> bool:
    layer_id_dict = basic_lyr_info(feature_layer_collection)
    layer_id_df = pd.DataFrame(data=layer_id_dict)
    try:
        layer_id_df.to_json(file_name, orient="records")
        if os.path.exists(file_name):
            return True
    except FileNotFoundError as fex:
        print(f"Something went wrong creating the file: {fex}")
        return False
    except Exception as ex:
        print(f"Something went wrong creating the file: {ex}")
        return False
    return False


def load_feature_json(file):
    """Read in json files from the test suite's feature_data dir

    Args:
      file (str): The name of the file to be read

    Returns:
      Dict of features from a file
    """
    cwd = os.getcwd()

    filepath = os.path.join(cwd, "tests", "feature_data", file)
    if not os.path.exists(filepath):
        filepath = os.path.join(cwd, "feature_data", file)
    try:
        with open(filepath, "r") as features:
            parcel_features = json.load(features)
    except Exception as ex:
        print(str(ex))

    return parcel_features

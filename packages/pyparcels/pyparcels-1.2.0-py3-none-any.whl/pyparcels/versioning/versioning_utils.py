import time


def clean_up_versions(vms, filter=None):
    """Delete all versions that match a search criteria.

    Args:
      vms (arcgis.features._version.VersionManager): VersionManager object 
      filter (str): String to filter versions by name

    Returns:
      void
    """
    try:
        for version in vms.all:
          if ".default" not in version.properties.versionName.lower():
            if filter:
              if filter in version.properties.versionName.lower():
                  version.delete()
                  print(f"deleted version: {version.properties.versionName}")
            else:
                version.delete()
                print(f"deleted version: {version.properties.versionName}")

    except Exception as ex:
        print("Error deleting version(s):", str(ex))


def get_version(vms, owner_name, version_name):
    """Get an existing branch version by name

        Args:
          vms (arcgis.features._version.VersionManager): VersionManager object
          owner_name (str): The owner of the branch version to search for
          version_name (str): The name of the branch version to search for
        Returns:
          The fully qualified version name (`owner.version_name`) string
        """

    _version = [
        x for x in vms.all
        if x.properties.versionName.lower() == f"{owner_name}.{version_name}".lower()
    ]
    fq_version_name = _version[0].properties.versionName
    return fq_version_name


def create_version(vms, version_name=None):
    """Create a new branch version

    Args:
      vms (arcgis.features._version.VersionManager): VersionManager object 
      version_name (str): (Optional) name of the version to be created
    Returns:
      The fully qualified version name (`owner.version_name`) string
    """
    try:
        timestamp = int(time.time())
        if not version_name:
            # VersionManagementServer - Create a new version
            version_name = "api-{}".format(timestamp)
        else:
            version_name = f"{version_name}_{timestamp}"
        return vms.create(version_name)["versionInfo"]["versionName"]
    except Exception as ex:
        print(ex)
        return None

def reconcile_version(vms, fq_version_name, future=False):
  try:
    with vms.get(fq_version_name, "read") as version:
        version.mode = "edit"
        result = version.reconcile(
            end_with_conflict=True,
            conflict_detection="byAttribute",
            with_post=False,
            future=future,
        )
    return result

  except Exception as ex:
    print(ex)
    return None

def purge_version_locks(vms, version=None):
    """Remove shared and exclusive locks from all branch versions

    Args:
      vms (arcgis.features._version.VersionManager): VersionManager object 
      version (arcgis.features._version.Version): Version
    Returns:
    void
    """
    if version:
        vms.purge(version.properties.versionName)
    else:
        for version in vms.all:
            vms.purge(version.properties.versionName)

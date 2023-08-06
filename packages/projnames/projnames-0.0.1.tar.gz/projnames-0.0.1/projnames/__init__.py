import pkg_resources
import json
import sys
import re

# epsgnames.json has been extracted from pyproj using the following very slow code:
#
# {pyproj.crs.CRS(code).name: code for code in pyproj.get_codes("epsg", "CRS")}

projections = json.load(pkg_resources.resource_stream("projnames", "epsgnames.json"))
by_epsg = {value: key for key, value in projections.items()}

def search(name):
    match = re.match(r".*\(?epsg:([0-9]*)\)?.*", name)
    if match:
        return int(match.groups()[0])
    else:
        name = name.lower()
        name = name.replace("wgs84", "wgs 84")
        ptn = re.compile(".*" + name.replace(" ", ".*") + ".*")
        matches = [(name, value)
                   for name, value in projections.items()
                   if ptn.match(name.lower())]
        if matches:
            # NOTE: Sometimes the projection given does not
            # specify N or S for UTM zones... We are forced to
            # choose one here quite arbitrarily... This is why we
            # should use EPSG codes kids!
            return matches[0][1]
    return None

def cmd():
    if not sys.argv[1:]:
        print("""Usages:
  $ projnames 3857
  WGS 84 / Pseudo-Mercator
  $ projnames "pseudo"
  3857
""")
        
    try:
        code = int(sys.argv[1])
    except:
        print(search(sys.argv[1]))
    else:
        print(by_epsg[code])

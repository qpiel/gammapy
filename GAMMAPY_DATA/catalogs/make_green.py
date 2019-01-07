"""
Make a FITS version of Green's SNR catalog.

What this script does:
- Download the catalog from Vizier
- Add some convenient extra columns
"""
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.units import Quantity


def compute_mean_diameter(d_major, d_minor):
    """Compute geometric mean diameter (preserves area)"""
    diameter = np.sqrt(d_major * d_minor)
    # If no `d_minor` is given, use `d_major` as mean radius
    with np.errstate(invalid='ignore'):
        diameter = np.where(d_minor > 0, diameter, d_major)

    return diameter


def green_catalog_download():
    # This allows easy access to Vizier tables:
    # https://astroquery.readthedocs.org/en/latest/vizier/vizier.html
    from astroquery.vizier import Vizier
    Vizier.ROW_LIMIT = -1
    # This is the 2014-05 version of Green's catalog
    # http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=VII/272
    results = Vizier.get_catalogs(['VII/272'])
    table = results[0]
    return table


def green_catalog_cleanup(table):
    # The table has float columns in deg `_RAJ2000`, `_DEJ2000`
    # as well as string columns in hms `RAJ2000` and in dms `DEJ2000`
    # Here we convert to the more common form where `RAJ2000` and
    # `DEJ2000` are float columns and remove the string columns
    # table['RAJ2000'] = table['_RAJ2000']
    # table['DEJ2000'] = table['_DEJ2000']
    table.remove_columns(['RAJ2000', 'DEJ2000'])
    table.rename_column('_RAJ2000', 'RAJ2000')
    table.rename_column('_DEJ2000', 'DEJ2000')

    # Add Galactic coordinates
    skycoord = SkyCoord(table['RAJ2000'], table['DEJ2000'], unit='deg').galactic
    table['GLON'], table['GLAT'] = skycoord.l, skycoord.b

    # The extension unit is `arcm`, which is a bit cryptic ... change to `arcmin`:
    table['Dmaj'].unit = 'arcmin'
    table['Dmin'].unit = 'arcmin'

    mean_diameter = compute_mean_diameter(table['Dmaj'], table['Dmin'])
    table['Dmean'] = Quantity(mean_diameter, 'arcmin')

    table.rename_column('SNR', 'Source_Name')

    # Finally, sort and group table columns in a sensible way
    cols = ['Source_Name', 'RAJ2000', 'DEJ2000', 'GLON', 'GLAT',
            'Dmean', 'Dmaj', 'Dmin', 'u_Dmin',
            'l_S_1GHz_', 'S_1GHz_', 'u_S_1GHz_',
            'alpha', 'u_alpha',
            'type', 'Names']
    # Make sure we don't accidentally remove columns
    assert set(cols) == set(table.colnames)
    table = table[cols]

    return table


def main():
    table = green_catalog_download()
    table = green_catalog_cleanup(table)
    filename = 'Green_2014-05.fits.gz'
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


if __name__ == '__main__':
    main()
import cdsapi
c = cdsapi.Client()

var = 'u' #'temperature', 'z', 'v', 'u'

c.retrieve('reanalysis-era5-pressure-levels', {
    "variable": var,
    #"pressure_level": ["200", "300", "500", "700" ,"850"],
    "pressure_level": ['10', '20', '30',
                       '50', '70', '100',
                       '125', '150', '175',
                       '200', '225', '250',
                       '300', '350', '400',
                       '450', '500', '550',
                       '600', '650', '700',
                       '750', '775', '800',
                       '825', '850', '875',
                       '900', '925', '950',
                       '975', '1000'],
    "product_type": "reanalysis",
    "date": "2015-08-01/2016-09-10",
    "time": [
            '00:00', '06:00', '12:00','18:00'
        ],
    'area': [
            24, -180, -24,
            180,
        ],
    "grid": "1/1",
    "format": "netcdf"
}, 'ecmwf/era5_%s_2015-2016.nc' % var)#'test.nc' % var)
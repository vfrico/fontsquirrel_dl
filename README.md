fontsquirrel_dl
=========================

This is a Python 3.x library which provides an easy access to [FontSquirrel API](http://www.fontsquirrel.com/blog/2010/12/the-font-squirrel-api).

Some cache is stored to get data faster.

##Documentation
This library allows to:

1. Download all fonts freely available on Font Squirrel
1. Download a family (using url_name)
1. Return data from Font Squirrel on a similar way on Google Fonts 

### #1: Download all familes on FontSquirrel
Font Squirrel's API allows access to free and open fonts. All fonts which needs to go to another site **are not** available here. The function is contained on FontSquirrel class. 
It takes one argument: the folder where you want to download and extract the fonts.

    import FontSquirrel
    FontSquirrel.get_all_families("Fonts/")

### #2: Download one family from FontSquirrel
Once you know the url_name for the font you want, you can use the get_family() function. Takes one argument: the folder where you have to download.

    import FontSquirrel
    FontSquirrel.get_all_families("Fonts/")
    
### #3: Get Json data like Google Font's API
You can get the data from FontSquirrel on a similar way that Google provides with his Web Fonts API. It does not have the same atributes: some of them are not available.
    
    { 'kind': 'fontsquirrel',
      'family': #family_name
      'family_url': #family_urlname
      'category': #Classification
      "variants" : [ "regular" .. "thin" ]
      "files" : {
         "regular" : "Family-variant.otf",
         "thin" : "Family-variant2.otf",
      }
        
The files must be looked into the zip.
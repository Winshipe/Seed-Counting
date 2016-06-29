@REM echo %time%
set "b=%CD%"
python2 image_converter.py .\images
@REM seed_images\template_testing
@chdir C:\Program Files\ImageJ\
@REM echo %time%
FOR %%a in (%b%\images\8bit_*) DO (

@REM echo %time%

java -cp ij.jar ij.ImageJ -macro %b%\3_small_plate_partial_macro.ijm %%a

@REM echo %time%

)
@REM echo %time%
@PAUSE

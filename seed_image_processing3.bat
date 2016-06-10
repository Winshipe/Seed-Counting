@REM chdir C:\Users\Eamon\Documents\ShiuLab\seed_density_test
@REM echo %time%
set "b=%CD%"
python2 image_converter.py .\seed_density_test
@REM seed_images\template_testing
@chdir C:\ImageJ\
@REM echo %time%
FOR %%a in (%b%\images\8bit_*) DO (

@REM echo %time%

java -cp ij.jar ij.ImageJ -macro %b%\5_small_plate_partial_macro.ijm %%a
java -cp ij.jar ij.ImageJ -macro %b%\6_small_plate_partial_macro.ijm %%a

@REM echo %time%

)
@REM python %b%\predict_seeds.py 
@REM echo %time%
@PAUSE

@REM CHDIR C:\Users\Eamon\fiji-win64\Fiji.app\
@REM python C:\Users\Eamon\Documents\ShiuLab\add_extra_slashes.py %%a >C:\Users\Eamon\temp.txt
@REM ImageJ-win64.exe --console -macro C:\Users\Eamon\Documents\ShiuLab\3_small_plate_partial_macro.ijm temp.txt4
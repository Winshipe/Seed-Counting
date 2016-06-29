file_name = getArgument();
if (endsWith(file_name,"xls") || endsWith(file_name,"txt")){
exit();
}
//Current template
ovals = newArray(432,600,2736,2712,3648,552,2640,2808,6984,528,2640,2808,504,3984,2736,2808,3720,3984,2736,2808,6864,3912,2736,2808,456,7440,2736,2808,3744,7368,2736,2808,6912,7344,2736,2808,576,10776,2736,2808,3792,10776,2736,2808,6960,10728,2736,2808);


function count_seeds(file_name,ovals) {
        //print(file_path);
        //print(file_name);
        open( file_name);/*               v      1500 DPI       v v 2000 DPI             v  v  500 DPI            v v      1000 DPI        v*/
        makeLine(2256, 480, 2256, 3336);//1848, 648, 1872, 3576);//2496, 352, 2496, 4000);//(480, 1116, 1356, 312);//1080, 2400, 2448, 408);//Scale
        run("Set Scale...", "known=60 unit=unit");
        setAutoThreshold("Default");
        setThreshold(50, 140);
        //waitForUser("Say CHEESE!");
        //print(toString(lastIndexOf(file_name,'\\')));
        //print(toString(indexOf(file_name,'.bmp')));
        path = substring(file_name,0,lastIndexOf(file_name,"\\"));
        new_path = path+'\\counts\\';
        new_base_name = substring(file_name,(lastIndexOf(file_name,'\\')+1),indexOf(file_name,'.bmp'));
        File.makeDirectory(new_path);
        savename = new_path+new_base_name+"_results_";
        for(i=0;i<ovals.length;i+=4){
            makeOval(ovals[i+0],ovals[i+1],ovals[i+2],ovals[i+3]);
            //waitForUser("Say CHEESE!");/**/ 
			results_name = savename+toString(i/4,0);
			//print(i/4);
			/*if (i==0){
			    run("Analyze Particles...", "size=0.06-0.18 circularity=0.25-1.00 clear display");
				saveAs("Results", results_name+'.xls');
			}
			else{
				run("Analyze Particles...", "size=0.06-infinity circularity=0.25-1.00 clear display");
				IJ.renameResults("Results");
				String.copyResults();
				//waitForUser("");
				table = String.paste();
				File.saveString(table,results_name+'.txt');*/
			run("Analyze Particles...","size=0.06-infinity circularity=0.25-1.00 display clear summarize add");
			//}
	       /* if(i%8==0)
			   {waitForUser("Say CHEESE!");}         
            */
        };
        saveAs("Results",savename+".xls");
        //setBatchMode(false);
        run("Close");
        close("*");
        exit();
}
count_seeds(file_name,ovals);


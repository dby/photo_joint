# photo_joint

- 拼接照片的结果为：  
 ![image](test1.jpg)


- 程序说明  
 - lib: PIL, numpy, numexpr, 
 - photo source: 照片默认放在当前目录的photos文件夹中  
 - 前面一张照片: 在createNevImage中定义的，可以自行修改  
 - alpha: 修改前一张照片的透明度，默认为0.5，可以自行修改测试
 - photos: 运行代码后，会在代码目录下生成几张照片，分别是运行中间接生成的。最终生成的照片为final.jpg  
 - test1.jpg: 一个示例照片，，程序中又添加了向照片中添加文字，旋转等  
 - 详见程序说明。  



- note: transfer函数直接重置照片的大小，所以照片会有所变形。由于对照片按比例进行裁剪可能会使照片不再协调。

- thanks: @世界上没有真理





# ASCII Art Converter

#### Консольное приложение преобразующее изображение в ASCII Art c заданной шириной и высотой и возможностью получения цветного результата  

#### Поддерживаемые форматы изображения: .PNG, .JPEG, .PPM, .GIF, .TIFF, .BMP  

#### Требования
- Python (рекомендуется версия не ниже 3.8.9)
- Pillow (рекомендуется версия 10.3.0)

#### Запуск
Справка по приложению: ./ascii_art.py --help  
Пример запуска: ./ascii_art.py  

Есть возможность передачи параметров сразу через командную строку  
Пример (без автоподбора высоты): ./ascii_art.py --width=200 --height=200 --mode=1 --path=/some_path  
Пример (с автоподбором высоты): ./ascii_art.py --width=200 --mode=1 --path=/some_path  

__Доступные параметры:__   
--width _Ширина ASCII Art в символах_  
--height _Высота ASCII Art в символах_  
--mode _Режим работы (1 - обычный, 2 - инверсия, 3 - цветной)_    
--path _Путь до изображения_   
 

Можно передавать параметры частично (например только --path), тогда программа попросит ввести оставшиеся данные в консольном приложении.  
Но если передать --width и не передавать --height, программа подберет высоту автоматически.  
Если не передавать --width, программа попросит ввести размеры в приложении, вне зависимости от наличия флага --height.

#### Подробности реализации
Программа переводит изображение в черно-белое, далее путем сопоставления оттенков серого и ASCII символов получается результат.  
Реализован простой просмотрщик с помощью встроенной библиотеки TKinter.  
Программа поддерживает 3 режима работы: в первом самому яркому пикселю сопоставляется наименее "плотный" cимвол, во втором и третьем - наоборот.  
1 и 2 режимы работы сохраняют результат в файл .txt, 3 режим - в .png  
Обработка изображения в цветном режиме может занимать некоторое время, поэтому реализован прогресс-бар



# ***************** Catalog starts here *******************

catalog = {}
index = []

#----------------------------------------------------------------------
fileopen = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAAt5J"
    "REFUOI3VlDtoFEEYx3/7yMs7TeI7isRIokErbbSzUQSLNApWIoiVoCBiaWdjEMGUgtY2omLj"
    "A/EBKig+kCgiicnJmXi5XHK3yd7e7s7sWMxcTi8JQbt8MMzMzuxv//Of71tYbmH9y+YjR/ve"
    "dXX1bhZxJBdadxsbnSv9/c+BYxp84H7frq6V9xYDfn799iSDF25fGxgonT1zBgGoBRS6QE/P"
    "lszQUHarC4Bt3xu8vn9B6I3HeU59mr5Jz/m1fijwJJSKQFIvFzraIRIqNFMd3z3dT0zX9kYS"
    "Thxcx/r0PvrO0e/NjDL8C+IAHAeUUti2hVIQC6gAidDv2lVIKdCtHIFIQCp9vDcZ6O1eT/Hh"
    "IaIEclOQzcPYJIwXLH7m4WdeC5ryIFZzB9Ax6ev+yfsxHoxuqjunDbSwZ8NhXmYgqMy/9f1b"
    "oX0FIOvAbzPgFca4fGsCdacebPZ8gM7tUAn0t6KKIgwkqVaXgbsZf3dvZ8oyLsyBB8chMP6+"
    "yoBjQZSANC1OoFgAiuCXwXKhmJdMjYds3uGyYmNnalULSFUHjgTE5hilCrg2hFL7LaS+yFha"
    "JNQSIowUs35CrMBWkHZAKe3SHHimAmFFj8uxBscGHBtwk9sMCbQ0Ag6kWqA1bZFqgnSzyWW7"
    "oekv8GwIUaTHXgBY2gJhbBACQmcL758OMZkdAhcmf4RMjARs29vGiy9w9fjpQi43+nSe4jis"
    "WYFl0q4KNqrtNd2sbutGNYBvl3GmS7Tu7CAogZcbuQg8mqdYGsWFMlhGsVRGtdDg6hypcz6U"
    "4MfzS3wOXBa1qvEi7VfyJ1jWCkdIvV693FCCchYBB7MS5Uuo5PlR0M+SBBKle2HmVXvsJvB8"
    "h3LokC+CmM4l/CFcg0tfT3rDm24C0LyOu88ClowGG3IBZENGXmbh46XbwCwQQa0yVwG9wA4g"
    "vTR1wZgBvgFfAa8Ktg2wFWj8T3AElNCq63+qyyB+AyLLeyB9WsvgAAAAAElFTkSuQmCC")
index.append('fileopen')
catalog['fileopen'] = fileopen
getfileopenData = fileopen.GetData
getfileopenImage = fileopen.GetImage
getfileopenBitmap = fileopen.GetBitmap

#----------------------------------------------------------------------
filesaveas = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAABCFJ"
    "REFUOI3V01tsFFUYwPH/ucxst11aKYUimoLcKkQpcmsgxAgJJGLSPqA+ocQbatREfTBeMJD4"
    "UDHGBH3QxAeDRiXxVpQ0Ri6aSABjLNWSoqWJLWsvsF3ahb3M7syZ48O0i4QSX3zxJCdzkjnz"
    "yzffRfEfrC2zN8zdsVn0bG6sf3GmnT/YnR7q1lde70pA/FHQNYD/75wB4kDRrlj76Y4n2xrn"
    "uOnf6fh4+EPHWTmjDMfqbj68atu65iX1UB8LMCisDQlDCK0FJrYFa0OUkmRzDqKnjWdfXkDV"
    "ogch/jqt27vV0FhVWxm+pblx1b07lrLKGWf9wgSgsUAABCZilQAlYfKjzoNv0tCaZcbtD8PI"
    "J1DxF7m62VzyYyNlWLvSelnIaYMpGYpoTABBCMaAb8BacB1wYvDLV+8yZ9YR6pY9A+l20Mcw"
    "xNj3hjx/qtNsuJJjazEhSCVRGhwLwgIChIieJgQRg98OtzO96jNuvespyBwFeQRimnd2N4T7"
    "Ppr1QFduf1KWYQWhBSUjSUlQCrQCLcBREE/AHz9+j1t8j+VbnoD8ryC/ASeg/cBy9v70nOnK"
    "resDKMNKgLGglAQhkCJClQSlIV4FfSdPEqbbWN26DREkIfgCG2Q5uL+BfRf24CxoFJCOXwOH"
    "IQgpo/8G5GSkLvR39ZAbbGNN631IfxxG3ydMpej8sobT3k7CuYuImUvlBJRhKSPY1eJKa2ER"
    "ApJn/2S4ZzfNLXfjFg307YXBc5w+lICGt1m6tpnAm6jFZDNMHoSIKC+QpMeLlIIiQisyqQwD"
    "R3eyrqUJtxCDntcgn6S3u4KexKusWLKawkAWa29ATgUrGaXj6ECcI/0h2ZKlKBSVZ37g+Y1N"
    "JIjB8V1wOUlfr2bPpbcw6x/iuxM+eS8BE0WeEg4tXCzA6ECRWhVQ8Aos5iKzF7XA8afhXJKR"
    "C9B++SWS0x/jbEeBWQtjuDWSeGVkXANLEcFZD5bUFti9VTKSvEBqsBJZ5ZCqvYf+Y/1crG3h"
    "8RdeYVlnikf2aPQ8ByUkxjB1KvTEAJgQjA3JlTRfd5ygv+8wo0NnKHhVVN/5AU13LCcmi5QC"
    "nxvnVOC4At+PpOtGbGwUtR9YMmPjdP98it4Bl40bm7ht/UoqEtPwvTzjYwGBCairFZS0IGdA"
    "2uvBE+0WhOD7IcVChl5vO5n6+SxeYwhKPuOpURAQaLAmoK5Ocl4L/BI4BpypYO1K4YfgB5Av"
    "lEiNlti8aRql4jCDAyCkwtrorqMsnieZWatI5aFQBB2HKi1hYjbKsJcphBWVqIpqcIuKeKXL"
    "1k2a0Chy3j+qAjgqpNqTzKuJkRwG7UNlNQS5AqBzV8Gdh858nqhL3O9UV4rU5TTfjpfQjhuN"
    "+dUuSliGxgxpkScowk0lie0r2c6OrkMQJPlfrr8BIHbBybUn56IAAAAASUVORK5CYII=")
index.append('filesaveas')
catalog['filesaveas'] = filesaveas
getfilesaveasData = filesaveas.GetData
getfilesaveasImage = filesaveas.GetImage
getfilesaveasBitmap = filesaveas.GetBitmap

#----------------------------------------------------------------------
kig_doc = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAA/ZJ"
    "REFUOI2dlc2PFUUUxX9VXf1ev/loYPhwYMZEMBlAEjCAMSYuXPhBnJXBDTFoIn8Bf4Brt4a4"
    "IFFJZMeYGBPjRllMwkZxRENAg9FxUGRAkXFmXvd7r7vqXhf9XvPGqAtvOqmuvtWnbp1zbrcB"
    "OH78+Ouzs7NvpmmaeO89fwtrITJggACEYKG6ADDGYK21WZaZc+fOnZ+fn38DgLNnzy7of0QW"
    "VG+uqy6tqWblxpyIqIjU8zNnzrSBlxxAs9lsAoQQUAVnBUFZ+NVw+bYlL2EkVlAlLw2NSHhy"
    "0nN4R0EpSuFBVZiYmCBJkgaw1fUBA4ACkVFyD+9/HbHag2f3BGY2e1pOUIH1Ehb/tHz2U4Mr"
    "dxyv7M+JrVD0Ebz3AogFEJGKSwSvyjsLEU2nnH6q4OhOTyNSuh56AkmkHNlRcPpIm4YV3r3a"
    "QhEMIKJDWICq9kVSPv3eEILy2qGSSJR2R/ECaEVFEGW1B0GUVw9kqMLFpYQkCojqA6xh4LWO"
    "8s1tw+yMJ1Kh5xVQVATVqhoRAVV6QfFBOba7w9U7DVZ7FmeEPqsVcAhV+T+vGJxV9mwO9Lzp"
    "F1ltOhjre1V6AXaNeWIr/HjfYqwiUq1z/aUA/JZBMwJnlI6AojXIYBTd+CyyStMK93ILSI3l"
    "AHyf8IYRQmnql1UUBdS5ahw81z49AAg+GJwRwNTiVRX3J1OpsN51rHWhFSs+VP4kz6EoKgEr"
    "LjCqWISOh3Z3hOlxD6E6UQ082GXXeCBxyhc3I47t83RDBCtrROfPo60WGkU1BYJhMzkL5V6S"
    "xyaZTku6ZXWSIY6rcFZ5cV/Be58nzGwreWSHsnIro3QOc+IEagxSHYO0GbixFvPxJwUn1y+h"
    "7nHCkNh20MoA7Z5yYLLkhX093ppvcfmmYyQORE1DPNokHm0yMh4ztinmy99T3r42xTOtRR7t"
    "LtKlUYk7XPGwpda78PxMl/GG58MrI1wsHmK/Pcj0skWN4e5qg2vLTe7nhpcPtzkw3mFlMSJR"
    "qYX9R+BBoxx9uGD/Ts9X3xYs3J7guxstFBiNPYenOhyc7DCSJtz7wVAIJEM+/1dgBdo9iJzh"
    "ia332G0vsu3p3aiBWEtUlawHeQEeKNCahgGtg68bA3cYY+oGCKJkhWHFtNjqGmANndJVlmoI"
    "LkkQ5yh0Y9vXwMYYM1zxIIkqxDF/LC/j5z4AY/sAVd5EEetLS4xNT1f8AtbaB8BZllmALVu2"
    "bOwuYCxJSE6dwmcZakzd1gM/66FDtLZvp5EkbEpTiqKwgHUAc3NzH01NTe1N0zQqikIGAtSe"
    "jOMHqvQ3rMMY9Pp1DJDnubtw4cIt4K7pp0eB54Bpqv/l/40I+AW49BeW/MxrXZ+3vQAAAABJ"
    "RU5ErkJggg==")
index.append('kig_doc')
catalog['kig_doc'] = kig_doc
getkig_docData = kig_doc.GetData
getkig_docImage = kig_doc.GetImage
getkig_docBitmap = kig_doc.GetBitmap

#----------------------------------------------------------------------
thumbnail = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAA5xJ"
    "REFUOI19lc1rXFUUwH/nvvdmJpNJR9M4IwNqi4K4EezGulL/B3FTujYboSii+0CgXRRr3Qp2"
    "oRsxVuiqgghKSgU/qI0kdVqbdBISm6aZzLx5877ucfFmJjOZpAcO9+Pd+zsf99z7hJ7Mzs6u"
    "VCqVE6pqrbWAoqpYm7V9tdYOWlCsVSMiqqrSaDQ2FhYWTjIs8/Pz1vd9TZJIkzjTOIo0jsIh"
    "7WoYdjXsdjUI9rXdDrTd7ujc3Jzt89x+J5fztFAoys2bv/HfRgPHcRmsQhFAFUR6U0I2Z1Om"
    "nnqG1984TT6f1zGwKhhRPv3iGjfaL1GtlXBdxXFBgSSGKIDQh05TaTeh/VgItwLefPUa1797"
    "DdUBdwiMgk2ZmK7y4ul3eeF5j6IHOQcs0I2h5UPzMTS3YGcTZB1CQvC2MZKiKuNgNNN8wVI5"
    "1qVW9Cg64JkMHDqwJ+ApSJxiw4Q0sOxOBRjHIlliDgH38pZzhcoUVErgGjAm+2RTKLhZjuPU"
    "IQyUoA25KYN4wkEZBSt4RihOQDEPx3PKyYmI3Uh4EOVwHEgFIgOtpqEwqeSLguOazKsjwQKO"
    "K+Qd5fgxeGtGKKcR3Vhw2kLdQPDvKvXFG0ydOkuuaPCKJRzrZGc0JGYkxQqe61IqT7Jzf5nm"
    "xl3Em6BULrHy41W+/2yO1vot1q5fQG0Hx0mwu78iaQsR93CwAGIMUWePtaXf+ebi+1y58iWO"
    "57L8zwqfn/+AR3cXKU7PkPgbLJ5/h9bG3+jtj8C/gzi5I8pNAWPobv7JVxc/IYki1u9t8eyp"
    "tylVJtjbbRDnyvz87dc82txBzU+07v2Cv3UbfbmKmCflGIhiS8ePyBUcHq7+xYWP36Ny4hXC"
    "OEfYWOLOH0tYIF+aRG9dJfabGILejTyq3IDmXkKUQNROaQMPH9e5v1w/uIywvU1Y/wGAJEn3"
    "oz4KPDMzTbVaxXHczAORQSGNvBW9G5WmSrVaHTM8AItAtxtz7tyHnDlzFtf1erDRMsqGOjCS"
    "JAnl8tP4fjRk9IDH3W5MpVKjVnsOa3UAVt03MDzuw8MwIgieABYROp0Aa9NDQePg/hzk8+WR"
    "yMzwQNWyf7LSC3v8HRhyZXBgB1M28NgYwRiDiEFEBxHsb+i/XqOvmKogor19Zhycpql4nmFy"
    "Mt9LxWDrSBkNp6TvsQgUix5pmsoYeHV17cHly5dqqmpVbW9j/weaGbBWSdN00O+3Ioq1mHq9"
    "vt3n/Q8mySdOswRyTwAAAABJRU5ErkJggg==")
index.append('thumbnail')
catalog['thumbnail'] = thumbnail
getthumbnailData = thumbnail.GetData
getthumbnailImage = thumbnail.GetImage
getthumbnailBitmap = thumbnail.GetBitmap

#----------------------------------------------------------------------
tool_restart = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAABDlJ"
    "REFUOI2VlHtM1WUYxz+/8zv3w+1wEM+RwEyxCRVLHauh0yhJxFpK5rXwmEaexMQtWy1za8q8"
    "X2alzpB0llOaTisCNQvx7mSasCZyEUVQ0SMHlMvh/H5vf0gIccjx3d6/3u/zeZ/3ed7nhb7K"
    "aVzKdLKeZNP0lSupkuXlYYmfMSNgN1OCQvucWK9KZfmfV4rEoXP5ImhGxGXeDIjxm4Df4AyC"
    "aGSa1mh8PdQY/pSMLKPIAgVoFRE5n3zjiBqm0FARyswVrltVtZUpFHiK/x/8PmP7B9u3LkrM"
    "fDY+Ng5jgAaB2mmVkNAbZfLULQwxxzL4ZjJTl7pqquvqEjhad90/eC6jR0bFF3zt3GAqDzrN"
    "+aY/aPTdRyA6rAIAVVWxSEE0qQ2Md0zGVzSU2VkfrKDw3hf/orSd0DRCHMEDstfPWmXa3bKe"
    "ktvFJFgTGWFKQhKaTqhG0uDxesh378disBDpGc7yI7tUNLrDXXN8DJZId412RRe07OdI7TEW"
    "D1yKXBnGbxeP0epTfEKVJUkgpHaNnJaSKtmNxaQa57BuUy5HzhR8yIm7x/2CQwNtMxz2cBb/"
    "vYy37JNpLjWQuSttD4i1KPqHqEi0GwTetsy3xyanz7R8zJI169rOlhalc8K987+t6gTbAyNi"
    "Ii1RZNg/JSFkFAv3fV5Hi3CSTxt4O1xepBRH/dELpzl84VRVzc3yNIrcRT0eQNfmGdND7sT2"
    "i9VbpADR5H0oXbxRck782JAEwBxbIDvuNQEwIXIVbd44tAYnBdfrmOgwA1AH6GTBmZqWbhm3"
    "ehtiL5Sf7JhECyjWRjIaDNyRNuH1KsBHj56EYS2/37gLCCZE7BjSb8hrZk0g7TaF6ju1vmZq"
    "nvF3g8eaxSDz3LATzm0uoZ1l2+7PYkt9sfSq+4o41fyruNlWJUa73hM9atxN0xkz2Dpszw+L"
    "chwmg5mcX7JNTDDbwfJov6XdwMP2ea7xzpirliIO3N+OU7eCG7X1Vb2DpzEuftCoA1sWbrCc"
    "Nxwi1jOOpLhJ7yiK8gZCBlVCr8japPhXzfHjB/Bt9TLibCO5VtzKteqKn/2D39UPfd7xwt51"
    "85dbcppWUlFbhi7MyvwFKToVRdfpk6DaV8ZXFWuwGqy8osxkbvZGDwob/YNbvcnOBKe1WBRS"
    "WHOcMF04mytXgyS6D78Ak9bMS7YEJpnmkJW1j0slxQsoKa/qcnYXTTFFRIZGndo8b3VUrrKd"
    "c/fOkhGxhGBNCD5V6bTJkozZF0x9uZete39yXy77azGXK7sNSc/fbaJ5+NPh0XkrZ3/Z/6Qp"
    "j+EPxrLm+12Nik+tf1RjGaFI4q7Hc9tdf+sYqnYHl65c68HxqxTrcyGp0aXbDu4UBwvzBImO"
    "bKbE6InpWCNG6J4M6U0THWFS8sDcMZlThZwU/V1fw+Ved8oeNFPuya3WefRC0kpUufP7Av4H"
    "YOefHzvrW1YAAAAASUVORK5CYII=")
index.append('tool_restart')
catalog['tool_restart'] = tool_restart
gettool_restartData = tool_restart.GetData
gettool_restartImage = tool_restart.GetImage
gettool_restartBitmap = tool_restart.GetBitmap

#----------------------------------------------------------------------
viewmag_minus = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAABDlJ"
    "REFUOI21lFlslFUYhp9/mX+WFgq0nYWhUFuWUgjSlFgEwYWyFQNGbCQEWRJC1MRwgVti4oWJ"
    "F8YLL0RFEqQYIYIFQggSDBQEEaVIrFDAdqYMpZbWmU5b7HSW///P8WIARSOi6Ht1cnLOk/c7"
    "53s/+J+k/HGjtrbWcLuNNeVlY5/x+bxTQHP3xePRpvPnT3xWv+/DRCLR8I/BNTU1E2dOr9xc"
    "NaP6oVjaT891B+mMjbAGyFG7SPb8YG7d9vGWc+eaNwCDdwJrNxfV1dXjnlxcc7RqzspJzb0l"
    "FIz0MmXScMom5JMf9BO1AkQTI7R5M0qndXVcqei81rUbsO8IrqysdDz26Kz6OYvXTW78uZCp"
    "k5348xUUTSEjBGdbGrD1DhL6II2hOPeNUcZd6ro02iw3fyFICQFKGEkpQyklxlVAKABLljy+"
    "/KUXX90eUmeSMwLyDHCooKmw6YuXqQj6KPdOwrRNQAWpoEgFBRUkSKng1J20dLbxRt3b22L7"
    "Lq7WAcrGjV3tLCgj3gOaBVKAoYGmwDCXZMOCDRzuPEyePgTbFkgpEcJCCikUFAGQMhO88MAa"
    "WtvDs97d9yY6QHHxmKkpNReXExJpSKlZx6oCLscQLifbmFc/l1wjl1Q6hTQltmmDiYqJigBi"
    "cOr1kwwxPBaQBRuGM0fVFLy5kLYgaUHKyn6CEAJDdZDnziPfyCelppAOiW3ZCEsgTBtshXgm"
    "jtPhxJaCW+Devv5ep2Z6RjgMhMiCMzbYAjRVJS0y9Cf7sW37dscZwLrRG9chY2ZQFfU3cDh8"
    "+ZtHBqNLncNzcGtZ17YAISFjDVDqKWXv4j149BxsaYHIViIl2UNAKp2iatSD7DQPOW+B2yJX"
    "NkUuNC4tmVmErmk4VLAlSAnxwSRbj9cx3jsBM2GiyJuZUkCS7RIBBbrBjiN7qT+x/7vbkrdu"
    "7drtq9Y+u9w9poJct4oibzjOpDndcgyXWydtCpq/P0c03MSOPTt2WmXaFmwd0NCkrth9/Srt"
    "9gm6SdxKnj8QOBrt/unR4HBPUHUORTdcGA4Fl6Ez2jcWN8OI/XgVLR5j0cJaqj2Fwde+bQ9+"
    "eqr7k3Q4fVa2JcN0yhAJzNsi3dramvJ6ffWRcMgvErEpmYFepa8nRndHO20Xmrhw+ktONhyM"
    "Hfv84JHyQGD89FUr3eUrzfHlZy7OPxRJ7E9B/+8j/afpBlBUVDStpLj4iUJvQYWua3mxnt5o"
    "KBT+OhKJ7NoFHaUr5l4reeX+wmF2IxT42Ln8q+Y1xzsXJKHjr2bHXWm3yrIrNYolNxZK2Thb"
    "yo5l8qMZ/iYPBO4JDFAHK0ILdSHf80l5ZraU7U/LjdN9Z1xQdM/wD2B16yJdyvf9Up59WMqW"
    "p+T6UTn74UYf/1s9B3XvHLDU+TK2eaJT1TK5A3SnRf/f37xLvQXPH6hy9K4vVBv4L57iTvoV"
    "5X7ercqjtgAAAAAASUVORK5CYII=")
index.append('viewmag_minus')
catalog['viewmag_minus'] = viewmag_minus
getviewmag_minusData = viewmag_minus.GetData
getviewmag_minusImage = viewmag_minus.GetImage
getviewmag_minusBitmap = viewmag_minus.GetBitmap

#----------------------------------------------------------------------
viewmag_one = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAABAxJ"
    "REFUOI21lFlsVFUYx393mzt3pi1bO1MCDQ2CacFAcVAqKkWptlZjTLQpGgzQJ0ECkhANvhji"
    "k4lLQBZLXPpATKyI0YqkjRJpS5VFQgtUbDt1gC6W2doy01k69x4fpmyyGdF/cpKTL+f8vv/5"
    "zvkO/E+S/h6orKy0GYZt9ZyCWS+73a55oBhDoZC/7fTp5i/3flMTjUYPApBLIdk0k0UmKjYm"
    "sJZ6dlGCyiFS14ErKioKHy727F60uPSRQCKX4IhGImlipSI45T+JBdvHPvmstvZMtDs4zVOw"
    "8s2Vr7kenL1A7hvplV7fu2m409tZzD7OXue0tLR0ds2Orf2tJ/rEzu+iov6EKU71C3H2ohCH"
    "e4SoaYyITe83CffjxeLdPTVCCCHaA21iy5EtIiIiYmvjNsFSyi7zVACPx6M9VLzw4wcee3Hq"
    "z/2TKSpSmGAHBCQFOBxw/3wnF3wxqp+tYkNVNeU15bSEW4gqUZbNWIYqqSBjXQbLANOnT60s"
    "K3tmSXs4B9c0hWgC/JcgNApDMQjF4OIIGE6DAf8gKTlJycwS2te04zAc2NVxF9dIBiiYPWuV"
    "nl1ASEA8BUNxGE7AcDw9H0nApQRMmlFE469HOHLqDJtLN6PLOkkzedNXIQPk588oissZ2HWI"
    "JtLQoTiEx8HhWDom2TN5dd2HVK2vZtO2t3DaHVjCujXYZtOdsiLhyoBMHSQp7Xx0LD3GLNAU"
    "mGgXeObOZf0r24hZJjec/xqpAOGh4bCujDkmazYsC2IpSJpgjptRZdBVMFSJLAPi0SCIWzKv"
    "gr3eP35ZOup/Xp/kxFAgkUpDrfG9sgyanE7gtEM8Mnxb6JVS9PjOfeTrOIaBiapAhg0y9HRZ"
    "snTItIGhpWOjCQhd+B0ASZaEdGPzXgU3NDT80NjQ+Hns/ElSYxa6Bk4NHFoaaGiQZaRXn2xt"
    "Ih7uQ5YVTCuFGTVJmAlkSbkRDNA3MLBuX92eo8GOZkaCIVKmQFNB19KlGLwYorXxAKGe49zn"
    "WUh8LM5EZbK08dGNFE4pwBQmWFd5V9J0dXXFXS73Xp+3O9eKBuYlI2FpKBhgsPc8PR1tdBw9"
    "xOGDBwI/fX/gx0WFc+79+myL5JoySXpyWhneAS9vf7sl5o/53+M3/HCT3w0gLy9v4cz8/Ody"
    "XNkLVFWZEAiG/d3d3lafz1dXB733rHhiYOYb83Mmmscg280XL7WcWd3UXx6D3jve6u30lczy"
    "cxVSSmzPEeLYEiF6l4tPF+e2OWDqXYEBamFF91OqJXa4hTi+RIjzVWJ7sfu4HfLuGr4LVnU9"
    "rQqxM1eIEyVCdL4gNkx31sN4g/xbrYHaD/an5DIR2F2oy0oyI8Jgwrpz9/xTvQNr9y/Swhty"
    "5IP8F6W4nf4Cp1e+W6AIPCoAAAAASUVORK5CYII=")
index.append('viewmag_one')
catalog['viewmag_one'] = viewmag_one
getviewmag_oneData = viewmag_one.GetData
getviewmag_oneImage = viewmag_one.GetImage
getviewmag_oneBitmap = viewmag_one.GetBitmap

#----------------------------------------------------------------------
viewmag_plus = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAABHhJ"
    "REFUOI21lFlslUUYhp/5//8sPec0LXQ90JPW0iqFAF1YCiV1SRtqUdFAwxJWL0ANCUKMeKUh"
    "wagXBDVQpDHAhSGIS0SD0AgIQigtBQGBILSlLaUt3Vva07P8/4wXpyiKUSP6zs1kknnyfu/3"
    "zcD/JPHHg7KyMntUlH3VhPEZy5KSEieDHtXX09N58fLlk599daBiqH/o6N/w1APg0tLSrIL8"
    "vIoZs4pmdwWT6R6wEQxZSHMQt9bOcPel8If7yg+MLXlkQl5qnh4KhYVdd6qfmq6J76u+Xc1x"
    "8wRvobEJ+Su4qKgos+yFZ09MmrnAe6E1Ft8YJ2nJGjYDugfhct0QtxvqONa4nqObK7ljtqNG"
    "Voo9hRnrS34898GRXKWUEEIoAyAvL882M3/qx9OeXOytah1NdrZOjDNSVFAqXC5B7hQ3cWOn"
    "UNWZSkD6mbh7IlJITMuifmUdcZ5RIQAhhAIwAFJSvGVz5jxTeKk3gcSxMBSEUBh0LZLWteaL"
    "7DuzmVj7aOKiNVw2N3GOOKSShHWTaEc03tjkSflrS2q7hwbljZpTrxoA4zMzVjrix9PTDboJ"
    "SoJdB11EOnHowvscXr8Xv+XHZXfR0t+CaZqErBACQUtfCzs2vOuSyDynFsVzG5fvNgDS0lKz"
    "A5oHpyPiNqCBTQNtpAOZyZm0B9rIKp9AjDsGgLAVRgiBVJLifcUooei920f16tNMzciOZGy3"
    "O9yaLkj0QNCEYRMC5m/TEgqHsJRkKDyEJ+whLMMIBCoyWVhYGJpBwBxGKknADAoDoLevv9eh"
    "h12jbXakjIBDFlgyAnba7SBBDGv4DT9CCTRNG5lYIlkThmGQlsRpOCKO6+tvnnnC3znfMcpN"
    "lB5xbUmQIxcbOq6T4kmh8bWbRDujae5tpnhPMQErgC50Di87TEb8OEJWiGSPl01N2x0GQENj"
    "00eNV8/OTy/wYeg6Ng0sBUpFXlBJ9oss3LGKJHcyygqxZcU7yLBEILCUxaMJmby5a8vwrfZb"
    "1zv773Km5vgbBkBlZeWRVJ9v7wpf+pKo1Bw8URpCRRwrpZidVchTkwsJWrChfDGWNBnoGYiU"
    "b0EgHORGa92V797+fNq9vhj3Nrfb2tZ+uf+TjJK5g9Nl2iTcMaNw2AWaEIRMyZ2OPq6eq6a/"
    "vx2XzU3N6zVILFDgjfYy6L9rB1i9c6etYs0a63d/xbx582IT4+O35uTmLB+TmqE5PDFYlmSg"
    "r4e25gbO11Z3VV89+XPuwoKC6Y/lQ7iTQEcgVNVxu/3gqa9f4pj/0AN/xf3y+XxT09PSnk9I"
    "jM8xDD2mq7u3s66u/nRjY+P+/dAybmlxW/rGKQmx1lmIT+LTJaeurPqhtWQYWv6M94/1hcai"
    "plJhqm0JSp0tVKplkdo1K/miC7wPBQbYA0vrnjak2p6kVG2hUs0L1bb8pFon+B4avgNW3phr"
    "KFWerNT5x5W6vkCtS3F/A/dNxb/Ry7Bn60FTm6O6KrIcmh7yDHInKPsf2vE9vQevHJxh612X"
    "oB3jv4jir/QLPNP1XkCVsjAAAAAASUVORK5CYII=")
index.append('viewmag_plus')
catalog['viewmag_plus'] = viewmag_plus
getviewmag_plusData = viewmag_plus.GetData
getviewmag_plusImage = viewmag_plus.GetImage
getviewmag_plusBitmap = viewmag_plus.GetBitmap

#----------------------------------------------------------------------
view_nofullscreen = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAA7xJ"
    "REFUOI3NlU2MVEUQx3/Vr9/M7sAuu8RVFlASXFxEMfHCxRMX4xGPGkWNukEOejBI4tnEk9GD"
    "iSYK+JXowUQIJnrCi8YEEk9CoiKgK5v9YqILM7vzXleVh/dmAA1HEzupVH+9f/1fd/2r4T9q"
    "Mjp68Nyu3ZM7JURP6hjgBgaYV+a1134fMLthvb8XwVSlfenybNz94NbpQ++8KCs+LMWakQwK"
    "hVIhGaS6X2rdt3+M+3MJVAK9suT0m29vjTHL+aWdc+Z3QwsdMFOtfc3sxnGyet6qOasJeHDG"
    "RyPEBtEk58LZBVorPcbXB9QAEaTZqGkkEMEDCEAG7k6IkZDnWNEDc0IGvcL4YXGYImXEbilM"
    "rDNmHp1ky0QLcDCBn87BbRthYhug/Sup1sko24sUs3O0dt2P5BmQ6HQSM8dWOFMIwSRQuuBk"
    "9YeB5c+/4OcX9rM6N18DZrWF2kN3+S++f2WGi59+giKUBag5yQVCICgZqiBSQcwdP0Hn1NNs"
    "2LNK8qFB+rg77o6qAaBF5K6HcuT0DH8cOYo18mqfgUlWMTaEkDeY+/Irzr71ErZpjBXfhTRj"
    "DVqnmTlmjgLZcEQ7UwxvmKT7/mHa732A5M0q5YIQVQLJwIqC8Z3b2f3aRwQfYmhshHU7tuMD"
    "tlYHcMpeSXPrHUzsf5Vi6SDjD5fkw0OkTgczh5ARXTLUHHBaU9O0pqZv+n28WjO7HsDUMXeG"
    "7tlBc7oiJqlA+8AIUUNA/dbS9DpPK/C+WXUkndXKqyJUMjQAyYgm1eVVuizxJGgSQgRy+RfY"
    "gLGAklGuKWQR0Q6CVCRCqM5YCYRGTvfESZaOv0vzgUm6djebHn+O5pZJvFcMArgZHnOK5TbL"
    "nx0lNs6z+ONF8nv3se2pZzDvQT8rVA0cWnv3YmObie0PkfQ11y5fwQFVG1hSR7OMtYUVRjrf"
    "cPvaMfLYYmzvI5gmtKJMUMmqCpVKGBvjztePsMTzzH57AXLDAFXH3DCrAyRDorN25ldmz+9j"
    "48sf09w8QdldrUpfCESTgPl1gcRWYOrwG/jR+2iubxAByxxV8AwCjnmi0TCKPc+y4bEnYQS0"
    "c5U8RjKRKt0ki6wVztz8NXClVyghi4w8cYArnS5XLrXremy4GeaO6SoWRrH9B7CixBeuAk4W"
    "SlZ7NXAWke7QKIdOdnEr0LoU9ou3KiSvs8MFNcdMUBeMHqpgnuPmqMGfvg6GReL8fPu3dOq7"
    "bWq5J3VcKr33gQdyrl8O95tfGO9rwKvqJ5KEa4sLt1bG/7X9DULDkJiJPh7hAAAAAElFTkSu"
    "QmCC")
index.append('view_nofullscreen')
catalog['view_nofullscreen'] = view_nofullscreen
getview_nofullscreenData = view_nofullscreen.GetData
getview_nofullscreenImage = view_nofullscreen.GetImage
getview_nofullscreenBitmap = view_nofullscreen.GetBitmap

